
from typing import NamedTuple
from shapely.geometry import Point, Polygon, shape
from shapely import wkt
import pandas as pd
import pathlib
import geopandas as gpd
import csv
import json

class Tract:
    def __init__(self, id, polygon):
        self.id = id
        self.polygon = polygon
        
    def __repr__(self):
        return f"Tract(id={self.id}, polygon={self.polygon})"

def load_geojson(path: pathlib.Path) -> list:
    tracts = []
    with open(path, "r") as f:
        data = json.load(f)
        for feature in data["features"]:
            if feature["properties"].get("ZCTA5CE20") is not None:
                geom = shape(feature["geometry"])
                tracts.append(
                    Tract(
                        id=feature["properties"]["ZCTA5CE20"],
                        polygon=geom
                    )
                )
    return tracts

def load_frs_csv():
    """
    Given a CSV containing facility data, return a list of points objects.
    """
    count=0
    facilities = []
    file_path = pathlib.Path("C:/Users/aleja/Downloads/crimes.csv")
    with file_path.open(mode="r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            lat=row["Latitude"].strip()
            lon=row["Longitude"].strip()
            if count<=3:
                print(type(row["Longitude"]),row["Longitude"])
            count+=1
            if lat != "" and lon !="":
                if row["Arrest"].lower()=="true":
                    if row["Domestic"].lower()=="false":
                        point=Point(lon,lat)
                        facilities.append(point)
    return facilities

def find_zip_codes(gdf_zip, points):
    processed_points = []
    for p in points:
        if isinstance(p, str):
            geom = wkt.loads(p)
            processed_points.append((geom.y, geom.x))  # (lat, lon)
        elif isinstance(p, (tuple, list)) and len(p) == 2:
            processed_points.append(p)
        elif isinstance(p, Point):
            processed_points.append((p.y, p.x))
    df_points = pd.DataFrame(processed_points, columns=['lat', 'lon'])
    df_points['geometry'] = df_points.apply(lambda row: Point(row['lon'], row['lat']), axis=1)
    gdf_points = gpd.GeoDataFrame(df_points, geometry='geometry', crs="EPSG:4326")
    gdf_joined = gpd.sjoin(gdf_points, gdf_zip, how='left', predicate='within')
    df_result=gdf_joined[['lat', 'lon', 'ZCTA5CE20']]
    df_result.to_csv("crimes_zip.csv", index=False)
    return gdf_joined[['lat', 'lon', 'ZCTA5CE20']]
shp_path = pathlib.Path("C:/Users/aleja/Downloads/tl_2020_us_zcta520/tl_2020_us_zcta520.shp")

def info():
    df = pd.read_csv("C:/Users/aleja/pa-5-Alejandroinfo/crimes_zip.csv")
    conteo_por_zip = df.groupby("ZCTA5CE20").size().reset_index(name="count")
    conteo_por_zip.to_csv("resultados_por_zip.csv", index=False)
    return 