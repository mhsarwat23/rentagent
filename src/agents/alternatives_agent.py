"""
Alternatives Agent for RentAgent.

Generates ranked relaxations when a household's constraints cannot be jointly
satisfied. Receives only the sanitised constraint object; no household
composition attributes cross the boundary described in Section 3.5.

Bedroom relaxations never fall below min_bedrooms, which is the statutory floor
derived from the Local Housing Allowance size criteria. Suggesting fewer would
propose overcrowding.
"""

from pathlib import Path
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[2]
PROCESSED = PROJECT_ROOT / 'data' / 'processed'

DISTRICT_BRMA = pd.read_csv(PROCESSED / 'district_brma.csv').set_index('district')
DISTRICT_SPATIAL = pd.read_csv(PROCESSED / 'district_spatial.csv').set_index('district')

def nearby_districts(district, max_km=5.0):
    """
    Find districts within max_km of the given district's centroid.

    Uses easting and northing from the ONS Postcode Directory. These are
    metres on the British National Grid, a flat projection, so straight-line
    distance is computed directly.

    Returns a DataFrame of nearby districts with their distance in km.
    """
    if district not in DISTRICT_SPATIAL.index:
        return pd.DataFrame()

    origin = DISTRICT_SPATIAL.loc[district]

    d = DISTRICT_SPATIAL.copy()
    d['distance_km'] = (
        ((d['easting'] - origin['easting']) ** 2 +
         (d['northing'] - origin['northing']) ** 2) ** 0.5
    ) / 1000

    nearby = d[(d['distance_km'] <= max_km) & (d.index != district)]
    return nearby[['distance_km']].sort_values('distance_km')

from affordability_agent import (
    brma_for_district, council_tax_for_district,
    LHA_RATES, MARKET_30TH, LHA_CATEGORY, weekly_to_monthly,
)

def cheaper_areas(constraints, max_km=5.0, limit=5, min_confidence=0.80):
    """
    Find nearby districts where the total benchmark cost is lower.
    Compares the 30th percentile market rent for the household's bedroom
    entitlement plus council tax, so the comparison reflects what a tenant
    would actually pay rather than rent alone.
    """
    origin = constraints['area']
    category = LHA_CATEGORY.get(min(constraints['min_bedrooms'], 4), 'CAT E')

    def total_cost(district):
        brma, conf = brma_for_district(district)
        if brma is None or brma not in MARKET_30TH.index:
            return None
        rent = weekly_to_monthly(MARKET_30TH.loc[brma, category])
        ct, _ = council_tax_for_district(district)
        return rent + (ct or 0), brma, conf

    base = total_cost(origin)
    if base is None:
        return pd.DataFrame()

    rows = []
    for district, row in nearby_districts(origin, max_km).iterrows():
        result = total_cost(district)
        if result is None:
            continue
        cost, brma, conf = result
        # Districts spanning multiple rental market areas are excluded, since
        # the benchmark may not apply to the part of the district a tenant
        # would actually search in
        if cost < base[0] and conf >= min_confidence:
            rows.append({
                'district': district,
                'distance_km': round(row['distance_km'], 1),
                'brma': brma,
                'monthly_benchmark': round(cost),
                'saving': round(base[0] - cost),
                'confidence': round(conf, 2),
            })

    # An empty result has no columns, so sorting on 'saving' would fail
    out = pd.DataFrame(rows)
    if out.empty:
        return out
    return out.sort_values('saving', ascending=False).head(limit)

def bedroom_options(constraints):
    """
    Bedroom counts the household could consider.

    The statutory floor from the Local Housing Allowance size criteria is never
    breached: a household entitled to three bedrooms is not offered a
    two-bedroom property, since that would propose overcrowding.
    """
    floor = constraints['min_bedrooms']
    preferred = constraints['preferred_bedrooms']

    options = []
    for n in range(preferred, floor - 1, -1):
        options.append({
            'bedrooms': n,
            'at_statutory_floor': n == floor,
            'below_preference': n < preferred,
        })
    return options

def budget_gap(constraints, benchmark_monthly):
    """
    Quantify the gap between the household's budget and the local benchmark.

    Reports the shortfall in pounds and as a percentage, so a user can judge
    whether the requirement is marginally or substantially unrealistic.
    """
    budget = constraints['budget_max']
    gap = benchmark_monthly - budget

    return {
        'budget_max': budget,
        'benchmark_monthly': round(benchmark_monthly),
        'achievable': gap <= 0,
        'shortfall': round(max(0, gap)),
        'shortfall_pct': round(max(0, gap) / budget * 100, 1) if budget else None,
    }

if __name__ == '__main__':
    print(nearby_districts('SE13').head(10))

    constraints = {'area': 'SE13', 'min_bedrooms': 2, 'budget_max': 2200}
    print(cheaper_areas(constraints))

    c = {'area': 'SE13', 'min_bedrooms': 2, 'preferred_bedrooms': 3, 'budget_max': 2200}
    for opt in bedroom_options(c):
        print(opt)

    print(budget_gap(c, 1904))

    tight = dict(c, budget_max=1500)
    print(budget_gap(tight, 1904))