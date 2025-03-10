from shapely.geometry import Point
from shapely import wkt
from analysis.zips import load_shapefile_with_cache
import pandas as pd
import pathlib
import geopandas as gpd
import csv

def load_frs_csv(file_path):
    """
    Given a CSV containing crimes locations, return a list of points objects.
    """
    crime_points = []
    with file_path.open(mode="r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            lat=row["Latitude"].strip()
            lon=row["Longitude"].strip()
            if lat != "" and lon !="":
                if row["Arrest"].lower()=="true":
                    if row["Domestic"].lower()=="false":
                        point=Point(lon,lat)
                        crime_points.append(point)
    return crime_points

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
    df_result.to_csv("./data/raw_data/crimes_zip.csv", index=False)
    return gdf_joined[['lat', 'lon', 'ZCTA5CE20']]

def info():
    BASE_DIR = pathlib.Path(__file__).parent.parent
    shp_file = BASE_DIR / "data" / "raw_data" /"Zips"/  "tl_2020_us_zcta520.shp"
    file_path = BASE_DIR / "data" / "raw_data" / "crimes.csv"
    zips=load_shapefile_with_cache(shp_file)
    find_zip_codes(zips,load_frs_csv(file_path))
    df = pd.read_csv("./data/raw_data/crimes_zip.csv")
    zip_codes_df = pd.read_csv("./data/cleaned_data/chicago_zip.csv")
    zip_column = "ZCTA5CE20"
    zip_codes_list = zip_codes_df["zip_code"].astype(str).tolist()
    df_filtered = df[df[zip_column].astype(str).isin(zip_codes_list)]

    total_per_zip = df_filtered.groupby(zip_column).size().reset_index(name="count")
    total_per_zip.to_csv("./data/cleaned_data/cleaned_data_crime.csv", index=False)
    return 
if __name__ == '__main__':
    info()