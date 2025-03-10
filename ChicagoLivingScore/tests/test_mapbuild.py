import pytest
import pandas as pd
import geopandas as gpd
import lxml.html
import folium
from pathlib import Path
from map.mapbuild import *


@pytest.fixture
def sample_dataframe():
    # Load local metrics data
    BASE_DIR = pathlib.Path(__file__).parent.parent  
    DATA_FILE = BASE_DIR / "data" / "cleaned_data" / "final_living_score.csv"
    df_metrics = pd.read_csv(DATA_FILE, nrows=3)
    return df_metrics

def test_get_chicago_zip_geo():
    assert not get_chicago_zip_geo().empty
    assert "geometry" in get_chicago_zip_geo().columns
    assert "zip" in get_chicago_zip_geo().columns

def test_create_map():
    assert isinstance(create_map(), folium.Map)

def test_map_show_avg_price(sample_dataframe):
    assert "avg_price_per_sqft" in sample_dataframe.columns
    assert isinstance(map_show_avg_price(create_map(),sample_dataframe), folium.Map)

def test_show_unemployed_score(sample_dataframe):
    assert "unemployed_score" in sample_dataframe.columns
    assert isinstance(show_unemployed_score(create_map(),sample_dataframe), folium.Map)

