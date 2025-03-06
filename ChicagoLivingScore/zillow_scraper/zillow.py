"""
Main source: https://scrapfly.io/blog/how-to-scrape-zillow/
"""
import json
import os
import random
import re
from typing import List
from urllib.parse import quote, urlencode
import requests
from bs4 import BeautifulSoup
import json
from loguru import logger as log
from scrapfly import ScrapeConfig, ScrapflyClient

# Support from ScrapFly website
SCRAPFLY = ScrapflyClient(key=os.environ["SCRAPFLY_KEY"])
BASE_CONFIG = {
    # Zillow.com requires Anti Scraping Protection bypass feature:
    "asp": True,
    "country": "US",
}


def create_search_payload(query_data: dict, page_number: int = None):

    # According to the dynamic nature of Zillow's website, when a search query is entered,
    # the frontend encapsulates the criteria into a payload and sends it to the backend.
    # To scrape data, we simulate this process.
    # Analyzing the Fetch/XHR code of the site, we found that the payload mainly consists of the following three elements.

    payload = {
        "searchQueryState": query_data,   # The main search query and criteria set by the user
        "wants": {"cat1": ["listResults", "mapResults"], "cat2": ["total"]}, # Data types to be returned; mapResults is needed for geographic information
        "requestId": random.randint(1, 10), # A random number used to distinguish requests
    }

    # Add pagination information to the request payload
    if page_number:
        payload["searchQueryState"]["pagination"] = {"currentPage": page_number}
    return json.dumps(payload)

# To minimize the potential impact on the website, we split the scraping process into two parts:
# One part scrapes the main Zillow search page to extract the query data for the list view.
# The other part further scrapes the detailed property information for each property in the list.

# PART 1: Scrape the main search page and extract query_data
# Using asynchronous functions to improve efficiency
async def scrape_search(url: str, max_scrape_pages: int = None) -> List[dict]:

    # Initialize list to restore the information
    search_results = []

    # 1. Scrape the search page HTML to extract query data.
    # Call Scrapfly's function to send a request based on the main search page URL
    response = await SCRAPFLY.async_scrape(ScrapeConfig(url, **BASE_CONFIG))
    soup = BeautifulSoup(response.content, "html.parser")
    # Extract the key data used for page rendering based on the HTML structure
    house_data = soup.find("script", id="__NEXT_DATA__").text
    # Parse the JSON data from __NEXT_DATA__ to extract the valid data structure (following the hierarchy)
    query_data = json.loads(house_data)["props"]["pageProps"]["searchPageState"]["queryState"]
    

    # 2. Use the extracted query_data to simulate the payload and obtain data from the backend.
    # Scrape Zillow's backend API for property listings
    backend_url = "https://www.zillow.com/async-create-search-page-state"
    headers = {"content-type": "application/json"} # Sending data in JSON format
    payload = create_search_payload(query_data) # Simulate the process of constructing the payload
    
    # Send the request and obtain the response
    backend_response = await SCRAPFLY.async_scrape(
        ScrapeConfig(backend_url, **BASE_CONFIG, headers=headers, body=payload, method="PUT")
    )
    data = json.loads(backend_response.content)


    # Add the scraped property list data to the list
    search_results.extend(data["cat1"]["searchResults"]["listResults"])
    # Get the total number of pages in the search results
    total_pages = data["cat1"]["searchList"]["totalPages"]

    # To reduce the impact on Zillow, we set it to scrape only one page at a time
    if total_pages == 1 or max_scrape_pages == 1:
        log.success(f"Scraped {len(house_data)} properties from search pages")
        return search_results
    
# PART 2: Scrape detailed property information for each property in the search results
async def scrape_properties(urls: List[str]) -> List[dict]:
    property_results = []

    # Loop through all the property detail page URLs provided
    for url in urls:
        response = await SCRAPFLY.async_scrape(ScrapeConfig(url, **BASE_CONFIG))
        soup = BeautifulSoup(response.content, "html.parser")

        # Extract the key data used for page rendering from the HTML structure
        property = soup.find("script", id="__NEXT_DATA__")
        if property:
            data = json.loads(property.text)
            # Parse the JSON data from __NEXT_DATA__ to extract the valid data structure (following the hierarchy)
            property_data = json.loads(data["props"]["pageProps"]["componentProps"]["gdpClientCache"])
            property_data = property_data[list(property_data)[0]]['property']
            property_results.append(property_data)
        else:
            log.error(f"__NEXT_DATA__ not found for URL: {url}")
    return property_results
