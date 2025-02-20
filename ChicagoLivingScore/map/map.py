import folium
from shapely.wkt import loads
import geopandas as gpd
import pandas as pd
import httpx
from shapely import wkt
import lxml.html

def cssscraper(key):
    rows = root.cssselect(key)
    rv_lst = []
    for row in rows:
        rv_lst.append(row.text)
    return rv_lst

url = "https://data.cityofchicago.org/api/views/unjd-c2ca/rows.xml?accessType=DOWNLOAD"
resp = httpx.get(url)
html_text = resp.text
root = lxml.html.fromstring(html_text)

polygon_lst = cssscraper("the_geom")
zip_lst = cssscraper("zip")
objectid_lst = cssscraper("objectid") # variables that we need for basic map
dataframe_lst = []
for i in range(1, len(polygon_lst)):
    row = [polygon_lst[i], zip_lst[i], objectid_lst[i]]
    dataframe_lst.append(row)

df = pd.DataFrame(dataframe_lst,columns=['geometry','zip','objectid']) # transformed to a df
df['geometry'] = wkt.loads(df['geometry']) # generate multipolygons
gdf = gpd.GeoDataFrame(df, geometry = "geometry")

m = folium.Map(location=(41.8781, -87.6298), zoom_start=11)
for _, r in gdf.iterrows():
    sim_geo = gpd.GeoSeries(r["geometry"]).simplify(tolerance=0.00001)
    geo_j = sim_geo.to_json()
    geo_j = folium.GeoJson(data=geo_j, style_function=lambda x: {"fillColor": "orange"})
    folium.Popup(r["zip"]).add_to(geo_j)
    geo_j.add_to(m)
    
m # present map