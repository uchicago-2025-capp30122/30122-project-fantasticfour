import pytest
import pathlib
from analysis.economic_infrastructure_analysis import main

@pytest.fixture
def df_eco():
    data = pathlib.Path("./data/cleaned_data/cleaned_data_economic_infrastructure.csv")
    return data

def test_normalize_max(df_eco):
    assert df_eco["unemployed"].max() <= 1, "Test failed: normalized value greater than 1 found!"

def test_chicago_zip(df_eco):
    assert len(df_eco["zipcode"]) <= 60, "Test failed: you have more than actual zipcodes in Chicago"
