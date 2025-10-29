from typing import Dict, List, Optional
from pydantic import BaseModel, ConfigDict, field_validator

class PredictRequest(BaseModel):
    """Accept either a single row via `features` or a batch via `rows`."""
    model_config = ConfigDict(extra="forbid")

    features: Optional[Dict[str, float]] = None
    rows: Optional[List[Dict[str, float]]] = None

    @field_validator("rows", mode="before")
    @classmethod
    def empty_list_to_none(cls, v):
        return None if v == [] else v

    @field_validator("features")
    @classmethod
    def ensure_not_empty(cls, v):
        if v is not None and len(v) == 0:
            raise ValueError("`features` cannot be empty.")
        return v

    @field_validator("rows")
    @classmethod
    def ensure_rows_not_empty(cls, v):
        if v is not None and len(v) == 0:
            raise ValueError("`rows` cannot be an empty list.")
        return v

    @field_validator("*", mode="after")
    @classmethod
    def check_exactly_one(cls, values):
        features = values.get("features")
        rows = values.get("rows")
        if (features is None) == (rows is None):
            raise ValueError("Provide exactly one of 'features' or 'rows'.")
        return values
