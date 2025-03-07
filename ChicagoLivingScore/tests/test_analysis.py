import pytest
import pandas as pd
import pathlib
from analysis.economic_infrastructure_analysis import main

@pytest.fixture
def df_eco():
    data_path = pathlib.Path("./data/cleaned_data/cleaned_data_economic_infrastructure.csv")
    
    # Ensure the file exists before reading
    assert data_path.exists(), f"test failed: data not found!"
    
    return pd.read_csv(data_path)

def test_normalize_max(df_eco):
    assert df_eco["unemployed"].max() <= 1, "test failed: normalized value greater than 1 found!"

def test_chicago_zip(df_eco):
    assert len(df_eco["zipcode"].unique()) <= 60, "test failed: you have more zipcodes than actual ones in Chicago!"
