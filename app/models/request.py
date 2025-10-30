from typing import Dict, List, Optional
from pydantic import BaseModel, ConfigDict, field_validator

# You can optionally enforce typed columns, but Dict is also fine.
# If you want hard-coded feature names later, we can generate a typed class dynamically.
class FeatureRow(BaseModel):
    __annotations__ = {}

class PredictRequest(BaseModel):
    """
    Request schema for prediction.
    - `features`: single inference
    - `rows`: batch inference
    """

    model_config = ConfigDict(extra="forbid")

    features: Optional[Dict[str, float]] = None
    rows: Optional[List[Dict[str, float]]] = None

    # Empty list -> None
    @field_validator("rows", mode="before")
    @classmethod
    def empty_list_to_none(cls, v):
        return None if v == [] else v

    # Single-row cannot be empty
    @field_validator("features")
    @classmethod
    def ensure_not_empty(cls, v):
        if v is not None and len(v) == 0:
            raise ValueError("`features` cannot be empty.")
        return v

    # Batch cannot be empty
    @field_validator("rows")
    @classmethod
    def ensure_rows_not_empty(cls, v):
        if v is not None and len(v) == 0:
            raise ValueError("`rows` cannot be an empty list.")
        return v

    # Ensure exactly one of (features, rows)
    @field_validator("*", mode="after")
    @classmethod
    def check_exactly_one(cls, values):
        features = values.get("features")
        rows = values.get("rows")
        if (features is None) == (rows is None):
            raise ValueError("Provide exactly one of 'features' or 'rows'.")
        return values
