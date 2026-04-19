"""
FastAPI app for loan default prediction (correct inference pipeline).
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, validator
from typing import Optional
import joblib
import pandas as pd
import time
import os
import logging

# 🔥 IMPORT YOUR TRAINING LOGIC (IMPORTANT)
from src.features.feature_eng import engineer_features

# -------------------- logging --------------------
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s")
logger = logging.getLogger(__name__)

# -------------------- config --------------------
MODEL_PATH = os.getenv("MODEL_PATH", "models/model.pkl")

# -------------------- app --------------------
app = FastAPI(
    title="Loan Default Prediction API",
    version="1.0.0"
)

model = None


# -------------------- startup --------------------
@app.on_event("startup")
def load_model():
    global model
    try:
        model = joblib.load(MODEL_PATH)
        logger.info(f"✅ Model loaded from {MODEL_PATH}")
    except Exception as e:
        logger.error(f"❌ Model loading failed: {e}")


# -------------------- schemas --------------------
class LoanApplication(BaseModel):
    Client_Income: float = Field(..., gt=0)
    Credit_Amount: float = Field(..., gt=0)
    Loan_Annuity: float = Field(..., gt=0)
    Age_Days: float
    Employed_Days: Optional[float] = 0

    # Optional categorical + binary defaults
    Client_Gender: Optional[str] = "M"
    Client_Education: Optional[str] = "Secondary"
    Client_Marital_Status: Optional[str] = "Married"
    Loan_Contract_Type: Optional[str] = "Cash loans"

    Car_Owned: Optional[int] = 0
    Bike_Owned: Optional[int] = 0
    House_Own: Optional[int] = 0

    @validator("Age_Days")
    def validate_age(cls, v):
        if abs(v) < 365 * 18:
            raise ValueError("Must be at least 18 years old")
        return abs(v)


class PredictionResponse(BaseModel):
    probability: float
    risk_label: str
    decision: str
    latency_ms: float


# -------------------- helper --------------------
def prepare_full_input(df: pd.DataFrame) -> pd.DataFrame:
    """
    Ensures input matches training schema before inference.
    """

    # 🔥 Apply same feature engineering
    df = engineer_features(df)

    # 🔥 Fill missing columns with safe defaults
    expected_cols = model.named_steps["preprocessor"].feature_names_in_

    for col in expected_cols:
        if col not in df.columns:
            df[col] = 0

    return df[expected_cols]


# -------------------- routes --------------------
@app.get("/")
def root():
    return {"message": "Loan Default API is running"}


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/ready")
def ready():
    if model is None:
        raise HTTPException(status_code=503, detail="Model not loaded")
    return {"status": "ready"}


@app.post("/predict", response_model=PredictionResponse)
def predict(application: LoanApplication):

    if model is None:
        raise HTTPException(status_code=503, detail="Model not loaded")

    start = time.time()

    # convert input → dataframe
    input_df = pd.DataFrame([application.dict()])

    try:
        # 🔥 FIXED PIPELINE
        input_df = prepare_full_input(input_df)

        proba = float(model.predict_proba(input_df)[0][1])

    except Exception as e:
        logger.error(f"❌ Prediction failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

    # business logic
    if proba < 0.3:
        risk, decision = "LOW", "APPROVE"
    elif proba < 0.6:
        risk, decision = "MEDIUM", "REVIEW"
    else:
        risk, decision = "HIGH", "DECLINE"

    latency = round((time.time() - start) * 1000, 2)

    logger.info(f"{proba:.3f} → {decision} ({latency}ms)")

    return {
        "probability": round(proba, 4),
        "risk_label": risk,
        "decision": decision,
        "latency_ms": latency
    }


@app.get("/metrics")
def metrics():
    return {"requests_total": 0}
