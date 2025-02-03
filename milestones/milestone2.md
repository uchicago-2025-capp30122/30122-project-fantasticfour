# {Fantastic Four}

## Members

- Ziqi(Lydia) Liu <ziqil@uchicago.edu>
- Alejandro Armas <alarmasb@uchicago.edu>
- Rongruo(Yuri) Chang <yurichang@uchicago.edu>
- Hamza Tariq <hamzatariq@uchicago.edu>

## Abstract

This project aims to develop an interactive map-based platform to assist individuals, especially those planning to move to Chicago, in evaluating potential housing options. By integrating data on essential factors like education resources, transit facilities, public services, safety, and healthcare facilities near a given location, the platform will provide users with a comprehensive understanding of a location's livability.

To standardize our evaluation process, we have decided to adopt a structured **Living Score** framework. The primary reference for this framework is **Numbeo’s Quality of Life Index (QoL Matrix)**, which provides a benchmark for defining livability across various dimensions. However, instead of directly using Numbeo's index, we will design a customized livability score by selecting and combining indicators from different sources to ensure a holistic and localized assessment. Zip Codes will be **color-coded based on livability scores (e.g., heatmap representation)**. Clicking on a Zip Code will display a **breakdown of individual scores** for education, crime rate, transit, and other factors. Users can filter areas based on their own preferences (like if they want the best areas for families, or safest neighborhoods”).


## Data Sources
Please review the following table for a quick overview of the indexes affecting livability scores and their corresponding data sources.

#### Indicators & Weights

| Category               | Indicator                           | Weight (%) | Source  |
|------------------------|------------------------------------|------------|------------------------------------------------------|
| **Economic Stability** | Job Opportunities (Unemployment Rate) | 10%       | United States Census Bureau |
|                        | Income & Economic Well-Being               | 6%         | United States Census Bureau |
|                        | Health Insurance Coverage               | 3%         | United States Census Bureau|
| **Real Estate & Housing** | Median Rent Price                | 10%        | Zillow  |
|                        | Real Estate Price per sqft        | 8%         | Zillow  |
| **Infrastructure**      | Public Transport Accessibility    | 7%         | United States Census Bureau |
|                        | Traffic Congestion                | 7%         | United States Census Bureau |
|                        | Commute Time                      | 6%         | United States Census Bureau |
|                        | Walkability Score                 | 5%         | Under Consideration |
| **Safety & Healthcare** | Crime Rate                        | 8%         | portal |
|                        | Healthcare Quality/access         | 7%         | portal (May need to find the right variable) |
| **Environment & Climate** | Pollution Index                 | 5%         | portal |
|                        | Air Quality Index                 | 5%         | EPA/local pollution monitoring |
|                        | Green Space & Parks Access       | 5%         | portal |
| **Social & Cultural**   | Education Quality                 | 6%         | portal |
|                        | Cultural & Recreational           | 5%         | portal |


### Data Source #1: city of chicago, United States Census Bureau

https://data.cityofchicago.org/

https://data.census.gov/

  - Type: Webpage
  - Retrieve Methods: Open-source CSV files
  #### United States Census Bureau
      - For Ecomonic & Infrastructure indexes
      - Description:
          - 53 rows
          - 137 columns (variables)
      - Insights from the Data
        - Economic Activity: Employment rates and income distribution.
        - Economic Inequality: Poverty levels.
        - Quality of Life: Commuting times, healthcare access, and reliance on public assistance.
        - To assess the economic conditions and affordability of different neighborhoods in Chicago, we have selected the most relevant variables from the Census dataset. These indicators will help evaluate job availability, income distribution, poverty levels, and access to essential services factors that directly influence livability.

  #### city of chicago
      - For Ecomonic & Infrastructure indexes
      - Description:
          - 53 rows
          - 137 columns (variables)
      - Insights from the Data
        - Economic Activity: Employment rates and income distribution.
        - Economic Inequality: Poverty levels.
        - Quality of Life: Commuting times, healthcare access, and reliance on public assistance.
        - To assess the economic conditions and affordability of different neighborhoods in Chicago, we have selected the most relevant variables from the Census dataset. These indicators will help evaluate job availability, income distribution, poverty levels, and access to essential services factors that directly influence livability.



