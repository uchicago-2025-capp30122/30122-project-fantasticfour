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

