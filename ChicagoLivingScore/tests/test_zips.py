import pytest
from pathlib import Path
import joblib
import geopandas as gpd
from analysis.zips import load_shapefile_with_cache  

def test_load_shapefile_with_cache(tmp_path):
    """Test that load_shapefile_with_cache correctly loads and caches shapefiles."""
    BASE_DIR = Path(__file__).parent.parent
    DATA_FILE = BASE_DIR / "data" / "raw_data" /"Zips"/  "tl_2020_us_zcta520.shp"
    # Ensure the file exists before reading
    cache_path = tmp_path / "cached_shapefile.pkl"
    shp_path = Path(DATA_FILE)
    
    # Ensure the function runs without errors and returns a GeoDataFrame
    gdf = load_shapefile_with_cache(shp_path, cache_path)
    assert isinstance(gdf, gpd.GeoDataFrame), "Returned object is not a GeoDataFrame"

    assert gdf.crs is not None, "CRS is not set in the loaded GeoDataFrame"
    assert cache_path.exists(), "Cache file was not created"
    # Load from cache and verify it's the same
    gdf_cached = joblib.load(cache_path)
    assert gdf.equals(gdf_cached), "Cached GeoDataFrame does not match the original"
if __name__ == "__main__":
    pytest.main()

