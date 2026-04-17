"""
Drift Detection Module
Compares training vs production data using PSI.
"""

import pandas as pd
import numpy as np
from pathlib import Path


# -----------------------------
# PSI Calculation
# -----------------------------
def calculate_psi(expected, actual, bins=10):
    """
    Calculate Population Stability Index (PSI)
    """

    expected = expected.dropna()
    actual = actual.dropna()

    # Handle empty columns
    if len(expected) == 0 or len(actual) == 0:
        return 0.0

    # Create bins using training distribution
    percentiles = np.linspace(0, 100, bins + 1)
    breakpoints = np.percentile(expected, percentiles)
    breakpoints = np.unique(breakpoints)

    # If constant column
    if len(breakpoints) < 2:
        return 0.0

    # Histogram counts
    expected_counts = np.histogram(expected, bins=breakpoints)[0]
    actual_counts = np.histogram(actual, bins=breakpoints)[0]

    # Convert to proportions
    expected_perc = expected_counts / len(expected)
    actual_perc = actual_counts / len(actual)

    # Avoid divide-by-zero
    epsilon = 1e-6
    expected_perc = np.where(expected_perc == 0, epsilon, expected_perc)
    actual_perc = np.where(actual_perc == 0, epsilon, actual_perc)

    # PSI formula
    psi = np.sum((actual_perc - expected_perc) * np.log(actual_perc / expected_perc))

    return psi


# -----------------------------
# Drift Check
# -----------------------------
def check_drift(train_df, prod_df):

    numeric_cols = train_df.select_dtypes(include=np.number).columns
    report = {}

    print(f"\n🔍 Checking {len(numeric_cols)} numeric features...\n")

    if len(numeric_cols) == 0:
        print("❌ No numeric columns found — check data types!")
        return {}

    for col in numeric_cols:

        if col not in prod_df.columns:
            print(f"⚠️ {col} missing in production — skipping")
            continue

        psi = calculate_psi(train_df[col], prod_df[col])

        # Classification
        if psi < 0.1:
            status = "OK"
        elif psi < 0.25:
            status = "WARNING"
        else:
            status = "CRITICAL"

        print(f"{col:30s} | PSI: {psi:.4f} | {status}")

        if status == "CRITICAL":
            print(f"🚨 CRITICAL DRIFT detected in {col}")

        report[col] = {
            "psi": round(psi, 4),
            "status": status
        }

    return report


# -----------------------------
# MAIN
# -----------------------------
if __name__ == "__main__":

    print("\n🚀 Starting Drift Detection...\n")

    train_path = Path("data/processed/train.csv")
    prod_path = Path("data/processed/test.csv")

    # Check files exist
    if not train_path.exists() or not prod_path.exists():
        print("❌ Train/Test files not found. Run ingestion first.")
        exit(1)

    # Load data
    train_df = pd.read_csv(train_path, low_memory=False)
    prod_df = pd.read_csv(prod_path, low_memory=False)

    print(f"Train shape: {train_df.shape}")
    print(f"Prod shape : {prod_df.shape}")

    # Ensure numeric types
    train_df = train_df.apply(lambda x: pd.to_numeric(x, errors="ignore"))
    prod_df = prod_df.apply(lambda x: pd.to_numeric(x, errors="ignore"))

    # Run drift detection
    report = check_drift(train_df, prod_df)

    print(f"\n✅ Drift check completed for {len(report)} features\n")