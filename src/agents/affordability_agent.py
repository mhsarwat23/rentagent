"""
Affordability Agent for RentAgent.

Assesses total cost of occupancy against a household's budget ceiling.
Receives only the sanitised constraint object; no household composition
attributes cross the boundary described in Section 3.5.
"""

from pathlib import Path
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_RAW = PROJECT_ROOT / 'data' / 'raw'
LHA_FILE = DATA_RAW / '2026-27_LHA_TABLES.xlsx'

# LHA size categories map to bedroom entitlement
LHA_CATEGORY = {
    0: 'CAT A',   # shared accommodation
    1: 'CAT B',
    2: 'CAT C',
    3: 'CAT D',
    4: 'CAT E',
}

# LHA is published weekly; rents are monthly
WEEKS_PER_MONTH = 52 / 12


def load_lha_rates():
    """
    Load both LHA tables.

    Table 4 holds the April 2026 LHA rates, used for cross-area comparison
    because they are set per BRMA on a consistent statutory basis.

    Table 2 holds the 30th percentile of actual market rents, used for
    affordability assessment. LHA rates have been frozen at April 2024 levels,
    so Table 4 understates current market cost.

    Returns (lha_rates, market_30th) as DataFrames indexed by BRMA.
    """
    lha = pd.read_excel(LHA_FILE, 'Table 4', header=1).set_index('BRMA')
    market = pd.read_excel(LHA_FILE, 'Table 2', header=1).set_index('BRMA')
    return lha, market

def load_district_brma():
    """
    Load the district-to-BRMA mapping derived in notebooks/03_brma_lookup.ipynb.

    Returns a DataFrame indexed by postcode district, with the assigned BRMA
    and the modal share recording how much of that district the BRMA covers.
    """
    path = PROJECT_ROOT / 'data' / 'processed' / 'district_brma.csv'
    return pd.read_csv(path).set_index('district')

DISTRICT_BRMA = load_district_brma()

def brma_for_district(district):
    """
    Find the BRMA covering a postcode district.

    Returns (brma_name, modal_share). The modal share indicates confidence:
    1.0 means the district lies wholly within that BRMA, lower values mean
    the district spans more than one and the rate may not apply to every
    address within it.
    """
    if district not in DISTRICT_BRMA.index:
        return None, 0.0

    row = DISTRICT_BRMA.loc[district]
    return row['brma'], float(row['modal_share'])

# Loaded once at import; the published rates are fixed for the year
LHA_RATES, MARKET_30TH = load_lha_rates()

def weekly_to_monthly(weekly):
    """Convert a weekly rate to its monthly equivalent."""
    return weekly * WEEKS_PER_MONTH

def assess_affordability(constraints, rent):
    """
    Assess whether a property is affordable against the household's budget.

    constraints: the sanitised constraint object from the Profile agent
    rent:        monthly rent for the property

    The BRMA is derived from the constraint object's area. The returned
    assessment includes the mapping confidence so that a benchmark drawn from
    a district spanning multiple areas can be identified as such.
    """
    brma, confidence = brma_for_district(constraints['area'])

    if brma is None:
        return {
            'rent': rent,
            'within_budget': bool(rent <= constraints['budget_max']),
            'benchmark_available': False,
            'reason': f"No BRMA mapping for district {constraints['area']}",
        }

    category = LHA_CATEGORY.get(min(constraints['min_bedrooms'], 4), 'CAT E')
    lha_monthly = weekly_to_monthly(LHA_RATES.loc[brma, category])
    market_monthly = weekly_to_monthly(MARKET_30TH.loc[brma, category])

    return {
        'rent': rent,
        'budget_max': constraints['budget_max'],
        'within_budget': bool(rent <= constraints['budget_max']),
        'brma': brma,
        'brma_confidence': round(confidence, 3),
        'lha_benchmark': round(lha_monthly),
        'market_30th_percentile': round(market_monthly),
        'above_market_30th': bool(rent > market_monthly),
        'lha_shortfall': round(max(0, rent - lha_monthly)),
        'benchmark_available': True,
    }

lha, market = load_lha_rates()
print("Central London 2-bed LHA weekly:", lha.loc['Central London', 'CAT C'])
print("Central London 2-bed 30th pct:  ", market.loc['Central London', 'CAT C'])
print("Monthly equivalents:",
      round(weekly_to_monthly(lha.loc['Central London', 'CAT C'])),
      round(weekly_to_monthly(market.loc['Central London', 'CAT C'])))
# Test: couple with two young children, 2-bed entitlement, £2,200 budget
constraints = {
    'occupants': 4,
    'min_bedrooms': 2,
    'preferred_bedrooms': 3,
    'budget_max': 2200,
    'area': 'SE13',
    'property_type': 'Flat',
}

print()
print(assess_affordability(constraints, rent=2400))

print(brma_for_district('SE13'))
print(brma_for_district('N4'))
print(brma_for_district('ZZ99'))