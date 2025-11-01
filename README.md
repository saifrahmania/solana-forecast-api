# Solana Price Forecast API

A Machine Learning-based REST API for predicting Solana’s **next-day HIGH** price using an ElasticNet regression pipeline with engineered technical indicators, volatility features, and cyclical time encodings.

## Table of Contents

* [Overview](#overview)
* [Model Details](#model-details)
* [API Endpoints](#api-endpoints)
* [Installation](#installation)
* [Usage Examples](#usage-examples)
* [Testing](#testing)
* [Project Structure](#project-structure)
* [Model Training](#model-training)
* [Troubleshooting](#troubleshooting)
* [Deployment](#deployment)
* [Performance & Limitations](#performance--limitations)
* [Contributing](#contributing)
* [License](#license)

---

## Overview

This FastAPI service exposes a trained ML model capable of predicting **tomorrow’s HIGH** price for Solana (SOL).
The model was trained offline on historical OHLCV data, engineered technical indicators, volatility metrics, and calendar-driven features.

### Key Features

* ✅ Predicts **next-day HIGH**
* 🧠 ElasticNet regression pipeline
* 🔎 100+ engineered features
* ⏱ Low-latency inference
* 🧾 Strict schema validation
* 🐳 Docker support
* ⚙️ Time-series cross-validation
* 📦 Single or batch prediction

### Quick Stats

* **Algorithm**: ElasticNet (RobustScaler + K-Best)
* **Cross-Validation**: TimeSeriesSplit (n_splits = 3)
* **Performance**: ~6.60 MAE (CV mean)
* **Prediction Target**: Next-day HIGH
* **Features**: Rolling windows, candle geometry, cyclical dates, RSI, MACD…

---

## Model Details

### Algorithm & Architecture

**Model Type:** ElasticNet Regression
**Pipeline Components:**

```
RobustScaler → KBest → ElasticNet
```

### Why ElasticNet?

* Handles correlated indicators
* Avoids overfitting on noisy crypto patterns
* Sparse coefficients highlight signal features

### Performance Metrics

| Metric           | Value                        |
| ---------------- | ---------------------------- |
| MAE (CV mean)    | ~6.60                        |
| Cross-Validation | TimeSeriesSplit              |
| Robustness       | High (handles outliers well) |

### Feature Categories

* Lagged OHLC windows (1–90d)
* RSI (7,14)
* MACD line/signal/histogram
* Parkinson volatility
* Candle geometry (wicks, body)
* Volume ratios
* Bollinger metrics
* Calendar (month, quarter, DOW sine/cosine)
* Time elapsed index

Full list in:

```
artifacts/solana_feature_columns.json
```

---

## API Endpoints

### Base URLs

* Local: `http://localhost:8000`

---

### 1. GET `/api/v1/health`

Health probe to verify the service is running.

**Response:**

```json
{ "status": "ok" }
```

---

### 2. GET `/api/v1/version`

Returns the API version.

```json
"0.1.0"
```

---

### 3. GET `/api/v1/features`

Returns feature ordering expected by the model.

---

### 4. POST `/api/v1/predict`

Prediction target: **next-day HIGH**

You must provide exactly **one**:

| Field      | Meaning       |
| ---------- | ------------- |
| `features` | single row    |
| `rows`     | batch of rows |

Example:

```json
{
  "features": {
    "open_prev_1": 10.5,
    "high_prev_1": 10.7,
    "rsi_14": 48,
    "month": 10
  }
}
```

**Response:**

```json
{
  "yhat": [11.86],
  "n": 1,
  "runtime_ms": 47.66,
  "model_name": "Pipeline",
  "token": "SOL",
  "details": null
}
```

---

## Installation

### Requirements

* Python 3.11+
* pip
* Docker (optional)

---

### Method A — Local

Clone:

```bash
git clone https://github.com/<your_repo>/solana-forecast-api.git
cd solana-forecast-api
```

Install:

```bash
pip install -r requirements.txt
```

Run:

```bash
uvicorn app.main:app --reload
```

Swagger UI:

```
http://localhost:8000/docs
```

---

### Method B — Docker Deployment

Build:

```bash
docker build -t solana-api .
```

Run:

```bash
docker run -p 8000:8000 solana-api
```

Access:

```
http://localhost:8000/docs
```

---

## Usage Examples

### 1. Curl

```bash
curl -X POST http://localhost:8000/api/v1/predict \
 -H "Content-Type: application/json" \
 -d '{"features":{"open_prev_1":10.5,"rsi_14":48}}'
```

---

### 2. Python

```python
import requests

payload = {"features": {"open_prev_1":10.5, "rsi_14":48}}
res = requests.post("http://localhost:8000/api/v1/predict", json=payload)
print(res.json())
```

---

### 3. Batch Prediction

```json
{
  "rows": [
    { "open_prev_1": 10.5, "rsi_14": 48 },
    { "open_prev_1": 9.9, "rsi_14": 60 }
  ]
}
```

---

## Testing

Run included tests:

```bash
pytest
```

Integration tests ensure:

* Health
* Schema validation
* Pipeline inference correctness

---

## Project Structure

```
solana-forecast-api/
├── app/
│   ├── api/v1/endpoints/     # Route handlers
│   ├── models/               # Input/Output schemas
│   ├── services/             # Loader & predictor logic
│   └── core/                 # Settings
├── artifacts/                # Model artifacts
├── notebooks/                # Data exploration & training
├── scripts/                  # Convenience launchers
├── tests/                    # Unit + integration
├── Dockerfile
├── README.md
└── requirements.txt
```

---

## Model Training

All model training was done via notebooks:

```
notebooks/solana_model_building.ipynb
notebooks/solana_feature_engineering.ipynb
```

Training workflow:

1. Collect OHLCV data
2. Engineer ~100 features
3. Scale via RobustScaler
4. Select K-best
5. Train ElasticNet
6. Save artifacts:

```
solana_best_pipeline_elasticnet.joblib
solana_scaler_top20.pkl
solana_feature_columns.json
```

---

## Troubleshooting

**Error:**
`Provide exactly one of "features" or "rows"`

✅ Fix: remove one key.

---

**Invalid feature ordering**

Check:

```bash
GET /api/v1/features
```

---

**Docker model not found**

Make sure `artifacts/` is copied in Dockerfile.

---

## Deployment

Recommended cloud targets:

* AWS EC2
* Azure App Service
* Google Cloud Run
* DigitalOcean Droplets

Suggested env vars:

```bash
API_HOST=0.0.0.0
API_PORT=8000
LOG_LEVEL=INFO
```

---

## Performance & Limitations

### Current Capabilities

* Predicts next-day HIGH
* Batch support
* Low inference latency

### Limitations

* Single asset (SOL)
* No news/sentiment
* Next-day horizon only

### Future Work

* [ ] Multi-asset support
* [ ] Confidence intervals
* [ ] Streaming predictions

---

## Contributing

PRs welcome!

Guidelines:

* PEP-8 formatting
* Update tests
* Update documentation
* Atomic commits

---

## Dependencies

Core:

```
fastapi
uvicorn
pydantic
scikit-learn
pandas
numpy
joblib
```

See `requirements.txt` for versions.

---

## License

MIT License (if applicable).

---

## Acknowledgments

This project was developed as part of **Advanced Machine Learning Applications** coursework.

Thanks to:

* FastAPI team
* scikit-learn community
* UTS teaching staff

---

## Quick Start

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Open browser:

```
http://localhost:8000/docs
```

---

## Support

Open GitHub issues for questions or bugs.

---

**Version:** 0.1.0
**Last Updated:** November 2025
**Author:** Saifur Rahman

---


