"""
UNIT TESTS
Run with: pytest src/tests/ -v
"""

import pytest
import pandas as pd
import numpy as np
import sys
import os

# Fix path
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, ROOT_DIR)

from data.ingest import clean_and_cast, validate_data
from features.feature_eng import engineer_features
from monitoring.drift import calculate_psi


@pytest.fixture
def sample_df():
    return pd.DataFrame({
        "ID": [1, 2, 3, 4, 5],
        "Client_Income": ["100000", "200000", None, "150000", "80000"],
        "Credit_Amount": ["500000", "800000", "300000", None, "200000"],
        "Loan_Annuity": ["25000", "40000", "15000", "20000", "10000"],
        "Age_Days": ["14600", "18000", "12000", "20000", "16000"],
        "Employed_Days": ["-1000", "-500", "365243", "-800", None],
        "Default": [0, 1, 0, 1, 0],
    })


class TestDataIngestion:

    def test_validate_data_passes(self, sample_df):
        assert validate_data(sample_df) is True

    def test_validate_data_fails_no_target(self):
        df = pd.DataFrame({"a": [1, 2, 3]})
        with pytest.raises(AssertionError):
            validate_data(df)

    def test_clean_and_cast_converts_numeric(self, sample_df):
        cleaned = clean_and_cast(sample_df)
        assert pd.api.types.is_float_dtype(cleaned["Client_Income"])

    def test_clean_and_cast_handles_employed_days(self, sample_df):
        cleaned = clean_and_cast(sample_df)
        assert cleaned["Employed_Days"].isna().sum() > 0

    def test_clean_and_cast_age_positive(self, sample_df):
        cleaned = clean_and_cast(sample_df)
        assert (cleaned["Age_Days"].dropna() >= 0).all()


class TestFeatureEngineering:

    def test_income_annuity_ratio_created(self, sample_df):
        cleaned = clean_and_cast(sample_df)
        featured = engineer_features(cleaned)
        assert "income_annuity_ratio" in featured.columns

    def test_credit_income_ratio_no_division_error(self, sample_df):
        cleaned = clean_and_cast(sample_df)
        featured = engineer_features(cleaned)
        assert not featured["credit_income_ratio"].isin([np.inf, -np.inf]).any()

    def test_age_years_in_range(self, sample_df):
        cleaned = clean_and_cast(sample_df)
        featured = engineer_features(cleaned)
        valid_ages = featured["age_years"].dropna()
        assert (valid_ages >= 0).all()
        assert (valid_ages < 100).all()


class TestDriftDetection:

    def test_psi_same_distribution_near_zero(self):
        arr = np.random.normal(0, 1, 1000)
        psi = calculate_psi(arr, arr + np.random.normal(0, 0.01, 1000))
        assert psi < 0.10

    def test_psi_different_distribution_high(self):
        ref = np.random.normal(0, 1, 1000)
        prod = np.random.normal(5, 1, 1000)
        psi = calculate_psi(ref, prod)
        assert psi > 0.25

    def test_psi_returns_float(self):
        a = np.random.uniform(0, 1, 500)
        b = np.random.uniform(0, 1, 500)
        result = calculate_psi(a, b)
        assert isinstance(result, float)