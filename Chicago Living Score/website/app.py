from flask import Flask, render_template, jsonify, request
import folium
import geopandas as gpd
import pandas as pd
from shapely import wkt
import httpx
import lxml.html
import pathlib

app = Flask(__name__)

# Load local metrics data
BASE_DIR = pathlib.Path(__file__).parent
DATA_FILE = BASE_DIR / ".." / "data" / "cleaned_data" / "Housing_Data_Final.csv"
df_metrics = pd.read_csv(DATA_FILE)


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
    for i in range(1, len(polygon_lst)):
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

# Render the home page with a default map (no zip code selected)
@app.route("/")
def index():
    m = create_map()
    map_html = m._repr_html_()
    return render_template("index.html", map_html=map_html)



@app.route("/api/zip/<zipcode>")
def get_zip_data(zipcode):
    """
    Placeholder endpoint: returns self-written JSON data for a given zip code.
    This will be replaced with a real database metrics
    """
    data = {
        "zipcode": zipcode,
        "education_score": 0.8,
        "crime_score": 0.3,
        "housing_score": 0.7,
        "overall_score": 0.75
    }
    return jsonify(data)


@app.route("/search", methods=["POST"])
def search_zip():
    zipcode = request.form.get("zipcode")
    # Create a new map highlighting the selected zipcode
    m = create_map(selected_zip=zipcode)
    map_html = m._repr_html_()
    # Get placeholder metrics (in future, fetch real data)
    data = {
        "zipcode": zipcode,
        "education_score": 0.8,
        "crime_score": 0.3,
        "housing_score": 0.7,
        "overall_score": 0.75
    }
    return render_template("index.html", map_html=map_html, zip_data=data)


# Below is the true logic, can initiate once have the prepared datasets
#@app.route("/search", methods=["POST"])
#def search_zip():
    zipcode = request.form.get("zipcode")
    # Generate map and highlight the zip area that is input by user
    m = create_map(selected_zip=zipcode)
    map_html = m._repr_html_()
    
    # Search the corresponding metrics based on zip code from dataset metrics
    row = df_metrics.loc[df_metrics['zipcode'] == int(zipcode)]  
    if not row.empty:
        data = {
            "zipcode": zipcode,
            "education_score": row.iloc[0]['education_score'],
            "crime_score": row.iloc[0]['crime_score'],
            "housing_score": row.iloc[0]['housing_score'],
            "overall_score": row.iloc[0]['overall_score']
        }
    else:
        # If cannot search the result
        data = {
            "zipcode": zipcode,
            "education_score": "N/A",
            "crime_score": "N/A",
            "housing_score": "N/A",
            "overall_score": "N/A"
        }

    return render_template("index.html", map_html=map_html, zip_data=data)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)