### Data Source #2: real estate website

https://www.zillow.com/

  - Type: API
  - We have successfully build the scraper that can retrieve data from zillow, in order to minimize the effect, we restrict the max_pages as 1 page per time. Please check the **milestone2** file to find more details and sample dataset.
  - To better align with Zillow's data structure, we will store the search interface data and individual property details in separate databases. Overall, these two databases contain the following:
      - 1. Search Dataset:
           - Rows: 4000 (planned for scraping)
           - Columns: 72 (variables)
      - 2. Property Dataset:
           - Rows: 4000 (planned for scraping)
           - Columns: 56 (variables)
   - We will only use the following relevant variables from these datasets: **address, zip code (for linking the databases), price, and size (sqft)**. These variables will help us calculate key metrics such as **Median Rent Price and Real Estate Price per sqft**. After an initial data check, we have confirmed that over 95% of the data contains these essential variables.
          

### Data Source #3: geographic information

https://data.cityofchicago.org/

  - Type: Webpage (CSV file)
  - Data Description:
      - Rows: 61
      - Columns: 5 (variables) - the_geom, OBJECTID, **ZIP**, SHAPE_AREA, SHAPE_LEN
  - The zip code map dataset contains **polygon geometries** that define the boundaries of each zip code area. This dataset will be stored in a **GeoDataFrame**, allowing us to perform spatial operations in Python. Meanwhile, our search and property datasets contain real estate information, including price, size (sqft), and ZIP codes. Since the ZIP code serves as a unique identifier in both datasets, it will be used as the key to join the geospatial and real estate data.


## Project Plan (Feb. 3 - Feb. 14)

This phase of the project focuses on **data preprocessing, feature engineering, livability index calculation, and interactive map research**. The goal is to ensure that all datasets are properly cleaned, structured, and prepared for visualization.

#### Special notes:
Since different variables have vastly different scales, we will apply **Min-Max Scaling** to normalize them between 0 and 1. For various datasets, we will apply **Zip Codes as the key geographic identifier to link various datasets**. Each livability factor (e.g., Education Quality) will be assigned a score. For example, within Education Quality, we will evaluate the number of public and private schools within a Zip Code, comparing it with other areas to determine a relative score. The weight assigned to each factor will depend on its impact on livability and the **data distribution (we may use principal component analysis (PCA)** to determine optimal weighting, or adopt predefined weights based on policy research). Each index’s weight will be adjusted based on its significance and combined to generate a Total Livability Score per Zip Code.

#### 1. Data Preprocessing (Feb. 3 - Feb. 6) - Lydia, Alejandro
- Ensure all datasets (City of Chicago, Zillow API, and geographic information) are properly retrieved and structured.
- Handle missing values, inconsistencies, and standardize units for real estate metrics.
- Link datasets using ZIP code as the primary key.

##### 2. Feature Engineering & Index Calculation (Feb. 7 - Feb. 10) - Lydia, Hamza
- Define transformations for livability score components.
- Apply Min-Max Scaling to normalize metrics across different scales.
- Compute key metrics:
    - Median Rent Price
    - Real Estate Price per Sqft
    - Education Index (school density per ZIP code)
    - Safety Index (crime rate per ZIP code)
    - … (to decide later)
- Determine appropriate weights for each metric (e.g., rule-based or PCA-based feature selection).

#### 3. Exploratory Data Analysis (EDA) (Feb. 11 - Feb. 14) - Hamza, Alejandro
- Generate summary statistics for each key index (rent price distribution, safety levels, etc.).
- Create initial visualizations (box plots, heatmaps) to understand spatial distribution.
- Detects outliers in price and livability scores.

#### 4. Interactive Map Research & Prototyping (Feb. 8 - Feb. 14) - Yuri
- Explore different visualization frameworks (Folium, Plotly Dash).
- Load and render the zip code boundaries on an interactive map.




## Questions

A **numbered** list of questions for us to respond to.
