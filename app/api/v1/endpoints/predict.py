import time
from fastapi import APIRouter, HTTPException

from app.core.config import settings
from app.models.request import PredictRequest
from app.models.response import PredictResponse
from app.services.predictor import predict_rows
from app.services.pipeline_loader import get_pipeline

router = APIRouter()

@router.post("/predict", response_model=PredictResponse)
def predict(req: PredictRequest):
    start = time.time()

    # Single-row -> list
    if req.features is not None:
        rows = [req.features]
    else:
        rows = req.rows or []

    if len(rows) == 0:
        raise HTTPException(status_code=400, detail="No rows to predict.")

    try:
        yhat = predict_rows(rows)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Inference failed: {e}")

    duration_ms = (time.time() - start) * 1000.0
    model_name = type(get_pipeline()).__name__

    return PredictResponse(
        yhat=yhat,
        n=len(yhat),
        runtime_ms=duration_ms,
        model_name=model_name,
        token=settings.TOKEN,
    )
