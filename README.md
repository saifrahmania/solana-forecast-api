# 🚀 Solana Forecast API

Predicts the **next-day HIGH price** of the Solana (SOL) cryptocurrency using a production-ready machine learning pipeline.  
The model is trained on engineered technical indicators, rolling window features, volatility signals, and cyclical time encodings.

This API exposes a lightweight prediction service suitable for backtesting, dashboards, and analytics systems.

---

## ✅ Features

- ⚡ Fast, low-latency predictions
- 📦 Pre-loaded trained pipeline (ElasticNet + RobustScaler + KBest)
- 🧾 Strict schema validation via Pydantic
- 🔁 Supports single or batch inference
- 🔐 Deterministic reproducibility via stored artifacts
- 🐳 Fully Dockerized deployment

---

## 📦 Artifacts Included

| File | Description |
|------|-------------|
| `solana_best_pipeline_elasticnet.joblib` | Main prediction pipeline |
| `solana_feature_columns.json` | Ordered feature list |
| `solana_scaler_top20.pkl` | Alternate scaler |
| `solana_rf_top20.pkl` | Random Forest variant |
| `solana_model_metadata_top20.pkl` | CV scores, hyperparameters |

All artifacts are automatically loaded at startup.

---

## 🔗 API Endpoints

### ✅ Health Check
`GET /api/v1/health`

```json
{ "status": "ok" }
```
