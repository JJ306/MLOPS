import logging
import time
from contextlib import asynccontextmanager
from datetime import datetime
from pathlib import Path
from typing import List

import joblib
import numpy as np
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Global variables for model
model = None
scaler = None

SEQ_LENGTH = 24
N_SENSORS = 6
N_FEATURES = SEQ_LENGTH * N_SENSORS  # 144


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Load model on startup (matches train.py behavior)."""
    global model, scaler

    model_path = Path("models/final_model.pkl")
    scaler_path = Path("models/scaler.pkl")

    if not model_path.exists() or not scaler_path.exists():
        logger.warning("⚠️ Model or scaler not found! Run: python src/model/train.py")
    else:
        model = joblib.load(model_path)
        scaler = joblib.load(scaler_path)
        logger.info("✅ Model and scaler loaded")
        # model.n_features_in_ should be 144
        logger.info(
            f"   Model expects {getattr(model, 'n_features_in_', 'unknown')} features"
        )

    yield  # nothing to clean up on shutdown


app = FastAPI(
    title="Predictive Maintenance API",
    description="MLOps project for predictive maintenance using 24-step time series.",
    version="1.0.0",
    lifespan=lifespan,
)


class SensorData(BaseModel):
    temperature: float
    pressure: float
    vibration: float
    rpm: float
    torque: float
    fuel_flow: float

    class Config:
        json_schema_extra = {
            "example": {
                "temperature": 55.0,
                "pressure": 105.0,
                "vibration": 5.0,
                "rpm": 3150.0,
                "torque": 53.0,
                "fuel_flow": 215.0,
            }
        }


class TimeSeriesData(BaseModel):
    # Exactly 24 timesteps, each with 6 features
    data: List[SensorData]

    class Config:
        json_schema_extra = {
            "example": {
                "data": [
                    # 24 points – shortened here; docs will show full example
                    {
                        "temperature": 50,
                        "pressure": 100,
                        "vibration": 5,
                        "rpm": 3000,
                        "torque": 50,
                        "fuel_flow": 200,
                    },
                    {
                        "temperature": 51,
                        "pressure": 101,
                        "vibration": 5.2,
                        "rpm": 3010,
                        "torque": 51,
                        "fuel_flow": 201,
                    },
                    # ...
                    {
                        "temperature": 56,
                        "pressure": 106,
                        "vibration": 5.2,
                        "rpm": 3170,
                        "torque": 53.5,
                        "fuel_flow": 217,
                    },
                    {
                        "temperature": 56.5,
                        "pressure": 106.5,
                        "vibration": 5.3,
                        "rpm": 3180,
                        "torque": 53.7,
                        "fuel_flow": 218,
                    },
                ]
            }
        }


class PredictionResponse(BaseModel):
    prediction: int
    probability: float
    timestamp: str
    message: str
    model_version: str = "1.0.0"
    seq_length: int = SEQ_LENGTH


@app.get("/")
def read_root():
    return {
        "status": "🚀 Predictive Maintenance API is running",
        "version": "1.0.0",
        "docs": "/docs",
        "note": f"Model expects {SEQ_LENGTH} timestamps × {N_SENSORS} sensors = {N_FEATURES} features",
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "model_loaded": model is not None,
        "expected_features": N_FEATURES if model is not None else None,
        "seq_length": SEQ_LENGTH,
        "n_sensors": N_SENSORS,
    }


@app.post("/predict", response_model=PredictionResponse)
def predict_failure(payload: TimeSeriesData):
    """
    Predict failure using time series sensor data.

    You MUST send exactly 24 consecutive readings (seq_length)
    with 6 features each.
    """
    start = time.time()
    try:
        if model is None or scaler is None:
            raise HTTPException(
                status_code=500,
                detail="Model/scaler not loaded. Run training: python src/model/train.py",
            )

        # Validate length
        sensor_data = payload.data
        if len(sensor_data) != SEQ_LENGTH:
            raise HTTPException(
                status_code=400,
                detail=f"Must provide exactly {SEQ_LENGTH} timesteps; got {len(sensor_data)}",
            )

        # Build (24, 6) array
        X = np.array(
            [
                [
                    d.temperature,
                    d.pressure,
                    d.vibration,
                    d.rpm,
                    d.torque,
                    d.fuel_flow,
                ]
                for d in sensor_data
            ]
        )  # shape: (24, 6)

        # Scale each row like in train.py
        # train.py did: X_flat = X.reshape(-1, 6); scaler.fit_transform(X_flat); X_scaled.reshape(...)
        # At inference: we mimic that: flatten to (24, 6), scale, then reshape back (24, 6)
        X_flat = X.reshape(-1, X.shape[-1])  # (24, 6)
        X_scaled_flat = scaler.transform(X_flat)  # (24, 6)
        X_scaled = X_scaled_flat.reshape(X.shape)  # (24, 6) again

        # Now flatten to 2D for RandomForest, like in evaluate_model()
        X_for_model = X_scaled.reshape(1, -1)  # (1, 144)

        if X_for_model.shape[1] != getattr(
            model, "n_features_in_", X_for_model.shape[1]
        ):
            raise HTTPException(
                status_code=500,
                detail=f"Feature mismatch: model expects {getattr(model, 'n_features_in_', 'unknown')} "
                f"features, but got {X_for_model.shape[1]}",
            )

        # Predict
        pred = model.predict(X_for_model)[0]
        proba = model.predict_proba(X_for_model)[0][1]

        logger.info(
            "prediction=%s proba=%.3f latency_ms=%.1f",
            int(pred),
            float(proba),
            (time.time() - start) * 1000,
        )

        return PredictionResponse(
            prediction=int(pred),
            probability=float(proba),
            timestamp=datetime.now().isoformat(),
            message="⚠️ Failure predicted!" if pred == 1 else "✅ Normal operation",
            model_version="1.0.0",
            seq_length=SEQ_LENGTH,
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Prediction error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn

    print(f"""
╔═══════════════════════════════════════════════════════════╗
║   🚀 Predictive Maintenance API                          ║
║                                                           ║
║   IMPORTANT:                                              ║
║   - Send 24 timesteps (seq_length={SEQ_LENGTH})           ║
║   - Each timestep: 6 features (temp, pressure, ...)       ║
║                                                           ║
║   Docs:   http://localhost:8000/docs                      ║
║   Health: http://localhost:8000/health                    ║
║   Predict: POST /predict                                  ║
╚═══════════════════════════════════════════════════════════╝
""")

    uvicorn.run(app, host="0.0.0.0", port=8000)
