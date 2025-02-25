
from typing import NamedTuple
from shapely.geometry import Point, shape
from shapely import wkt
import pandas as pd
import pathlib
import geopandas as gpd
import csv
import json

class Facility(NamedTuple):
    id: int
    arrest: bool
    domestic:bool
    latitude: float
    longitude: float


def load_frs_csv():
    """
    Given a CSV containing enviromental incidents
    locations , return a list of points objects.
    """
    environmental_incidents = []
    file_path = pathlib.Path("C:/Users/aleja/Downloads/environment.csv")
    with file_path.open(mode="r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            lat=row["LATITUDE"].strip()
            lon=row["LONGITUDE"].strip()
            if lat != "" and lon !="":
                        point=Point(lon,lat)
                        environmental_incidents.append(point)
    return environmental_incidents

def find_zip_codes(gdf_zip, points):
    processed_points = []
    for p in points:
        if isinstance(p, str):
            geom = wkt.loads(p)
            processed_points.append((geom.y, geom.x))
        elif isinstance(p, (tuple, list)) and len(p) == 2:
            processed_points.append(p)
        elif isinstance(p, Point):
            processed_points.append((p.y, p.x))
        else:
            print("Bad format")
    df_points = pd.DataFrame(processed_points, columns=['lat', 'lon'])
    df_points['geometry'] = df_points.apply(lambda row: Point(row['lon'], row['lat']), axis=1)
    
    gdf_points = gpd.GeoDataFrame(df_points, geometry='geometry', crs="EPSG:4326")
    gdf_joined = gpd.sjoin(gdf_points, gdf_zip, how='left', predicate='within')
    df_result=gdf_joined[['lat', 'lon', 'ZCTA5CE20']]
    df_result.to_csv("environment_zips.csv", index=False)
    return gdf_joined[['lat', 'lon', 'ZCTA5CE20']]
shp_path = pathlib.Path("C:/Users/aleja/Downloads/tl_2020_us_zcta520/tl_2020_us_zcta520.shp")

def info():
    df = pd.read_csv("C:/Users/aleja/environment_zips.csv")
    conteo_por_zip = df.groupby("ZCTA5CE20").size().reset_index(name="count")
    conteo_por_zip.to_csv("environmental_results.csv", index=False)
    return 