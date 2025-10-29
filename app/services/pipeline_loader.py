import json
from functools import lru_cache
from pathlib import Path
import joblib

from app.core.config import settings

@lru_cache(maxsize=1)
def get_pipeline():
    """Load and cache the trained sklearn pipeline."""
    path = Path(settings.MODEL_PATH)
    if not path.exists():
        raise FileNotFoundError(f"Model not found at {path.resolve()}")
    return joblib.load(path)

@lru_cache(maxsize=1)
def get_feature_names():
    """Load the feature-name list used during training."""
    path = Path(settings.FEATURES_JSON)
    if not path.exists():
        raise FileNotFoundError(f"Feature JSON not found at {path.resolve()}")
    with open(path, "r") as f:
        data = json.load(f)

    # Accept list or dict formats
    if isinstance(data, list):
        cols = data
    elif isinstance(data, dict):
        cols = (
            data.get("feature_names")
            or data.get("safe_features")
            or data.get("columns")
            or list(data.keys())
        )
    else:
        raise ValueError("Unsupported features JSON format.")

    if not isinstance(cols, list) or len(cols) == 0:
        raise ValueError("No feature names found in JSON.")
    return cols
