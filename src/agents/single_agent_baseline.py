"""
Single-agent baseline for RentAgent.

Implements the comparison condition for RQ2. The agent has access to the same
data and the same underlying functions as the multi-agent system, and runs on
the same model with the same decoding parameters. The difference is structural:
reasoning is not divided between specialists, and the agent receives the full
household profile including composition.

Prompting follows ReAct (Yao et al., 2023) with chain-of-thought reasoning
(Wei et al., 2022), so the comparison is against a properly constructed
baseline rather than a naive single prompt.

Note the architectural asymmetry this creates. The multi-agent system consumes
household composition at the Profile agent and passes only derived constraints
onward. This baseline receives composition directly in its context, and nothing
structurally prevents it from conditioning an affordability judgement on it.
That asymmetry is the subject of RQ3.
"""

import json
from affordability_agent import (
    brma_for_district, council_tax_for_district,
    LHA_RATES, MARKET_30TH, LHA_CATEGORY, weekly_to_monthly,
)
from alternatives_agent import nearby_districts
from price_agent import predict_rent
from rights_agent import ask_model, retrieve

TOOLS = {
    'predict_rent': {
        'description': 'Predict the expected monthly rent for a property, '
                       'given a postcode district and bedroom count.',
        'args': ['district', 'bedrooms'],
    },
    'get_benchmarks': {
        'description': 'Get the Local Housing Allowance rate, the 30th '
                       'percentile of market rents, and the council tax for a '
                       'postcode district at a given bedroom count.',
        'args': ['district', 'bedrooms'],
    },
    'find_nearby_districts': {
        'description': 'List postcode districts within 5km of a given district.',
        'args': ['district'],
    },
    'search_act': {
        'description': 'Search the Renters Rights Act 2025 for provisions '
                       'relevant to a question.',
        'args': ['question'],
    },
    'finish': {
        'description': 'Give the final recommendation. Call this when you have '
                       'enough information.',
        'args': ['recommendation'],
    },
}


def run_tool(name, args):
    """Execute a tool and return its result as text."""
    if name == 'predict_rent':
        p = predict_rent(args['district'], args['bedrooms'])
        return f"Predicted rent: £{p:.0f}/month" if p else "District not found"

    if name == 'get_benchmarks':
        brma, conf = brma_for_district(args['district'])
        if brma is None:
            return "District not found"
        cat = LHA_CATEGORY.get(min(args['bedrooms'], 4), 'CAT E')
        lha = weekly_to_monthly(LHA_RATES.loc[brma, cat])
        mkt = weekly_to_monthly(MARKET_30TH.loc[brma, cat])
        ct, borough = council_tax_for_district(args['district'])
        return (f"Area: {brma}. LHA: £{lha:.0f}/month. "
                f"30th percentile market rent: £{mkt:.0f}/month. "
                f"Council tax ({borough}): £{ct:.0f}/month.")

    if name == 'find_nearby_districts':
        n = nearby_districts(args['district'])
        return ', '.join(n.index[:8].tolist()) or "None found"

    if name == 'search_act':
        hits = retrieve(args['question'], k=2)
        return '\n\n'.join(
            f"Section {h['section']}: {h['heading']}\n"
            f"Status: {'in force' if h['in_force'] else 'NOT YET COMMENCED'}\n"
            f"{h['text'][:1500]}"
            for h in hits
        )

    return f"Unknown tool: {name}"

MAX_ITERATIONS = 10

ACTION_SCHEMA = {
    'type': 'object',
    'properties': {
        'thought': {'type': 'string'},
        'tool': {'type': 'string', 'enum': list(TOOLS.keys())},
        'district': {'type': 'string'},
        'bedrooms': {'type': 'integer'},
        'question': {'type': 'string'},
        'recommendation': {'type': 'string'},
        'affordable': {'type': 'boolean'},
        'recommended_bedrooms': {'type': 'integer'},
        'recommended_district': {'type': 'string'},
    },
    'required': ['thought', 'tool'],
}


def run_baseline(household, rent, rights_question=None):
    """
    Single-agent baseline. The agent receives the full household profile,
    including composition, and decides for itself which tools to call.

    Returns the recommendation, the trace of tool calls, and any failures.
    """
    task = (
        f"You are advising a tenant looking for a rental property in London.\n\n"
        f"HOUSEHOLD: {json.dumps(household)}\n"
        f"CANDIDATE PROPERTY: £{rent}/month in {household['area']}\n"
    )
    if rights_question:
        task += f"THEY ALSO ASK: {rights_question}\n"

    # Offer the Act search only when a tenancy question was asked, so the
    # baseline is not presented with a tool the multi-agent system would
    # not have called either
    available = {n: t for n, t in TOOLS.items()
                 if n != 'search_act' or rights_question}

    tool_list = '\n'.join(
        f"- {n}({', '.join(t['args'])}): {t['description']}"
        for n, t in available.items()
    )

    history = []
    trace = []
    failures = []

    for step in range(MAX_ITERATIONS):
        prompt = (
            f"{task}\n"
            f"AVAILABLE TOOLS:\n{tool_list}\n\n"
            f"PREVIOUS STEPS:\n" + ('\n'.join(history) or '(none)') + "\n\n"
            f"You have used {step} of {MAX_ITERATIONS} steps. "
            f"Think about what you need, then choose one tool. "
            f"Do not call the same tool twice with the same arguments. "
            f"Call 'finish' as soon as you can advise the tenant.\n"
            f"When calling 'finish', you must also set: affordable (true or "
            f"false), recommended_bedrooms, and recommended_district.\n"
        )

        # Make the no-repetition constraint explicit rather than advisory
        if trace:
            used = set(trace)
            remaining = [n for n in available if n not in used or n == 'finish']
            prompt += f"Tools you have NOT yet used: {', '.join(remaining)}\n"

        # Force termination on the final step
        if step == MAX_ITERATIONS - 1:
            prompt += "This is your LAST step. You must call 'finish' now.\n"

        prompt += "Respond in JSON."

        try:
            raw = ask_model(prompt, schema=ACTION_SCHEMA)
            action = json.loads(raw)
        except Exception as e:
            failures.append(f"step {step}: unparseable response ({e})")
            break

        tool = action['tool']
        trace.append(tool)

        print(f"[{step}] {tool}: {action['thought'][:100]}")

        if tool == 'finish':
            return {
                'recommendation': action.get('recommendation', ''),
                'affordable': action.get('affordable'),
                'recommended_bedrooms': action.get('recommended_bedrooms'),
                'recommended_district': action.get('recommended_district'),
                'tools_called': trace,
                'steps': step + 1,
                'failures': failures,
                'completed': True,
            }

        result = run_tool(tool, action)
        history.append(
            f"Thought: {action['thought']}\n"
            f"Action: {tool}\nObservation: {result}"
        )

    failures.append(f"did not finish within {MAX_ITERATIONS} iterations")
    return {
        'recommendation': None,
        'affordable': None,
        'recommended_bedrooms': None,
        'recommended_district': None,
        'tools_called': trace,
        'steps': MAX_ITERATIONS,
        'failures': failures,
        'completed': False,
    }

if __name__ == '__main__':
    household = {
        'adult_couples': 1, 'single_adults': 0,
        'children': [{'age': 6, 'sex': 'M'}, {'age': 8, 'sex': 'F'}],
        'budget_max': 2200, 'area': 'SE13',
        'property_type': 'Flat', 'preferred_bedrooms': 3,
    }
    r = run_baseline(household, rent=2600)
    print("Tools:", r['tools_called'])
    print("Completed:", r['completed'])
    print()
    print(r['recommendation'])