from fastapi import APIRouter
from app.core.config import settings
from app.services.pipeline_loader import get_pipeline, get_feature_names

router = APIRouter()

@router.get("/health")
def health():
    details = {}
    try:
        pipe = get_pipeline()
        details["model_loaded"] = True
        details["estimator"] = type(pipe).__name__
        details["n_features"] = len(get_feature_names())
    except Exception as e:
        details["model_loaded"] = False
        details["error"] = str(e)

    return {
        "status": "ok" if details.get("model_loaded") else "error",
        "token": settings.TOKEN,
        "details": details,
    }

@router.get("/version")
def version():
    return {
        "api": "solana-forecast-api",
        "token": settings.TOKEN,
        "model_path": settings.MODEL_PATH,
        "features_json": settings.FEATURES_JSON,
    }
