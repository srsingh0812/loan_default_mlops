"""
ROBUST TRAINING PIPELINE

Features:
- Reproducible training
- SMOTE + preprocessing pipeline
- Threshold-aware evaluation
- Model versioning (stable + canary)
- Experiment logging
- Safe file handling
"""

import sys
import os
import time
import json
import hashlib
import logging
from pathlib import Path

import pandas as pd
import joblib

from sklearn.metrics import (
    roc_auc_score, f1_score, precision_score,
    recall_score, confusion_matrix
)
from sklearn.ensemble import GradientBoostingClassifier
from imblearn.pipeline import Pipeline as ImbPipeline
from imblearn.over_sampling import SMOTE

# ─── Fix imports ─────────────────────────────────────────────────────────────
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

from src.features.feature_eng import (
    engineer_features, prepare_xy, load_preprocessor
)

# ─── Logging ────────────────────────────────────────────────────────────────
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s")
logger = logging.getLogger(__name__)

# ─── Constants ──────────────────────────────────────────────────────────────
MODEL_DIR = Path("models")
EXP_DIR = Path("experiments")
DATA_DIR = Path("data/processed")

MODEL_DIR.mkdir(exist_ok=True)
EXP_DIR.mkdir(exist_ok=True)

THRESHOLD = 0.3
BASELINE_F1 = 0.65  # used for canary decision


# ─── Model Definition ───────────────────────────────────────────────────────
def build_model():
    return GradientBoostingClassifier(
        n_estimators=200,
        max_depth=5,
        learning_rate=0.05,
        subsample=0.8,
        random_state=42
    )


# ─── Utilities ──────────────────────────────────────────────────────────────
def get_data_hash(df: pd.DataFrame) -> str:
    return hashlib.md5(
        pd.util.hash_pandas_object(df).values
    ).hexdigest()[:8]


# ─── Training ───────────────────────────────────────────────────────────────
def train_model(X_train, y_train, preprocessor):

    logger.info("Training model with SMOTE pipeline...")

    pipeline = ImbPipeline([
        ("preprocessor", preprocessor),
        ("smote", SMOTE(random_state=42)),
        ("model", build_model()),
    ])

    start = time.time()
    pipeline.fit(X_train, y_train)

    logger.info(f"Training completed in {time.time() - start:.1f}s")
    return pipeline


# ─── Evaluation ─────────────────────────────────────────────────────────────
def evaluate_model(pipeline, X_test, y_test):

    y_proba = pipeline.predict_proba(X_test)[:, 1]
    y_pred = (y_proba > THRESHOLD).astype(int)

    metrics = {
        "auc": roc_auc_score(y_test, y_proba),
        "f1": f1_score(y_test, y_pred),
        "recall": recall_score(y_test, y_pred),
        "precision": precision_score(y_test, y_pred)
    }

    logger.info("=== Evaluation Metrics ===")
    for k, v in metrics.items():
        logger.info(f"{k.upper()}: {v:.4f}")

    logger.info(f"\nConfusion Matrix:\n{confusion_matrix(y_test, y_pred)}")

    # Threshold scan
    logger.info("\nThreshold tuning:")
    for t in [0.1, 0.2, 0.3, 0.4, 0.5]:
        preds = (y_proba > t).astype(int)
        logger.info(
            f"t={t} → Recall: {recall_score(y_test, preds):.3f}, "
            f"F1: {f1_score(y_test, preds):.3f}"
        )

    return metrics


# ─── Model Saving ───────────────────────────────────────────────────────────
def save_model(pipeline, metrics):

    stable_path = MODEL_DIR / "model.pkl"
    canary_path = MODEL_DIR / "model_canary.pkl"

    # Save new model as canary first
    joblib.dump(pipeline, canary_path)
    logger.info(f"Canary model saved → {canary_path}")

    # Promote to stable if good enough
    if metrics["f1"] >= BASELINE_F1:
        joblib.dump(pipeline, stable_path)
        logger.info(f"Model promoted to production → {stable_path}")
    else:
        logger.warning("Model NOT promoted (below baseline)")


# ─── Experiment Logging ─────────────────────────────────────────────────────
def log_experiment(metrics, data_hash):

    run_id = f"run_{int(time.time())}"

    payload = {
        "run_id": run_id,
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "metrics": metrics,
        "data_hash": data_hash
    }

    with open(EXP_DIR / f"{run_id}.json", "w") as f:
        json.dump(payload, f, indent=2)

    logger.info(f"Experiment logged → {run_id}.json")


# ─── Main Pipeline ──────────────────────────────────────────────────────────
def main():

    logger.info("=== TRAINING START ===")

    try:
        train_df = pd.read_csv(DATA_DIR / "train.csv", low_memory=False)
        test_df = pd.read_csv(DATA_DIR / "test.csv", low_memory=False)

        logger.info("Data loaded successfully")

    except Exception as e:
        logger.error(f"Failed to load data: {e}")
        return

    # Feature engineering
    train_df = engineer_features(train_df)
    test_df = engineer_features(test_df)

    # Prepare data
    X_train, y_train = prepare_xy(train_df)
    X_test, y_test = prepare_xy(test_df)

    preprocessor = load_preprocessor()

    # Train
    model = train_model(X_train, y_train, preprocessor)

    # Evaluate
    metrics = evaluate_model(model, X_test, y_test)

    # Save + promote
    save_model(model, metrics)

    # Log experiment
    log_experiment(metrics, get_data_hash(train_df))

    logger.info("=== TRAINING END ===")


# ─── Entry Point ────────────────────────────────────────────────────────────
if __name__ == "__main__":
    main()