# LAB3: California Housing Price Regression API

## Overview

This project provides a FastAPI-based REST API for predicting California housing prices using a regression model. It features robust input/output schema validation, unit testing, and exposes endpoints for single and batch predictions. The model is trained using the California Housing dataset and a RandomForestRegressor.

## Features

- **Regression Model:** Predicts median house value using key features.
- **API Endpoints:** Health check, model info, single and batch prediction.
- **Input/Output Validation:** Strict schema validation with Pydantic.
- **Unit Testing:** Automated tests for endpoints and validation.
- **Directory Structure Explained:** See below.

## API Endpoints

- `GET /health`  
	Returns API and model status.

- `GET /model/info`  
	Returns model metadata (features, metrics, training info).

- `POST /predict`  
	Predicts house value for a single input.  
	**Input:** JSON with required features.  
	**Output:** `{ "prediction": float }`

- `POST /predict/batch`  
	Predicts house values for a batch of inputs.  
	**Input:** `{ "items": [ ... ] }`  
	**Output:** `{ "predictions": [float, ...] }`

## Input/Output Schema Validation

- All endpoints use Pydantic models for strict validation.
- Extra fields are rejected; missing/invalid fields return errors.

## Unit Testing

- Tests cover health, prediction, and validation logic.
- See `tests/unit_test.py` for details.

## Directory Structure

```
LAB3/
│
├── assets/                # (Optional) Static files, images, etc.
├── model/
│   ├── house_model.pkl    # Trained regression model
│   └── metadata.json      # Model metadata (features, metrics, etc.)
├── requirements.txt       # Python dependencies
├── src/
│   ├── app.py             # FastAPI app, endpoints, schema validation
│   └── train.py           # Model training script
├── tests/
│   └── unit_test.py       # Unit tests for API and validation
├── .gitignore             # Git ignore rules
├── README.md              # Project documentation (this file)
└── venv/                  # Python virtual environment (not tracked)
```

## Getting Started

1. Install dependencies:  
	 `pip install -r requirements.txt`
2. Train the model:  
	 `python src/train.py`
3. Run the API:  
	 `uvicorn src.app:app --reload`
4. Run tests:  
	 `pytest tests/unit_test.py`

---

