# src/train.py
import json
from datetime import datetime
from pathlib import Path

import joblib
import numpy as np
from sklearn.datasets import fetch_california_housing
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import train_test_split

MODEL_DIR = Path(__file__).resolve().parents[1] / "model"
MODEL_PATH = MODEL_DIR / "house_model.pkl"
META_PATH = MODEL_DIR / "metadata.json"

FEATURES = [
    "MedInc", "HouseAge", "AveRooms", "AveBedrms",
    "Population", "AveOccup", "Latitude", "Longitude"
]

def main():
    MODEL_DIR.mkdir(parents=True, exist_ok=True)

    data = fetch_california_housing(as_frame=True)
    df = data.frame

    X = df[FEATURES]
    y = df["MedHouseVal"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    model = RandomForestRegressor(
        n_estimators=250,
        random_state=42,
        n_jobs=-1
    )
    model.fit(X_train, y_train)

    preds = model.predict(X_test)
    rmse = float(np.sqrt(mean_squared_error(y_test, preds)))
    r2 = float(r2_score(y_test, preds))

    joblib.dump(model, MODEL_PATH)

    meta = {
        "problem_type": "regression",
        "dataset": "sklearn.datasets.fetch_california_housing",
        "model": "RandomForestRegressor",
        "features": FEATURES,
        "metrics": {"rmse": rmse, "r2": r2},
        "trained_at_utc": datetime.utcnow().isoformat() + "Z",
    }
    META_PATH.write_text(json.dumps(meta, indent=2))

    print(f"Saved model to: {MODEL_PATH}")
    print(f"Saved metadata to: {META_PATH}")
    print(f"RMSE={rmse:.4f} | R2={r2:.4f}")

if __name__ == "__main__":
    main()