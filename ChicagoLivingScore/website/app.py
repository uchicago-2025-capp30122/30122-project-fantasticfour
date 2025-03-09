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
from map.mapbuild import get_chicago_zip_geo, create_map, show_unemployed_score, show_trafic_score, show_education_score, map_show_avg_price, show_crime_score, show_environment_score, show_final_score
from analysis.data_visualization_analysis import create_heatmap, combine_charts, creat_bar_chats, create_heatmap_html, create_bar_html


app = Flask(__name__)

# Load local metrics data
BASE_DIR = pathlib.Path(__file__).parent.parent  
DATA_FILE = BASE_DIR / "data" / "cleaned_data" / "final_living_score.csv"
df_metrics = pd.read_csv(DATA_FILE)

# return 2 decimals
def format_score(val):
    if pd.isnull(val):
        return "N/A"
    else:
        return f"{val:.2f}"


# Construct the main page (About page)
# Contains the Project Overview on the left and Map Overview on the right
@app.route("/")
def about():
    """
    Main page = About page:
    Left side -> Project Overview
    Right side -> Map
    """
    m = folium.Map(location=[41.8781, -87.6298], zoom_start=11, tiles='cartodbpositron')
    m = show_final_score(m, df_metrics)
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
        user_input = request.form.get("zipcode").strip().lower()

        # If the input is numeric, treat it as a ZIP code
        if user_input.isdigit():
            zipcode = user_input
            m = create_map(selected_zip=zipcode)
            # Extract related scores corresponding to the zip code
            row = df_metrics.loc[df_metrics["zipcode"] == int(zipcode)]
            if not row.empty:
                df_row = row.iloc[0]
                zip_data = {
                    "zipcode": zipcode,
                    "housing_price": format_score(df_row.get("avg_price_per_sqft")),
                    "unemployed_score": format_score(df_row.get("unemployed_score")),
                    "commute_time_score": format_score(df_row.get("commute_time_score")),
                    "avg_income_score": format_score(df_row.get("avg_income_score")),
                    "private_insurance_score": format_score(df_row.get("private_insurance_score")),
                    "education_score": format_score(df_row.get("education_score")),
                    "crime_score": format_score(df_row.get("crime_score")),
                    "environment_score": format_score(df_row.get("environment_score")),
                    "final_score": format_score(df_row.get("final_score"))
                }
            else:
                zip_data = {
                    "zipcode": zipcode,
                    "housing_price": "N/A",
                    "unemployed_score": "N/A",
                    "commute_time_score": "N/A",
                    "avg_income_score": "N/A",
                    "private_insurance_score": "N/A",
                    "education_score": "N/A",
                    "crime_score": "N/A",
                    "environment_score": "N/A",
                    "final_score": "N/A"
                }
            # For GET requests, display the default map
            m = create_map(selected_zip=zipcode)
            map_html = m._repr_html_()

        # Handle keyword inputs to show specific indicators distribution
        elif user_input == "education":
            m = create_map()
            # Call the show_education_score function from mapbuild.py
            m = show_education_score(m, df_metrics)
            map_html = m._repr_html_()

        elif user_input == "crime":
            m = create_map()
            m = show_crime_score(m, df_metrics)
            map_html = m._repr_html_()

        elif user_input == "environment":
            m = create_map()
            m = show_environment_score(m, df_metrics)
            map_html = m._repr_html_()

        elif user_input == "traffic":
            m = create_map()
            m = show_trafic_score(m, df_metrics)
            map_html = m._repr_html_()

        elif user_input == "housing":
            m = create_map()
            m = map_show_avg_price(m, df_metrics)
            map_html = m._repr_html_()

        elif user_input == "unemployment":
            m = create_map()
            m = show_unemployed_score(m, df_metrics)
            map_html = m._repr_html_()

        elif user_input == "final":
            m = create_map()
            m = show_final_score(m, df_metrics)
            map_html = m._repr_html_()

        else:
            # For other inputs, just show the default map with placeholder data
            m = create_map()
            map_html = m._repr_html_()
            zip_data = {
                "zipcode": user_input,
                "housing_price": "N/A",
                "unemployed_score": "N/A",
                "commute_time_score": "N/A",
                "avg_income_score": "N/A",
                "private_insurance_score": "N/A",
                "education_score": "N/A",
                "crime_score": "N/A",
                "environment_score": "N/A",
                "final_score": "N/A"
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
    chart_html = None
    if request.method == "POST":
        query = request.form.get("query", "").strip().lower()
        # check whether the query is numeric or a keyword
        if query == "top 5":
            from analysis.data_visualization_analysis import create_bar_html
            chart_html = create_bar_html(df_metrics)
        elif query == "relationship":
            from analysis.data_visualization_analysis import create_heatmap_html
            chart_html = create_heatmap_html(df_metrics)
        else:
            results = "Analysis is not implemented yet."


    return render_template("analysis.html", results=results, chart_html=chart_html)



@app.route("/github")
def github():
    return render_template("github.html")



def open_browser():
    if os.environ.get("WERKZEUG_RUN_MAIN") == "true":
        webbrowser.open_new("http://127.0.0.1:5001/")


if __name__ == "__main__":
    Timer(1, open_browser).start()
    app.run(host="0.0.0.0", port=5001, debug=True)