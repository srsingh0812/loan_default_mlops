"""
Feature engineering and preprocessing for loan default model.

- Creates useful derived features
- Builds preprocessing pipelines
- Prepares data for model training
"""

import pandas as pd
import numpy as np
import joblib
from pathlib import Path
import logging

from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.impute import SimpleImputer

logger = logging.getLogger(__name__)

TARGET_COL = "Default"


# feature groups (kept explicit for stability)
NUMERIC_FEATURES = [
    "Client_Income", "Credit_Amount", "Loan_Annuity", "Age_Days",
    "Employed_Days", "Registration_Days", "ID_Days", "Own_House_Age",
    "Child_Count", "Client_Family_Members", "Cleint_City_Rating",
    "Score_Source_1", "Score_Source_2", "Social_Circle_Default",
    "Phone_Change", "Credit_Bureau", "Population_Region_Relative",
    "Application_Process_Hour"
]

CATEGORICAL_FEATURES = [
    "Accompany_Client", "Client_Income_Type", "Client_Education",
    "Client_Marital_Status", "Client_Gender", "Loan_Contract_Type",
    "Client_Housing_Type", "Client_Occupation", "Type_Organization"
]

BINARY_FEATURES = [
    "Car_Owned", "Bike_Owned", "Active_Loan", "House_Own",
    "Mobile_Tag", "Homephone_Tag", "Workphone_Working",
    "Client_Permanent_Match_Tag", "Client_Contact_Work_Tag"
]


def engineer_features(df: pd.DataFrame) -> pd.DataFrame:
    """Create a few domain-driven features."""
    df = df.copy()

    # ratios help capture financial stress / repayment ability
    df["income_annuity_ratio"] = (
        df["Client_Income"].fillna(1) /
        df["Loan_Annuity"].replace(0, 1).fillna(1)
    )

    df["credit_income_ratio"] = (
        df["Credit_Amount"].fillna(0) /
        df["Client_Income"].replace(0, 1).fillna(1)
    )

    # convert days → years for better interpretability
    df["age_years"] = df["Age_Days"].abs() / 365
    df["employment_years"] = df["Employed_Days"].abs() / 365

    return df


def build_preprocessor(X: pd.DataFrame) -> ColumnTransformer:
    """Create preprocessing pipelines for different feature types."""

    num_cols = [c for c in NUMERIC_FEATURES if c in X.columns]
    cat_cols = [c for c in CATEGORICAL_FEATURES if c in X.columns]
    bin_cols = [c for c in BINARY_FEATURES if c in X.columns]

    logger.info(f"Numerical features: {num_cols}")
    logger.info(f"Categorical features: {cat_cols}")
    logger.info(f"Binary features: {bin_cols}")

    # numeric → fill missing + scale
    num_pipeline = Pipeline([
        ("imputer", SimpleImputer(strategy="median")),
        ("scaler", StandardScaler())
    ])

    # categorical → fill + one-hot encode
    cat_pipeline = Pipeline([
        ("imputer", SimpleImputer(strategy="constant", fill_value="Unknown")),
        ("encoder", OneHotEncoder(handle_unknown="ignore"))
    ])

    # binary → fill + encode (drop one level)
    bin_pipeline = Pipeline([
        ("imputer", SimpleImputer(strategy="most_frequent")),
        ("encoder", OneHotEncoder(drop="if_binary", handle_unknown="ignore"))
    ])

    return ColumnTransformer(
        transformers=[
            ("num", num_pipeline, num_cols),
            ("cat", cat_pipeline, cat_cols),
            ("bin", bin_pipeline, bin_cols),
        ],
        remainder="drop",
        sparse_threshold=0
    )


def prepare_xy(df: pd.DataFrame):
    """Split into features and target."""
    X = df.drop(columns=[TARGET_COL], errors="ignore")
    y = df[TARGET_COL] if TARGET_COL in df.columns else None
    return X, y


def save_preprocessor(preprocessor, path="models/preprocessor.pkl"):
    """Save fitted preprocessor."""
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(preprocessor, path)
    logger.info(f"Preprocessor saved to {path}")


def load_preprocessor(path="models/preprocessor.pkl"):
    """Load saved preprocessor."""
    return joblib.load(path)


# quick test runner (for validation)
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    logger.info("Starting feature engineering test...")

    df = pd.read_csv("data/processed/train.csv")
    logger.info(f"Input shape: {df.shape}")

    df = engineer_features(df)
    logger.info(f"After feature engineering: {df.shape}")

    X, y = prepare_xy(df)
    logger.info(f"X shape: {X.shape}, y shape: {y.shape}")

    preprocessor = build_preprocessor(X)

    X_transformed = preprocessor.fit_transform(X)
    logger.info(f"Transformed shape: {X_transformed.shape}")

    if np.isnan(X_transformed).sum() > 0:
        raise ValueError("NaNs found after preprocessing")

    logger.info("No NaNs found ✓")

    save_preprocessor(preprocessor)

    logger.info("Feature engineering pipeline completed successfully")
