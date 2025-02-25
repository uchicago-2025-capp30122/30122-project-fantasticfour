import geopandas as gpd
import pathlib
from shapely.geometry import Point

BASE_DIR = pathlib.Path(__file__).parent.parent
INPUT_FILE = BASE_DIR / "data" / "raw_data" / "education.csv"
OUTPUT_FILE = BASE_DIR / "data" / "cleaned_data"/"cleaned_education.csv"

original_df = gpd.read_file(INPUT_FILE)
#original_df["geometry"] = original_df.apply(lambda row: Point(row['School_Longitude'], row['School_Latitude']), axis=1)
gdf_edu = gpd.GeoDataFrame(original_df[['School_ID', 'Short_Name', 'Long_Name', 'School_Type','School_Latitude','School_Longitude','Website',"Creative_School_Certification"]]) # use variables we need
gdf_edu.to_csv(OUTPUT_FILE, index=False, encoding="utf-8")