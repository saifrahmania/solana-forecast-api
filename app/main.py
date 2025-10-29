from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.api.v1.endpoints.health import router as health_router
from app.api.v1.endpoints.predict import router as predict_router

app = FastAPI(title="Solana Forecast API", version="0.1.0")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routes
app.include_router(health_router, prefix=settings.API_PREFIX, tags=["health"])
app.include_router(predict_router, prefix=settings.API_PREFIX, tags=["predict"])
