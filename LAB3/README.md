## Note on Model Size and GitHub

Since this project uses a regression model (RandomForestRegressor), the trained model file (`house_model.pkl`) is very large. The file size is 345.29 MB, which exceeds GitHub's file size limit of 100 MB. The error:

```
remote: error: File LAB3/model/house_model.pkl is 345.29 MB; this exceeds GitHub's file size limit of 100.00 MB
remote: error: GH001: Large files detected. You may want to try Git Large File Storage - https://git-lfs.github.com.
error: failed to push some refs to 'https://github.com/SanjanaB123/MLOps_LAB.git'
```

**Proof:**

```
Writing objects: 100% (22/22), 74.90 MiB | 7.77 MiB/s, done.
remote: error: File LAB3/model/house_model.pkl is 345.29 MB; this exceeds GitHub's file size limit of 100.00 MB
```

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

