"""
Train and evaluate loan default model.
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


# --- fix imports ---
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

from src.features.feature_eng import (
    engineer_features, prepare_xy, load_preprocessor
)


# --- logging ---
logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger(__name__)


# --- model ---
MODEL = GradientBoostingClassifier(
    n_estimators=200,
    max_depth=5,
    learning_rate=0.05,
    subsample=0.8,
    random_state=42
)


def get_data_hash(df):
    return hashlib.md5(
        pd.util.hash_pandas_object(df).values
    ).hexdigest()[:8]


def train_model(X_train, y_train, preprocessor):
    logger.info("Training Gradient Boosting with SMOTE...")

    pipeline = ImbPipeline([
        ("preprocessor", preprocessor),
        ("smote", SMOTE(random_state=42)),
        ("model", MODEL),
    ])

    start = time.time()
    pipeline.fit(X_train, y_train)
    logger.info(f"Training completed in {time.time() - start:.1f}s")

    return pipeline


def evaluate_model(pipeline, X_test, y_test):

    y_proba = pipeline.predict_proba(X_test)[:, 1]

    threshold = 0.3
    y_pred = (y_proba > threshold).astype(int)

    auc = roc_auc_score(y_test, y_proba)
    f1 = f1_score(y_test, y_pred)
    recall = recall_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred)

    logger.info(f"AUC: {auc:.4f}")
    logger.info(f"F1: {f1:.4f}")
    logger.info(f"Recall: {recall:.4f}")
    logger.info(f"Precision: {precision:.4f}")
    logger.info(f"Confusion Matrix:\n{confusion_matrix(y_test, y_pred)}")

    logger.info("\nThreshold tuning:")
    for t in [0.1, 0.2, 0.3, 0.4, 0.5]:
        preds = (y_proba > t).astype(int)
        logger.info(
            f"t={t} → Recall: {recall_score(y_test, preds):.3f}, "
            f"F1: {f1_score(y_test, preds):.3f}"
        )

    return {
        "auc": auc,
        "f1": f1,
        "recall": recall,
        "precision": precision
    }


def save_model(pipeline):
    Path("models").mkdir(exist_ok=True)
    joblib.dump(pipeline, "models/model.pkl")
    logger.info("Model saved → models/model.pkl")


def log_experiment(metrics, data_hash):
    Path("experiments").mkdir(exist_ok=True)

    run_id = f"run_{int(time.time())}"

    with open(f"experiments/{run_id}.json", "w") as f:
        json.dump({
            "metrics": metrics,
            "data_hash": data_hash
        }, f, indent=2)

    logger.info(f"Experiment logged → {run_id}.json")


# --- main ---
if __name__ == "__main__":

    logger.info("=== TRAINING START ===")

    train_df = pd.read_csv("data/processed/train.csv", low_memory=False)
    test_df = pd.read_csv("data/processed/test.csv", low_memory=False)

    train_df = engineer_features(train_df)
    test_df = engineer_features(test_df)

    X_train, y_train = prepare_xy(train_df)
    X_test, y_test = prepare_xy(test_df)

    preprocessor = load_preprocessor()

    model = train_model(X_train, y_train, preprocessor)

    metrics = evaluate_model(model, X_test, y_test)

    save_model(model)
    log_experiment(metrics, get_data_hash(train_df))

    logger.info("=== TRAINING END ===")