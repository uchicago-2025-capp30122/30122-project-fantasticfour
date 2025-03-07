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
    root = lxml.html.fromstring(html_text) # to get the root from the html
    
    polygon_lst = cssscraper(root, "the_geom")
    zip_lst = cssscraper(root, "zip")
    objectid_lst = cssscraper(root, "objectid") # get several components that we need
    
    data = []
    for i in range(0, len(polygon_lst)):
        data.append([polygon_lst[i], zip_lst[i], objectid_lst[i]])
    df = pd.DataFrame(data, columns=['geometry','zip','objectid'])
    df['geometry'] = df['geometry'].apply(wkt.loads) 
    # to load the multipolygon as geo information form
    
    def unify_zip(z):
        try:
            return str(int(float(z)))
        except:
            return None
    
    df['zip'] = df['zip'].apply(unify_zip)
    
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
        folium.Popup(row["zip"]).add_to(geo) # to add the mark that has zip number 
        geo.add_to(m)
    return m

def map_show_avg_price(m,df_metrics): # df_metrics is the final_score_analysis that we already read in app.py
    
    df_use = df_metrics[["zipcode","avg_price_per_sqft"]]
    df_use["zipcode"] = df_use["zipcode"].astype(str)
    gdf_json = get_chicago_zip_geo().to_json()

    folium.Choropleth(
        geo_data=gdf_json,
        data=df_use,
        columns=["zipcode","avg_price_per_sqft"],
        key_on="feature.properties.zip",
        fill_color="YlGn",
        bins=[100,200,300,400,500],
        name="average house price",
        highlight=True,
        legend_name="Average price per square feet",
        
    ).add_to(m)
    
    return m

def show_unemployed_score(m,df_metrics): # df_metrics is the final_score_analysis that we already read in app.py
    
    df_use = df_metrics[["zipcode","unemployed_score"]]
    df_use["zipcode"] = df_use["zipcode"].astype(str)
    gdf_json = get_chicago_zip_geo().to_json()

    folium.Choropleth(
        geo_data=gdf_json,
        data=df_use,
        columns=["zipcode","unemployed_score"],
        key_on="feature.properties.zip",
        fill_color="YlGn",
        bins=[0,0.2,0.4,0.6,0.8,1.0],
        name="employment rate",
        highlight=True,
        legend_name="employment rate",
        
    ).add_to(m)
    
    return m


def show_trafic_score(m,df_metrics): # df_metrics is the final_score_analysis that we already read in app.py
    
    df_use = df_metrics[["zipcode","commute_time_score"]]
    df_use["zipcode"] = df_use["zipcode"].astype(str)
    gdf_json = get_chicago_zip_geo().to_json()

    folium.Choropleth(
        geo_data=gdf_json,
        data=df_use,
        columns=["zipcode","commute_time_score"],
        key_on="feature.properties.zip",
        fill_color="YlGn",
        bins=[0,0.2,0.4,0.6,0.8,1.0],
        name="commute time score",
        highlight=True,
        legend_name="commute time score",
        
    ).add_to(m)
    
    return m


def show_education_score(m,df_metrics): # df_metrics is the final_score_analysis that we already read in app.py
    
    df_use = df_metrics[["zipcode","education_score"]]
    df_use["zipcode"] = df_use["zipcode"].astype(str)
    gdf_json = get_chicago_zip_geo().to_json()

    folium.Choropleth(
        geo_data=gdf_json,
        data=df_use,
        columns=["zipcode","education_score"],
        key_on="feature.properties.zip",
        fill_color="YlGn",
        bins=[0,0.2,0.4,0.6,0.8,1.0],
        name="education score",
        highlight=True,
        legend_name="education score",
        
    ).add_to(m)
    
    return m


def show_crime_score(m,df_metrics): # df_metrics is the final_score_analysis that we already read in app.py
    
    df_use = df_metrics[["zipcode","crime_score"]]
    df_use["zipcode"] = df_use["zipcode"].astype(str)
    gdf_json = get_chicago_zip_geo().to_json()

    folium.Choropleth(
        geo_data=gdf_json,
        data=df_use,
        columns=["zipcode","crime_score"],
        key_on="feature.properties.zip",
        fill_color="YlGn",
        bins=[0,0.2,0.4,0.6,0.8,1.0],
        name="crime score",
        highlight=True,
        legend_name="crime score",
        
    ).add_to(m)
    
    return m


def show_environment_score(m,df_metrics): # df_metrics is the final_score_analysis that we already read in app.py
    
    df_use = df_metrics[["zipcode","environment_score"]]
    df_use["zipcode"] = df_use["zipcode"].astype(str)
    gdf_json = get_chicago_zip_geo().to_json()

    folium.Choropleth(
        geo_data=gdf_json,
        data=df_use,
        columns=["zipcode","environment_score"],
        key_on="feature.properties.zip",
        fill_color="YlGn",
        bins=[0,0.2,0.4,0.6,0.8,1.0],
        name="environment score",
        highlight=True,
        legend_name="environment score",
        
    ).add_to(m)
    
    return m


def show_final_score(m,df_metrics): # df_metrics is the final_score_analysis that we already read in app.py
    
    df_use = df_metrics[["zipcode","final_score"]]
    df_use["zipcode"] = df_use["zipcode"].astype(str)
    gdf_json = get_chicago_zip_geo().to_json()

    folium.Choropleth(
        geo_data=gdf_json,
        data=df_use,
        columns=["zipcode","final_score"],
        key_on="feature.properties.zip",
        fill_color="YlGn",
        bins=[0,0.2,0.4,0.6,0.8,1.0],
        name="final score",
        highlight=True,
        legend_name="final score",
        
    ).add_to(m)
    
    return m