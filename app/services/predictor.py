from typing import Dict, List
import numpy as np
import pandas as pd

from app.services.pipeline_loader import get_pipeline, get_feature_names

def _rows_to_frame(rows: List[Dict[str, float]]) -> pd.DataFrame:
    cols = get_feature_names()
    df = pd.DataFrame(rows)

    # Add any missing columns with 0.0; keep only expected columns; enforce float dtype
    for c in cols:
        if c not in df.columns:
            df[c] = 0.0
    df = df[cols].astype(float)
    df = df.replace([np.inf, -np.inf], 0.0).fillna(0.0)
    return df

def predict_rows(rows: List[Dict[str, float]]) -> List[float]:
    pipe = get_pipeline()
    X = _rows_to_frame(rows)
    preds = pipe.predict(X)
    # Ensure list[float]
    return [float(p) for p in np.ravel(preds)]
