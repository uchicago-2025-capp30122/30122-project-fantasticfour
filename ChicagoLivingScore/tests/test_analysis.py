import pytest
import pandas as pd
from pathlib import Path
#from analysis.economic_infrastructure_analysis import main

@pytest.fixture
def df_eco():
    file_path = Path("data/cleaned_data/cleaned_data_economic_infrastructure.csv")
    # chek if data loads correctly
    assert file_path.exists(), f"test failed: data not found"
    return pd.read_csv(file_path)

def test_normalize_max(df_eco):
    assert df_eco["unemployed"].max() <= 1, "test failed: normalized value can't be greater than 1"

def test_chicago_zip(df_eco):
    assert len(df_eco["zipcode"].unique()) <= 60, "test failed: more zipcodes than actual ones in Chicago"
