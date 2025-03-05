import pathlib
import geopandas as gpd
import joblib

def load_shapefile_with_cache(shp_path: pathlib.Path, cache_path: pathlib.Path = pathlib.Path("cached_shapefile.pkl")) -> gpd.GeoDataFrame:

    try:
        gdf = joblib.load(cache_path)
    except FileNotFoundError:
        gdf = gpd.read_file(shp_path)
        if gdf.crs is None:
            gdf = gdf.set_crs("EPSG:4326", allow_override=True)
        joblib.dump(gdf, cache_path)
    return gdf
if __name__ == "__main__":
    shp_file = pathlib.Path("./data/raw_data/Zips/tl_2020_us_zcta520.shp")
    gdf_shapefile = load_shapefile_with_cache(shp_file)
