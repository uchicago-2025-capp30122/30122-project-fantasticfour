import folium
from shapely.wkt import loads
import geopandas as gpd
import pandas as pd
import httpx
from shapely import wkt
import lxml.html
import pathlib
from shapely.geometry import Point


BASE_DIR = pathlib.Path(__file__).parent

def cssscraper(root, key):
    rows = root.cssselect(key)
    return [row.text for row in rows]

def get_chicago_zip_geo():
    # Download Chicago zipcode data as XML
    url = "https://data.cityofchicago.org/api/views/unjd-c2ca/rows.xml?accessType=DOWNLOAD"
    resp = httpx.get(url)
    html_text = resp.text
    root = lxml.html.fromstring(html_text)
    
    polygon_lst = cssscraper(root, "the_geom")
    zip_lst = cssscraper(root, "zip")
    objectid_lst = cssscraper(root, "objectid")
    
    data = []
    for i in range(0, len(polygon_lst)):
        data.append([polygon_lst[i], zip_lst[i], objectid_lst[i]])
    df = pd.DataFrame(data, columns=['geometry','zip','objectid'])
    df['geometry'] = df['geometry'].apply(wkt.loads)
    gdf = gpd.GeoDataFrame(df, geometry='geometry')
    return gdf


def create_map(selected_zip=None):
    """
    Generate a Folium map centered on Chicago. If 'selected_zip' is provided,
    that region will be highlighted with a darker color.
    """
    m = folium.Map(location=[41.8781, -87.6298], zoom_start=11, tiles='cartodbpositron')
    gdf = get_chicago_zip_geo()
    
    for _, row in gdf.iterrows():
        # If this zipcode is selected, use dark color fill; otherwise use light blue fill.
        if selected_zip and row['zip'] == selected_zip:
            fill_color = "#2196F3"  
        else:
            fill_color = "#BBDEFB"
        sim_geo = gdf.loc[[_]]["geometry"].simplify(tolerance=0.00001)
        geo_json = sim_geo.to_json()

        geo = folium.GeoJson(
            data=geo_json,
            style_function=lambda feature, fill_color=fill_color: {
                'fillColor': fill_color,
                'color': "#0D47A1",  
                'weight': 2,
                'fillOpacity': 0.6,
            }
        )
        folium.Popup(row["zip"]).add_to(geo)
        geo.add_to(m)
    return m

def map_add_schools(m, selected_zip=None):
    DATA_FILE = BASE_DIR / ".." / "data" / "cleaned_data"/"cleaned_education.csv"

    original_df = gpd.read_file(DATA_FILE)
    original_df["geometry"] = original_df.apply(lambda row: Point(row['School_Longitude'], row['School_Latitude']), axis=1)
    gdf_edu = gpd.GeoDataFrame(original_df) # use variables we need
    
    # If we have a selected_zip, do a spatial filter
    if selected_zip is not None:
        gdf_zip = get_chicago_zip_geo()
        polygon = gdf_zip.loc[gdf_zip['zip'] == selected_zip, 'geometry']
        if not polygon.empty:
            polygon_geom = polygon.iloc[0]  
            gdf_edu = gdf_edu[gdf_edu.within(polygon_geom)]

    gdf_edu['Link'] = '<a href="' + gdf_edu.Website + '">' + gdf_edu.Website + "</a>"

    school_type = gdf_edu["School_Type"].unique()
    big_schools = ("Neighborhood","Charter","Citywide-Option")
    radius_index = {school:80 if school in big_schools else 60 for school in school_type} # generally bigger school has bigger radius

    school_rate = list(gdf_edu['Creative_School_Certification'].unique())
    colors = ['green','blue','yellow','grey','brown','white']
    color_index = {rate: colors[i] if i < len(colors) else "blue" for i, rate in enumerate(school_rate)}
    # better schools will have blue and green, worse schools will have yellowand brown,
    # no data or incomplete will have white or grey

    gdf_edu.set_crs(epsg=4326, inplace=True) # set the geo information


    folium.GeoJson( # add markers on the map
        gdf_edu,
        name="schools",
        marker=folium.Circle(radius=4, fill_color="orange", fill_opacity=0.4, color="black", weight=1),
        tooltip=folium.GeoJsonTooltip(fields=['School_ID', 'Long_Name',"School_Type"]), # show these labels
        popup=folium.GeoJsonPopup(fields=['School_ID', 'Long_Name', "Link"]), # show these labels when click on
        style_function=lambda x: {
            "fillColor": color_index.get(x['properties']['Creative_School_Certification'],2),
            "radius":  radius_index.get(x['properties']['School_Type']), # set fillcolor and radius based on certification and school type
        },
        highlight_function=lambda x: {"fillOpacity": 0.8},
        zoom_on_click=True,
    ).add_to(m)

    return m