from fastapi.testclient import TestClient
from app.main import app
from app.services.pipeline_loader import get_feature_names

def test_health():
    c = TestClient(app)
    r = c.get("/api/v1/health")
    assert r.status_code == 200

def test_predict_minimal_row():
    c = TestClient(app)
    cols = get_feature_names()
    payload = {"features": {cname: 0.0 for cname in cols}}
    r = c.post("/api/v1/predict", json=payload)
    assert r.status_code == 200
    data = r.json()
    assert "yhat" in data and isinstance(data["yhat"], list)
    assert len(data["yhat"]) == 1
