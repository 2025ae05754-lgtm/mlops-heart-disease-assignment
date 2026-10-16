import os
import joblib
import pandas as pd
import logging
from fastapi import FastAPI, HTTPException
from app.schemas import CardiacDataPayload, CardiacPredictionResponse
from prometheus_fastapi_instrumentator import Instrumentator

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger("api_server")

app = FastAPI(
    title="Cardiac Risk Assessment API",
    description="Production MLOps Service for UCI Heart Disease Classification",
    version="1.0.0"
)

# Instrument Prometheus Metrics
Instrumentator().instrument(app).expose(app)

MODEL_PATH = os.path.join("models", "cardiac_risk_pipeline.joblib")
model_pipeline = None

@app.on_event("startup")
def initialize_model():
    global model_pipeline
    if os.path.exists(MODEL_PATH):
        model_pipeline = joblib.load(MODEL_PATH)
        logger.info("Successfully loaded ML pipeline artifact.")
    else:
        logger.error(f"Critical error: Model binary missing at {MODEL_PATH}")

@app.get("/health", tags=["System Health"])
def health_check():
    if model_pipeline is None:
        raise HTTPException(status_code=503, detail="Model pipeline uninitialized.")
    return {"status": "healthy", "model_loaded": True}

@app.post("/predict", response_model=CardiacPredictionResponse, tags=["Inference"])
def predict_cardiac_risk(payload: CardiacDataPayload):
    if model_pipeline is None:
        raise HTTPException(status_code=503, detail="Model pipeline is unavailable.")

    try:
        data_dict = payload.dict()
        df = pd.DataFrame([data_dict])
        
        pred = int(model_pipeline.predict(df)[0])
        confidence = float(model_pipeline.predict_proba(df)[0][pred])

        risk_label = "High Risk (Presence)" if pred == 1 else "Low Risk (Absence)"
        logger.info(f"Inference Requested | Risk: {risk_label} | Confidence: {confidence:.4f}")

        return CardiacPredictionResponse(
            prediction=pred,
            heart_disease_risk=risk_label,
            confidence=round(confidence, 4)
        )
    except Exception as e:
        logger.error(f"Inference failure: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Inference execution failed: {str(e)}")