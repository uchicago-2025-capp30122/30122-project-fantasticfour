## Chicago Living Score Interactive Map Website


### Team Members

- Lydia Liu
- Yuri Chang
- Hamza Tariq
- Alejandro Armas


### Abstract
This project develops an interactive, map-based platform to help individuals—especially those considering a move to Chicago—assess potential housing options. By incorporating data on education resources, transit infrastructure, public services, safety, and healthcare facilities near a chosen location, the platform offers a comprehensive overview of an area's livability.

To streamline our evaluation process, we employ a structured Living Score framework. Inspired by Numbeo’s Quality of Life Index (QoL Matrix), we craft a tailored scoring system by selecting and integrating indicators from diverse sources, ensuring both breadth and local relevance. Our finalized indicators are as follows:

**1. Housing Living Cost Index**：average housing price per sqft group by zip code

**2. Overall Economic Index**: unemployment rate, walkability score, commute time, average income, and health insurance coverage

**3. Crime Rate Index**: distribution of crime incidents

**4. Education Index**: school performance, number of schools, and supportive resources

**5. Environment Index**: number of parks, pollution reports

Our website offers two core services:

In the **Service** interface, users can enter a specific ZIP code (e.g., 60605) to receive a detailed breakdown of that area's individual indicators and overall Living Score. Alternatively, users may input a specific indicator keyword (such as “education” or “crime”) to visualize the performance of that indicator across different regions on an interactive map.

The **Analysis** interface provides an immediate, visual overview of the top 5 best and top 5 worst areas based on the overall Living Score, offering users a quick reference to compare different neighborhoods.

Leveraging **Folium for map visualizations and Flask for backend integration**, our platform delivers a dynamic and insightful experience that empowers users to explore Chicago’s livability landscape and make informed housing decisions.



### How to Use?
**Step 1:**

Go to the project main directory, install packages
```bash
$ cd ChicagoLivingScore
$ uv sync
```


**Step 2:**

Initate the website, the website will automatically open in your browser
```bash
$ uv run python -m website.app
```


**Option: Test**

You can test our analysis / map / cleaning .. part under relevant tests file

Example:
```bash
$uv run pytest tests/test_normalize.py
```



### Data Sources

#### Scraper Data - Housing Price
Source: Zillow

Helper website: https://scrapfly.io/blog/how-to-scrape-zillow/

#### Index Data

**1) Economic and infrastructure index**

Source:

**2) Environment index**

Source:

**3) Education index**

Source:

**4) Crime index**

Source:


#### Map Data

Source: https://data.cityofchicago.org/api/views/unjd-c2ca/rows.xml?accessType=DOWNLOAD



