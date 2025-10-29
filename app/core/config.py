from typing import List
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    API_PREFIX: str = "/api/v1"
    PORT: int = 8000
    LOG_LEVEL: str = "INFO"

    MODEL_PATH: str = "artifacts/solana_best_pipeline_elasticnet.joblib"
    FEATURES_JSON: str = "artifacts/solana_feature_columns.json"

    TOKEN: str = "SOL"
    CORS_ORIGINS: List[str] = ["*"]

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

settings = Settings()
