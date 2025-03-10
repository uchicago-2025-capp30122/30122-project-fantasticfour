import pytest
import pandas as pd
import numpy as np
from pathlib import Path
from shapely.geometry import Point
from analysis.zips import load_shapefile_with_cache
from analysis.environment_data_analysis import load_frs_csv, find_zip_codes

def test_load_frs_csv(tmp_path):
    """Test that load_frs_csv correctly loads crime locations as Point objects."""
    csv_content = """LATITUDE,LONGITUDE
    41.8781,-87.6298
    41.881832,-87.623177
    41.9000,-87.7000"""
    csv_path = tmp_path / "environment.csv"
    csv_path.write_text(csv_content)
    
    points = load_frs_csv(csv_path)
    
    assert isinstance(points, list), "Returned object is not a list"
    assert len(points) == 3, "Incorrect number of points loaded"
    assert all(isinstance(p, Point) for p in points), "Not all elements are Point objects"

def test_find_zip_codes(tmp_path):
    """Test that find_zip_codes assigns correct zip codes to points."""
    points = [Point(-87.6298, 41.8781), Point(-87.623177, 41.881832)]
    
    BASE_DIR = Path(__file__).parent.parent
    shp_file = BASE_DIR / "data" / "raw_data" / "Zips" / "tl_2020_us_zcta520.shp"
    
    gdf_zip = load_shapefile_with_cache(shp_file)
    
    result = find_zip_codes(gdf_zip, points)
    
    assert "ZCTA5CE20" in result.columns, "Zip code column missing"
    assert len(result) == len(points), "Mismatch in number of points processed"
    assert not result["ZCTA5CE20"].isnull().all(), "All zip codes are missing"

if __name__ == "__main__":
    pytest.main()
