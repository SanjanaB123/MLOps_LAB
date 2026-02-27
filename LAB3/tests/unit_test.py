from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_health_endpoint():
    r = client.get("/health")
    assert r.status_code == 200
    assert "model_loaded" in r.json()

def test_predict_validation_fails_missing_fields():
    r = client.post("/predict", json={"MedInc": 2.0})
    assert r.status_code == 422

def test_predict_rejects_extra_fields():
    payload = {
        "MedInc": 2.0, "HouseAge": 20, "AveRooms": 5, "AveBedrms": 1,
        "Population": 1000, "AveOccup": 3, "Latitude": 34, "Longitude": -118,
        "ExtraKey": 123
    }
    r = client.post("/predict", json=payload)
    assert r.status_code == 422