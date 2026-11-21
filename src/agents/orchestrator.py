"""
Orchestrator for RentAgent.

Routes between the specialised agents and assembles the final recommendation.

Routing is conditional but deterministic. The Alternatives agent runs only when
no property satisfies the household's constraints, and the Rights agent only
when a tenancy question is asked. These conditions are facts about the request
rather than judgements requiring a language model, so delegating them would add
latency and failure modes without adding reasoning.

This also preserves the experimental design: the independent variable is the
division of reasoning between specialists, not the delegation of control flow.
Model-directed routing would introduce a second variable and reintroduce the
inter-agent coordination failures documented by Cemri et al. (2025).
"""

from profile_agent import build_constraints
from affordability_agent import assess_affordability
from alternatives_agent import cheaper_areas, bedroom_options, budget_gap
from price_agent import predict_rent

def recommend(household, rent, rights_question=None):
    """
    Produce a recommendation for a household and a candidate property.

    household:       raw household profile, including composition
    rent:            monthly rent of the candidate property
    rights_question: optional tenancy question

    Household composition is consumed by the Profile agent and does not appear
    in anything passed to subsequent agents.
    """
    trace = []

    # 1. Sanitisation boundary: composition in, constraints out
    constraints = build_constraints(household)
    trace.append('profile')

        # 2. Expected rent for a property of this specification in this area
    expected = predict_rent(
        district=constraints['area'],
        bedrooms=constraints['preferred_bedrooms'],
    )
    trace.append('price_prediction')

    # 3. Affordability against total occupancy cost
    affordability = assess_affordability(constraints, rent)
    trace.append('affordability')

    result = {
        'constraints': constraints,
        'expected_rent': round(expected) if expected else None,
        'asking_vs_expected': round(rent - expected) if expected else None,
        'affordability': affordability,
        'alternatives': None,
        'rights': None,
        'agents_called': trace,
    }

    # 4. Alternatives only if the property does not fit
    if not affordability['within_budget']:
        result['alternatives'] = {
            'cheaper_areas': cheaper_areas(constraints).to_dict('records'),
            'bedroom_options': bedroom_options(constraints),
            'budget_gap': budget_gap(
                constraints, affordability.get('market_30th_percentile', rent)
            ),
        }
        trace.append('alternatives')

    return result

if __name__ == '__main__':
    household = {
        'adult_couples': 1,
        'single_adults': 0,
        'children': [
            {'age': 6, 'sex': 'M'},
            {'age': 8, 'sex': 'F'},
            {'age': 12, 'sex': 'M'},
            {'age': 16, 'sex': 'F'},
        ],
        'budget_max': 2200,
        'area': 'SE13',
        'property_type': 'Flat',
        'preferred_bedrooms': 3,
    }

    r = recommend(household, rent=2000)
    print("Constraints:", r['constraints'])
    print("Within budget:", r['affordability']['within_budget'])
    print("Agents:", r['agents_called'])
    print()

    r = recommend(household, rent=2600)
    print("Expected rent: £", r['expected_rent'])
    print("Asking vs expected: £", r['asking_vs_expected'])
    print("Within budget:", r['affordability']['within_budget'])
    print("Agents:", r['agents_called'])
    print("Cheaper areas:", len(r['alternatives']['cheaper_areas']))