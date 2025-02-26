from flask import Flask, render_template, jsonify, request
import folium
import geopandas as gpd
import pandas as pd
from shapely import wkt
from shapely.geometry import Point
import httpx
import lxml.html
import pathlib
import webbrowser
from threading import Timer
import os
from map.mapbuild import get_chicago_zip_geo, create_map, map_add_schools


app = Flask(__name__)

# Load local metrics data
BASE_DIR = pathlib.Path(__file__).parent
DATA_FILE = BASE_DIR / ".." / "data" / "cleaned_data" / "cleaned_data_housing.csv"
df_metrics = pd.read_csv(DATA_FILE)


# Construct the main page (About page)
# Contains the Project Overview on the left and Map Overview on the right
@app.route("/")
def about():
    """
    Main page = About page:
    Left side -> Project Overview
    Right side -> Map
    """
    m = create_map()
    map_html = m._repr_html_()
    return render_template("about.html", map_html=map_html)

# Construct the main functionality of the website - Service page
# Contains a search input bar for users to input a Zip code, displaying corresponding scores,
# or directly clicking on the map on the right to display the corresponding scores.
@app.route("/service", methods=["GET", "POST"])
def service():
    """
    Service page:
    Left side: input zip code
    Right side: show map with the selected zip highlighted
    """
    map_html = None
    zip_data = None

    if request.method == "POST":
        user_input = request.form.get("zipcode").strip()

        # Example: 从 local metrics 中查询
        if user_input.isdigit():
            zipcode = user_input
            m = create_map(selected_zip=zipcode)
            # Extract related scores corresponding to the zip code
            row = df_metrics.loc[df_metrics["zipcode"] == int(zipcode)]
            if not row.empty:
                zip_data = {
                    "zipcode": zipcode,
                    "education_score": row.iloc[0].get("education_score", "N/A"),
                    "crime_score": row.iloc[0].get("crime_score", "N/A"),
                    "housing_score": row.iloc[0].get("housing_score", "N/A"),
                    "overall_score": row.iloc[0].get("overall_score", "N/A"),
                }
            else:
                zip_data = {
                    "zipcode": zipcode,
                    "education_score": "N/A",
                    "crime_score": "N/A",
                    "housing_score": "N/A",
                    "overall_score": "N/A",
                }
            # For GET requests, display the default map
            m = map_add_schools(m, selected_zip=zipcode)
            map_html = m._repr_html_()

        
        elif user_input.lower() == "education":
            m = create_map()  
            m = map_add_schools(m)  
            map_html = m._repr_html_()

            zip_data = {
                "zipcode": "N/A",
                "education_score": "N/A",
                "crime_score": "N/A",
                "housing_score": "N/A",
                "overall_score": "N/A",
            }

        else:
            m = create_map()
            map_html = m._repr_html_()
            zip_data = {
                "zipcode": user_input,
                "education_score": "N/A",
                "crime_score": "N/A",
                "housing_score": "N/A",
                "overall_score": "N/A",
            }

    else:
        # GET post, display the deafult map
        m = create_map()
        map_html = m._repr_html_()

    return render_template("service.html", map_html=map_html, zip_data=zip_data)


# Construct the Analysis Page for presenting data analysis results directly
@app.route("/analysis", methods=["GET", "POST"])
def analysis():
    """
    Analysis page:
    For advanced queries, like input a zip code or some keywords (like 'school') to display data analysis
    """
    results = None
    if request.method == "POST":
        query = request.form.get("query")
        # check whether the query is numeric or a keyword
        if query and query.isdigit():
            row = df_metrics.loc[df_metrics["zipcode"] == int(query)]
            # Here is just example placeholder, waiting for analysis
            if not row.empty:
                results = f"Analysis results for ZIP code {query} => Education={row.iloc[0]['education_score']}, Crime={row.iloc[0]['crime_score']}..."
            else:
                results = f"No data found for ZIP code {query}"
        else:
            results = f"Analysis for keyword '{query}' is not implemented yet."

    return render_template("analysis.html", results=results)



@app.route("/github")
def github():
    """
    Github page: link to your GitHub repository
    """
    return render_template("github.html")



# Test data for placeholder
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


def open_browser():
    if os.environ.get("WERKZEUG_RUN_MAIN") == "true":
        webbrowser.open_new("http://127.0.0.1:5001/")


if __name__ == "__main__":
    Timer(1, open_browser).start()
    app.run(host="0.0.0.0", port=5001, debug=True)