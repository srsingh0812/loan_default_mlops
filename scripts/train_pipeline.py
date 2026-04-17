"""
End-to-end training pipeline for loan default prediction.
"""

import sys
import os
import logging
import traceback

# make src importable
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../src"))

from data.ingest import load_data, validate_data, clean_and_cast, split_data
from features.feature_eng import (
    engineer_features,
    build_preprocessor,
    prepare_xy,
    save_preprocessor
)
from models.train import (
    train_model,
    evaluate_model,
    log_experiment,
    save_model,
    get_data_hash
)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)
logger = logging.getLogger(__name__)


def main():
    logger.info("=== PIPELINE START ===")

    try:
        # -------------------------
        # Step 1: Load + Validate
        # -------------------------
        df = load_data("data/raw/Dataset.csv")
        validate_data(df)
        logger.info("Step 1: Data loaded and validated")

        # -------------------------
        # Step 2: Clean
        # -------------------------
        df = clean_and_cast(df)
        df = df.drop(columns=["ID"], errors="ignore")
        logger.info("Step 2: Data cleaned")

        # -------------------------
        # Step 3: Feature Engineering
        # -------------------------
        df = engineer_features(df)
        logger.info("Step 3: Features created")

        # -------------------------
        # Step 4: Split
        # -------------------------
        data_hash = get_data_hash(df)
        train_df, test_df = split_data(df)

        X_train, y_train = prepare_xy(train_df)
        X_test, y_test = prepare_xy(test_df)

        logger.info("Step 4: Train-test split complete")

        # -------------------------
        # Step 5: Preprocessing
        # -------------------------
        preprocessor = build_preprocessor(X_train)
        preprocessor.fit(X_train)

        logger.info("Step 5: Preprocessor fitted")

        # -------------------------
        # Step 6: Training
        # -------------------------
        # 🔥 FIXED: match actual function signature
        model = train_model(X_train, y_train, preprocessor)

        logger.info("Step 6: Model trained")

        # -------------------------
        # Step 7: Evaluation
        # -------------------------
        metrics = evaluate_model(model, X_test, y_test)

        logger.info(f"AUC: {metrics['auc']}")
        logger.info(f"F1: {metrics['f1']}")
        logger.info(f"Recall: {metrics['recall']}")

        # -------------------------
        # Step 8: Save Artifacts
        # -------------------------
        save_model(model)
        save_preprocessor(preprocessor)

        logger.info("Step 8: Artifacts saved")

        # -------------------------
        # Step 9: Log Experiment
        # -------------------------
        log_experiment(metrics, data_hash)

        logger.info("Step 9: Experiment logged")

    except Exception as e:
        logger.error("Pipeline failed ❌")
        logger.error(traceback.format_exc())
        raise e

    logger.info("=== PIPELINE END ===")


if __name__ == "__main__":
    main()