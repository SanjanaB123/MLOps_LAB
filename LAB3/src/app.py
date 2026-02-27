# src/app.py
import json
import logging
from pathlib import Path
from typing import List, Optional

import joblib
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, ConfigDict, confloat

logger = logging.getLogger("house_api")
logging.basicConfig(level=logging.INFO)

BASE_DIR = Path(__file__).resolve().parents[1]
MODEL_PATH = BASE_DIR / "model" / "house_model.pkl"
META_PATH = BASE_DIR / "model" / "metadata.json"

app = FastAPI(title="California Housing Price Regression API")

_model = None
_meta: Optional[dict] = None

# ---- Schemas ----
class HousingFeatures(BaseModel):
    model_config = ConfigDict(extra="forbid")

    MedInc: float = Field(..., ge=0)
    HouseAge: float = Field(..., ge=0)
    AveRooms: float = Field(..., ge=0)
    AveBedrms: float = Field(..., ge=0)
    Population: float = Field(..., ge=0)
    AveOccup: float = Field(..., ge=0)
    Latitude: float = Field(..., ge=32, le=42)
    Longitude: float = Field(..., ge=-125, le=-113)

class PredictResponse(BaseModel):
    prediction: float

class BatchPredictRequest(BaseModel):
    items: List[HousingFeatures]

class BatchPredictResponse(BaseModel):
    predictions: List[float]

# ---- Helpers ----
def _load():
    global _model, _meta
    if not MODEL_PATH.exists():
        raise FileNotFoundError(f"Model not found at {MODEL_PATH}. Run: python train.py")
    _model = joblib.load(MODEL_PATH)
    _meta = json.loads(META_PATH.read_text()) if META_PATH.exists() else None

@app.on_event("startup")
def startup_event():
    try:
        _load()
        logger.info("Model loaded successfully.")
    except Exception as e:
        logger.exception("Failed to load model on startup: %s", e)

def _ensure_model():
    if _model is None:
        raise HTTPException(status_code=503, detail="Model not loaded. Train first and restart the API.")

# ---- Endpoints ----
@app.get("/health")
def health():
    return {
        "status": "ok" if _model is not None else "degraded",
        "model_loaded": _model is not None
    }

@app.get("/model/info")
def model_info():
    _ensure_model()
    return _meta or {"warning": "metadata.json not found. Retrain to generate it."}

@app.post("/predict", response_model=PredictResponse)
def predict(x: HousingFeatures):
    _ensure_model()
    features = [[
        x.MedInc, x.HouseAge, x.AveRooms, x.AveBedrms,
        x.Population, x.AveOccup, x.Latitude, x.Longitude
    ]]
    pred = float(_model.predict(features)[0])
    return PredictResponse(prediction=pred)

@app.post("/predict/batch", response_model=BatchPredictResponse)
def predict_batch(req: BatchPredictRequest):
    _ensure_model()
    if len(req.items) == 0:
        raise HTTPException(status_code=400, detail="items must be a non-empty list")

    features = [[
        it.MedInc, it.HouseAge, it.AveRooms, it.AveBedrms,
        it.Population, it.AveOccup, it.Latitude, it.Longitude
    ] for it in req.items]

    preds = _model.predict(features)
    return BatchPredictResponse(predictions=[float(p) for p in preds])