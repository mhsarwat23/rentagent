"""
Price Prediction Agent for RentAgent.

Estimates expected monthly rent from property characteristics using the
gradient-boosted model trained for RQ1. Prediction is made by the trained
model rather than by a language model call, so the estimate is deterministic
and reproducible.
"""

from pathlib import Path
import joblib
import numpy as np
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[2]
MODEL_PATH = PROJECT_ROOT / 'src' / 'models' / 'rent_model.joblib'
SPATIAL = pd.read_csv(PROJECT_ROOT / 'data' / 'processed' / 'district_spatial.csv').set_index('district')

_bundle = joblib.load(MODEL_PATH)
MODEL = _bundle['model']
FEATURES = _bundle['features']

def predict_rent(district, bedrooms, bathrooms=None, property_type='Flat',
                 furnish_type='Furnished', station_distance=0.5, is_shared=0):
    """
    Predict expected monthly rent for a property.

    Returns the prediction in pounds. The model is trained on log rent, so the
    output is exponentiated before returning.
    """
    if district not in SPATIAL.index:
        return None

    loc = SPATIAL.loc[district]

    row = {f: 0 for f in FEATURES}
    row['BEDROOMS'] = bedrooms
    row['BATHROOMS'] = bathrooms if bathrooms is not None else np.nan
    row['avg_distance_to_nearest_station'] = station_distance
    row['easting'] = loc['easting']
    row['northing'] = loc['northing']
    row['dist_centre_km'] = loc['dist_centre_km']
    row['is_shared'] = is_shared

    pt_col = f'PROPERTY TYPE_{property_type}'
    if pt_col in row:
        row[pt_col] = 1

    ft_col = f'Furnish Type_{furnish_type}'
    if ft_col in row:
        row[ft_col] = 1

    X = pd.DataFrame([row])[FEATURES]
    return float(np.exp(MODEL.predict(X)[0]))

if __name__ == '__main__':
    for d in ['SE13', 'W8', 'E14']:
        p = predict_rent(d, bedrooms=2, bathrooms=1)
        print(f"{d}: £{p:,.0f}")