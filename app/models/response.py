from typing import List, Optional
from pydantic import BaseModel, ConfigDict

class PredictResponse(BaseModel):
    model_config = ConfigDict(extra="ignore")
    yhat: List[float]
    n: int
    runtime_ms: float
    model_name: str
    token: str
    details: Optional[dict] = None
