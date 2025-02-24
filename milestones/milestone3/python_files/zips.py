
import pathlib
import shapefile
import geopandas as gpd
import csv
import joblib
import pandas as pd
"""shapefile_path = pathlib.Path("path/to/shapefile.shp")
tracts = load_shapefiles(shapefile_path)"""

def load_shapefile_with_cache(shp_path: pathlib.Path, cache_path: pathlib.Path = pathlib.Path("cached_shapefile.pkl")) -> gpd.GeoDataFrame:
    """
    Carga un shapefile y lo guarda en caché para un acceso más rápido en el futuro.
    
    Parámetros:
        shp_path: Ruta al archivo .shp.
        cache_path: Ruta al archivo de caché (por defecto 'cached_shapefile.pkl').
    
    Retorna:
        Un GeoDataFrame con los datos del shapefile.
    """
    try:
        gdf = joblib.load(cache_path)
    except FileNotFoundError:
        gdf = gpd.read_file(shp_path)
        if gdf.crs is None:
            gdf = gdf.set_crs("EPSG:4326", allow_override=True)
        joblib.dump(gdf, cache_path)
    return gdf
shp_file = pathlib.Path("C:/Users/aleja/Downloads/tl_2020_us_zcta520/tl_2020_us_zcta520.shp")
gdf_shapefile = load_shapefile_with_cache(shp_file)
print(gdf_shapefile.head())
