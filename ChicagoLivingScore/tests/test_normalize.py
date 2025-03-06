import pandas as pd
import pytest
from pathlib import Path
from analysis.all_data_normalize import DataNormalizer
from analysis.final_score_analysis import FinalScoreCalculator



def test_min_max_normalize():
    series = pd.Series([0, 50, 100])
    calc = DataNormalizer()  
    norm = calc.min_max_normalize(series)
    expected = pd.Series([0.0, 0.5, 1.0])
    pd.testing.assert_series_equal(norm, expected)




def test_min_max_normalize_invert():
    series = pd.Series([0, 50, 100])
    calc = DataNormalizer()  
    norm_inv = calc.min_max_normalize(series, invert=True)
    expected_inv = pd.Series([1.0, 0.5, 0.0])
    pd.testing.assert_series_equal(norm_inv, expected_inv)




@pytest.fixture
def temp_env_file(tmp_path):
    data = {
        "count": [100, 200, 300],
        "zipcode": ["60601", "60602", "60603"]
    }
    df = pd.DataFrame(data)
    file_path = tmp_path / "cleaned_data_environment.csv"
    df.to_csv(file_path, index=False)
    return file_path

def test_process_environment(temp_env_file):
    normalizer = DataNormalizer()
    normalizer.env_file = temp_env_file
    df_env = normalizer.process_environment()
    
    assert "environment_score" in df_env.columns
    assert df_env["environment_score"].min() >= 0
    assert df_env["environment_score"].max() <= 1



@pytest.fixture
def temp_crime_file(tmp_path):
    data = {
        "count": [50, 150, 250],
        "zipcode": ["60601", "60602", "60603"]
    }
    df = pd.DataFrame(data)
    file_path = tmp_path / "cleaned_data_crime.csv"
    df.to_csv(file_path, index=False)
    return file_path

def test_process_crime(temp_crime_file):
    normalizer = DataNormalizer()
    normalizer.crime_file = temp_crime_file
    df_crime = normalizer.process_crime()






def test_normalize_zip():
    calculator = FinalScoreCalculator()
    assert calculator.normalize_zip(60614) == "60614"
    assert calculator.normalize_zip("60614") == "60614"
    assert calculator.normalize_zip("60614.0") == "60614"





def test_impute_by_nearest():
    data = {
        "zipcode": ["60601", "60602", "60603", "60604"],
        "avg_price_per_sqft": [200, None, 400, 500]
    }
    df = pd.DataFrame(data)
    calc = FinalScoreCalculator()
    df_imputed = calc.impute_by_nearest(df, "avg_price_per_sqft")
    
    assert df_imputed["avg_price_per_sqft"].isnull().sum() == 0, "missing values"

