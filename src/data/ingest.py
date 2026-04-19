"""
Data ingestion pipeline for loan default prediction.
Handles loading, validation, cleaning, and train-test split.
"""

import pandas as pd
import numpy as np
from pathlib import Path
from typing import Tuple
import logging

# -----------------------------
# Logging
# -----------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)
logger = logging.getLogger(__name__)

# -----------------------------
# Constants
# -----------------------------
TARGET_COL = "Default"
DROP_COLS = ["ID"]

NUMERIC_COLS = [
    "Client_Income", "Credit_Amount", "Loan_Annuity",
    "Age_Days", "Employed_Days", "Registration_Days", "ID_Days"
]


# -----------------------------
# Load Data
# -----------------------------
def load_data(filepath: str) -> pd.DataFrame:
    """Load raw dataset and normalize missing values."""
    logger.info(f"Loading data from {filepath}")

    df = pd.read_csv(filepath, low_memory=False)

    # Normalize missing placeholders
    df.replace(['@', '#', 'NA', 'N/A', 'null', 'NULL', '', ' '],
               np.nan, inplace=True)

    logger.info(f"Dataset loaded: {df.shape[0]} rows, {df.shape[1]} columns")
    return df


# -----------------------------
# Validate Data (FIXED)
# -----------------------------
def validate_data(df: pd.DataFrame) -> bool:
    """Basic sanity checks on dataset (test-compatible)."""

    # Target must exist
    assert TARGET_COL in df.columns, f"Missing target column: {TARGET_COL}"

    # Data should not be empty
    assert not df.empty, "Dataset is empty"

    # Check high missing columns
    missing_pct = df.isnull().mean()
    high_missing = missing_pct[missing_pct > 0.9].index.tolist()

    assert len(
        high_missing) == 0, f"Columns with >90% missing values: {high_missing}"

    logger.info("Data validation passed ✓")

    return True


# -----------------------------
# Clean + Cast
# -----------------------------
def clean_and_cast(df: pd.DataFrame) -> pd.DataFrame:
    """Clean numeric columns and fix known data issues."""
    df = df.copy()

    for col in NUMERIC_COLS:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    # Domain fixes
    if "Age_Days" in df.columns:
        df["Age_Days"] = df["Age_Days"].abs()

    if "Employed_Days" in df.columns:
        df["Employed_Days"] = df["Employed_Days"].replace(365243, np.nan)

    return df


# -----------------------------
# Split Data
# -----------------------------
def split_data(
    df: pd.DataFrame,
    test_size: float = 0.2,
    random_state: int = 42
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """Split dataset into train and test using stratification."""

    from sklearn.model_selection import train_test_split

    train, test = train_test_split(
        df,
        test_size=test_size,
        random_state=random_state,
        stratify=df[TARGET_COL]
    )

    # Distribution logs
    logger.info("Target distribution (full dataset):")
    logger.info(df[TARGET_COL].value_counts(normalize=True))

    logger.info("Target distribution (train):")
    logger.info(train[TARGET_COL].value_counts(normalize=True))

    logger.info("Target distribution (test):")
    logger.info(test[TARGET_COL].value_counts(normalize=True))

    # Stratification sanity check
    if abs(train[TARGET_COL].mean() - test[TARGET_COL].mean()) > 0.01:
        raise ValueError("Stratification failed")

    logger.info(f"Split complete — train: {len(train)}, test: {len(test)}")

    return train, test


# -----------------------------
# Full Pipeline
# -----------------------------
def run_ingestion(raw_path: str, output_dir: str = "data/processed") -> None:
    """Run full ingestion pipeline."""

    logger.info("=== DATA INGESTION START ===")

    Path(output_dir).mkdir(parents=True, exist_ok=True)

    df = load_data(raw_path)
    validate_data(df)

    df = clean_and_cast(df)

    logger.info("Top missing columns after cleaning:")
    logger.info(df.isnull().mean().sort_values(ascending=False).head(10))

    # Drop unnecessary columns
    df = df.drop(columns=[c for c in DROP_COLS if c in df.columns])

    train, test = split_data(df)

    train.to_csv(f"{output_dir}/train.csv", index=False)
    test.to_csv(f"{output_dir}/test.csv", index=False)

    logger.info(f"Saved processed data to {output_dir}")
    logger.info("=== DATA INGESTION END ===")


# -----------------------------
# MAIN
# -----------------------------
if __name__ == "__main__":
    run_ingestion("data/raw/Dataset.csv")
