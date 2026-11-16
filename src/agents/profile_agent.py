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

    This is the sanitisation boundary. Household composition is consumed here
    and does not appear in the returned object. Only derived numerical and
    categorical constraints cross to downstream agents.

    household: dict containing
        adult_couples, single_adults, children,
        budget_max, area, property_type, preferred_bedrooms

    Returns dict: the constraint object.
    """
    occupants = (household['adult_couples'] * 2
                 + household['single_adults']
                 + len(household['children']))

    min_bedrooms = bedroom_standard(
        household['adult_couples'],
        household['single_adults'],
        household['children'],
    )

    # A stated preference may exceed the statutory floor but never fall below it
    preferred = household.get('preferred_bedrooms', min_bedrooms)
    preferred = max(preferred, min_bedrooms)

    return {
        'occupants': occupants,
        'min_bedrooms': min_bedrooms,
        'preferred_bedrooms': preferred,
        'budget_max': household['budget_max'],
        'area': household['area'],
        'property_type': household['property_type'],
    }