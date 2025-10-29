# Solana Forecast API (Saifur – Individual Submission)

Predicts next-day HIGH for SOL using an ElasticNet-based pipeline trained with time-series CV (n_splits=3) on engineered technical indicators.

## Endpoints
- GET /health
- GET /features
- POST /predict

Example:
POST /predict
{
  "records": [{"pct_close_change":0.7, "rsi_14":51.2, "ema_close_7":145.2, "...":0.0}],
  "strict": false
}

## Quickstart
pip install -r requirements-min.txt
uvicorn app.main:app --reload

## Docker
docker build -t solana-api .
docker run -p 8000:8000 solana-api

## Model
- Best: ElasticNet pipeline (KBest + RobustScaler + ElasticNet)
- CV (MAE mean): 6.60 vs naive/roll7 baselines …
- Features: see `artifacts/solana_feature_columns.json`

## Notes
This repository contains only my API component extracted from the group project.