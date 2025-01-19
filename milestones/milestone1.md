# {Fantastic Four}

## Members

- Ziqi(Lydia) Liu <ziqil@uchicago.edu>
- Alejandro Armas <alarmasb@uchicago.edu>
- Rongruo(Yuri) Chang <yurichang@uchicago.edu>
- Name <name@uchicago.edu>

## Abstract

This project aims to develop an interactive map-based platform to assist individuals, especially those planning to move to Chicago, in evaluating potential housing options. By integrating data on essential factors like the education resources, transit facilities, public services, safety, and healthcare facilities nearby the location that people input, the platform will provide users with a comprehensive understanding of a location's livability.

Using publicly available datasets from sources like the Chicago Data Portal, and housing websites like Zillowwe will perform data collection, cleaning, and feature engineering. Each address input by users will be geocoded to latitude and longitude, allowing us to spatially merge it with relevant datasets. Advanced analytical methods, including clustering techniques (e.g., K-Means, K-Prototype), will categorize Chicago’s neighborhoods into groups such as “Highly Suitable for Living” or “Less Suitable,” based on weighted scores derived from metrics.

The results will be presented via an interactive web-based map, created with tools like Folium or Plotly Dash. Users can input specific addresses to explore nearby amenities and safety conditions.


## Preliminary Data Sources

### Data Source #1: city of chicago

https://data.cityofchicago.org/

  - Type: Webpage
  - Retrieve Methods: Open-source CSV files
  - Useful Information: We will use datasets related to education, parks & recreation, health, transportation, public safety, and food from this website. These datasets will form the core metrics influencing people’s decisions on whether to live in a specific area.
  - Potential Challenges: Since the datasets are diverse and some contain large amounts of data, we might need to sample metrics with excessive data volume during later stages. Additionally, extensive data preprocessing will be required, such as standardizing data ranges to ensure uniformity.

### Data Source #2: real estate website

https://www.zillow.com/
https://www.realtor.com/

  - Type: API
  - Useful Information: We will use these real estate websites to gather the addresses of housing spots in Chicago. These addresses will be linked with other core metrics.
  - Potential Challenges: Initial research suggests that scraping data from Zillow is feasible; however, if any issues arise, Realtor will serve as a backup option.

### Data Source #3: geographic information

https://data.cityofchicago.org/

  - Type: Webpage
  - Useful Information: We will retrieve geographic boundaries of Chicago, specifically GeoJSON files, to aid in visualizing geographical boundaries.


## Preliminary Project Plan

1. Retrieve Data
We will employ a combination of open-source databases and APIs to collect datasets related to housing and key factors affecting livability in Chicago. For example
Housing Data: Zillow / Realtor (API)
Public Services: Chicago Data Portal (Open-source CSV)
Safety Data: Chicago Data Portal (Open-source CSV)
Geographic Data: Chicago Data Portal (GeoJSON)

2. Data Preprocessing
Given the complexity and diversity of the data sources, comprehensive preprocessing steps are essential to ensure data reliability and usability:
-	Handling Missing Values (like imputation)
-	Handling Outliers (like log transformation)
-	Data Standardization (standardize, one-hot encoding, ect.)

3. Analytical Models
1) Scoring System:
Develop a livability index by assigning weighted scores to factors such as safety, transit, schools, and public services. Calculate weighted averages or use machine learning models like Random Forest to assess feature importance.
2) Clustering Analysis:
Categorize neighborhoods based on livability factors. For now, consider using K-Means and K-Prototype to cluster various categories based on the overall living condition of different areas.


4. Data Visualization
For now, we consider utilizing tools like Folium, Plotly Dash to build interactive maps, to display housing and neighborhood scores based on user-input addresses. Clustering results (e.g., color-coded areas for livability).



## Questions

A **numbered** list of questions for us to respond to.
