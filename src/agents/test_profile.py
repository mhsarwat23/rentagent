from profile_agent import bedroom_standard

# Boy 8, girl 12 -> 2 bedrooms
print(bedroom_standard(1, 0, [
    {'age': 8, 'sex': 'M'},
    {'age': 12, 'sex': 'F'},
]))

# Boy 8, girl 9 -> both under 10, share. 1 couple + 1 = 2
print("boy 8, girl 9:", bedroom_standard(1, 0, [
    {'age': 8, 'sex': 'M'},
    {'age': 9, 'sex': 'F'},
]))

# Boy 7, girl 7, boy 14 -> under-10s pair, 14 alone. 1 + 2 = 3
print("boy 7, girl 7, boy 14:", bedroom_standard(1, 0, [
    {'age': 7, 'sex': 'M'},
    {'age': 7, 'sex': 'F'},
    {'age': 14, 'sex': 'M'},
]))

# Boy 7, boy 9, boy 14 -> two pair, one alone. 1 + 2 = 3
print("three boys 7, 9, 14:", bedroom_standard(1, 0, [
    {'age': 7, 'sex': 'M'},
    {'age': 9, 'sex': 'M'},
    {'age': 14, 'sex': 'M'},
]))

# Single adult, no children -> 1
print("single adult:", bedroom_standard(0, 1, []))

# Couple, no children -> 1
print("couple:", bedroom_standard(1, 0, []))

# Boy 9 alone with a boy 14 -> under-10 pairs with same-sex older. 1 + 1 = 2
print("boy 9, boy 14:", bedroom_standard(1, 0, [
    {'age': 9, 'sex': 'M'},
    {'age': 14, 'sex': 'M'},
]))

from profile_agent import build_constraints

# Couple with two young children, preferring 3 bedrooms
household = {
    'adult_couples': 1,
    'single_adults': 0,
    'children': [
        {'age': 6, 'sex': 'M'},
        {'age': 8, 'sex': 'F'},
    ],
    'budget_max': 2200,
    'area': 'SE13',
    'property_type': 'Flat',
    'preferred_bedrooms': 3,
}

print(build_constraints(household))

# Same household asking for 1 bedroom - should be clamped to the floor
household['preferred_bedrooms'] = 1
print(build_constraints(household))