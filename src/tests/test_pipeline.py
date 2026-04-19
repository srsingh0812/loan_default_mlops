"""
UNIT TESTS
Run with: pytest src/tests/ -v
"""

import sys
import os

# Fix path FIRST
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, ROOT_DIR)

import pytest
import pandas as pd
import numpy as np

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


def test_validate_data_passes(sample_df):
    assert validate_data(sample_df) is True


def test_clean_and_cast(sample_df):
    df = clean_and_cast(sample_df)
    assert "Client_Income" in df.columns


def test_feature_engineering(sample_df):
    df = clean_and_cast(sample_df)
    df = engineer_features(df)
    assert "income_annuity_ratio" in df.columns


def test_psi():
    a = np.random.normal(0, 1, 1000)
    b = np.random.normal(1, 1, 1000)
    psi = calculate_psi(a, b)
    assert isinstance(psi, float)