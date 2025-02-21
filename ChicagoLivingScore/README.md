### Team Members


### Abstract
This project develops an interactive, map-based platform to help individuals—especially those considering a move to Chicago—assess potential housing options. By incorporating data on education resources, transit infrastructure, public services, safety, and healthcare facilities near a chosen location, the platform offers a comprehensive overview of an area's livability.

To streamline our evaluation process, we employ a structured Living Score framework. Inspired by Numbeo’s Quality of Life Index (QoL Matrix), we craft a tailored scoring system by selecting and integrating indicators from diverse sources, ensuring both breadth and local relevance. Our finalized indicators are as follows:

**1. Housing Living Cost Index**：average housing price per sqft group by zip code

**2. Overall Economic Index**: unemployment rate, walkability score, commute time, average income, and health insurance coverage

**3. Crime Rate Index**: distribution of crime incidents

**4. Education Index**: school performance, number of schools, and supportive resources

**5. Environment Index**: number of parks, pollution reports

When a user clicks on a Zip Code, the platform displays a detailed breakdown of these scores and an overall score. Users can further filter areas based on personal preferences (e.g., best family-friendly neighborhoods, safest locations, etc.). The system leverages **Folium and Flask** to deliver a fully interactive map-based website, enabling an engaging and insightful exploration of Chicago’s livability landscape.


### Project Structure

```bash
ChicagoLivingScore/
├── .venv/
├── analysis/
│   └── zillow_data_analysis.py
├── data/
│   ├── cleaned_data/
│   │   └── Housing_Data_Final.csv
│   └── raw_data/
│       └── Housing_Data.csv
├── map/ 
├── scraper/
│   ├── scraper_data/
│   │   └── zillow.py
├── website/
│   ├── static/
│   ├── templates/
│   └── app.py
├── pyproject.toml
├── uv.lock
├── README.md
└── ...
```



#### Project Stucture Details
This project is structured in the following section
- Data(\data)
    - raw_data:
      
        original datasets downloaded from Chicago Data Portal
        scraped datasets from Zillow
    - cleaned_data:
      
        normalized datasets after cleaning, analyzing

- Scraper(\scraper)
    - results:
      
        extracted datasets from Zillow
    - function:
      
        main scraper function(\zillow.py)
      
        change url for scraping (\run.py)

- Map and Spatial Analysis(\map)

- Interactive Website(\website)
    - main function (\app.py)
    - fronend file:
      
        templates(\base.html; \about.html; \service.html; \analyis.html; github.html\)
      
        static(style.css)


### Data Sources
**1. Scraped Dataset: Housing Data from Zillow**
**How to Use?**
Step 1:

Register on https://scrapfly.io/login to get the API key
```bash
$ export SCRAPFLY_KEY="YOUR SCRAPFLY KEY"
```
Step 2:
```bash
$ git clone https://github.com/scrapfly/scrapfly-scrapers.git
$ cd ChicagoLivingScore/scraper
$ poetry install
```
Step 3:
Open the **run.py**, customize 2 urls:

1) First url: 
   Open the main interface of Zillow, after entering the the city or zip code or address you want to search, you will be led to a main interface with map and property listing, use the url of this page as our first url
2) Seconf url:
   On the same page, randomly click one of the house listings, then you will be led to a page listed the detailed properties of this listing, use the url of the new page as your second url

After changing these 2 urls, please enter:
```bash
$ poetry run python run.py
```
Step 4:
You can check the extracted results stored in the **results** file.

Overall we utilized the API supported by Scrapefly, and we rewrote the code using the skills during this quarter. In order to avoid influence on Zillow, we limit 1 page of scraping per time, once you can scrape around 80-100 house listing information. If you want to get more data, please change the urls every time you run, and the free limiation of one account is 1000.

**Please see more deatails in the zillow.py by checking the comments**


### How to Run
```bash
uv sync
```
**1) How to scrape data?**
```bash
Please see the **Data Source** section for more deatils
```
**2) How to clean and normalize the raw datsets?**
   
Example: housing datasets from Zillow
```bash
$ cd ChicagoLivingScore/analysis
$ uv run python zillow_data_analysis.py
```

**3) How to initiate the website**
```bash
$ cd ChicagoLivingScore/website
$ uv run python app.py
```
**The Website is composted of 4 Parts, please use the navigation bar to see the deatils**

**1) About**:

the main page of website, where we can check the website function overview

**2) Service**:

on this page, we can utilize the main function of our project, please input the zip code you want to explore in the search bar on the left side, then we will display the corresponding scores of this area, and this area will also pop out on the map.

(for now since we don't have the finalized analysis datasets yet, we will the sample score as placeholder)

**3) Analysis**:

on this page, we would like to display the overview of the datasets, like inputing certain zip code or metrics category (like education, environment), and we will display the visualization analysis of this category

**4) Github**:

link to our github




