from typing import Dict, List, Optional
from pydantic import BaseModel, model_validator

class PredictRequest(BaseModel):
    features: Optional[Dict[str, float]] = None
    rows: Optional[List[Dict[str, float]]] = None

    @model_validator(mode="after")
    def check_exclusive(self):
        if (self.features is None) and (self.rows is None):
            raise ValueError("Provide either 'features' or 'rows'.")
        if (self.features is not None) and (self.rows is not None):
            raise ValueError("Provide only one of 'features' or 'rows', not both.")
        return self

class PredictResponse(BaseModel):
    yhat: List[float]
    n: int
    runtime_ms: float
    model_name: str
    token: Optional[str] = None
    details: Optional[Dict] = None
