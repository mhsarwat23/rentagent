"""
Profile Agent for RentAgent.

Converts household information into a numerical constraint object.
Household composition does not pass beyond this module: only the derived
constraints are returned, implementing the sanitisation boundary described
in Section 3.5 of the methodology.
"""


def bedroom_standard(adult_couples, single_adults, children):
    """
    Minimum bedroom entitlement under the Local Housing Allowance size criteria.

    One bedroom is allowed for each of:
      - an adult couple
      - any other adult aged 16 or over
      - any two children of the same sex under 16
      - any two children of either sex under 10
      - any other child

    adult_couples: int, number of adult couples
    single_adults: int, adults aged 16+ not in a couple
    children:      list of dicts, each {'age': int, 'sex': 'M' or 'F'}

    Returns int: minimum bedrooms required.
    """
    bedrooms = adult_couples + single_adults

    # Children under 10 may share regardless of sex
    under_10 = [c for c in children if c['age'] < 10]
    aged_10_to_15 = [c for c in children if 10 <= c['age'] < 16]

    # Pair off the under-10s
    bedrooms += len(under_10) // 2
    leftover_under_10 = len(under_10) % 2

    # Children aged 10 to 15 pair by sex
    boys = [c for c in aged_10_to_15 if c['sex'] == 'M']
    girls = [c for c in aged_10_to_15 if c['sex'] == 'F']

    # A leftover under-10 can pair with an older child of the same sex
    if leftover_under_10:
        odd_child = [c for c in under_10][-1]
        same_sex = boys if odd_child['sex'] == 'M' else girls
        if same_sex:
            same_sex.pop()          # that older child is now paired
            leftover_under_10 = 0
        bedrooms += 1               # the pair, or the lone child

    # Remaining 10-15s pair within their own sex
    bedrooms += (len(boys) + 1) // 2
    bedrooms += (len(girls) + 1) // 2

    return bedrooms

def build_constraints(household):
    """
    Convert a household profile into a sanitised constraint object.

    Anyone aged 16 or over is an adult under the Local Housing Allowance size
    criteria. Where such a person is supplied as a child, they are reclassified
    and a notice is returned alongside the constraints, so the reclassification
    is visible to the caller rather than silent.
    """
    children = list(household['children'])
    single_adults = household['single_adults']
    notices = []

    over_16 = [c for c in children if c['age'] >= 16]
    if over_16:
        children = [c for c in children if c['age'] < 16]
        single_adults += len(over_16)
        notices.append(
            f"{len(over_16)} household member(s) aged 16 or over were counted "
            f"as adults rather than children. Under the Local Housing Allowance "
            f"size criteria, a person aged 16 or over is entitled to their own "
            f"bedroom."
        )

    occupants = (household['adult_couples'] * 2
                 + single_adults
                 + len(children))

    min_bedrooms = bedroom_standard(
        household['adult_couples'], single_adults, children
    )

    preferred = max(household.get('preferred_bedrooms', min_bedrooms), min_bedrooms)

    return {
        'constraints': {
            'occupants': occupants,
            'min_bedrooms': min_bedrooms,
            'preferred_bedrooms': preferred,
            'budget_max': household['budget_max'],
            'area': household['area'],
            'property_type': household['property_type'],
        },
        'notices': notices,
    }