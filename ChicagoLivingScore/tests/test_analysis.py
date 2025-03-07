import pytest
from pathlib import Path
from analysis.economic_infrastructure_analysis import main

data = Path(__file__).parent.parent / "data/raw_data/raw_data_eco_infra.csv"
df_eco = main(data)

def test_normalize_max(df_eco):
    assert df_eco["unemployed"].max() <= 1, "Test failed: normalized value greater than 1 found!"
    
def test_chicago_zip():
    assert len(df_eco["zipcode"]) <= 60, "Test failed: you have more than actual zipcodes in Chicago"
