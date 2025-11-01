# app/models/request.py
from typing import Dict, List, Optional
from pydantic import BaseModel, ConfigDict, model_validator, field_validator

class PredictRequest(BaseModel):
    """
    Request schema for prediction.
    - `features`: single-row inference (dict of feature_name -> float)
    - `rows`: batch inference (list of dicts)
    """
    model_config = ConfigDict(extra="forbid")

    features: Optional[Dict[str, float]] = None
    rows: Optional[List[Dict[str, float]]] = None

    # Optional safety checks
    @field_validator("features")
    @classmethod
    def ensure_features_not_empty(cls, v):
        if v is not None and len(v) == 0:
            raise ValueError("`features` cannot be an empty object.")
        return v

    @field_validator("rows")
    @classmethod
    def ensure_rows_not_empty(cls, v):
        if v is not None and len(v) == 0:
            raise ValueError("`rows` cannot be an empty list.")
        return v

    # ✅ Correct way in Pydantic v2 to validate across multiple fields
    @model_validator(mode="after")
    def check_exactly_one(self):
        has_features = self.features is not None
        has_rows = self.rows is not None
        if has_features == has_rows:
            # both True or both False → invalid
            raise ValueError("Provide exactly one of 'features' or 'rows'.")
        return self
