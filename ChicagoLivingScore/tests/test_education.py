import pytest
import pandas as pd
from pathlib import Path
import numpy as np
from analysis.education_data_analysis import load_data, standardize_column 

def test_load_data(tmp_path):
    """Test that load_data correctly loads and cleans a CSV file."""
    csv_content = """ZIP,SAT_SCORE
    60601,1200
    60602,1100
    """
    BASE_DIR = Path(__file__).parent.parent
    csv_path = BASE_DIR / "data" / "raw_data" / "test_data.csv"
    csv_path = tmp_path / "test_data.csv"
    csv_path.write_text(csv_content)
    
    df = load_data(csv_path)
    
    assert "zip_code" in df.columns, "Column 'zip_code' not created"
    assert df["zip_code"].dtype == object, "'zip_code' column is not a string"
    assert df.columns.tolist() == ["zip", "sat_score", "zip_code"], "Unexpected column names"

def test_standardize_column():
    """Test that standardize_column correctly scales values between 0 and 1."""
    series = pd.Series([10, 20, 30, 40, 50])
    standardized = standardize_column(series)
    
    assert standardized.min() == 0, "Minimum value is not 0"
    assert standardized.max() == 1, "Maximum value is not 1"
    assert np.all((standardized >= 0) & (standardized <= 1)), "Values are not within [0,1] range"
    single_value_series = pd.Series([10, 10, 10])
    standardized_single = standardize_column(single_value_series)
    assert all(standardized_single == 1), "Standardization failed when all values are equal"

if __name__ == "__main__":
    pytest.main()