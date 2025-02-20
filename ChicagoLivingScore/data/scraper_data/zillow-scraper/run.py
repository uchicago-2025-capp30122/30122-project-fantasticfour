"""
This example run script shows how to run the Zillow scraper defined in ./zillow.py
It scrapes hotel data and saves it to ./results/

To run this script set the env variable $SCRAPFLY_KEY with your scrapfly API key:
$ export $SCRAPFLY_KEY="your key from https://scrapfly.io/dashboard"
"""
import asyncio
import json
from pathlib import Path
import zillow

output = Path(__file__).parent / "results"
output.mkdir(exist_ok=True)


async def run():
    # enable scrapfly cache for basic use
    zillow.BASE_CONFIG["cache"] = True

    print("running Zillow scrape and saving results to ./results directory")

    url = "https://www.zillow.com/chicago-il/3_p/?searchQueryState=%7B%22pagination%22%3A%7B%22currentPage%22%3A3%7D%2C%22isMapVisible%22%3Atrue%2C%22mapBounds%22%3A%7B%22west%22%3A-88.8470543046875%2C%22east%22%3A-86.6168296953125%2C%22south%22%3A41.215077112846544%2C%22north%22%3A42.44701957473035%7D%2C%22regionSelection%22%3A%5B%7B%22regionId%22%3A17426%2C%22regionType%22%3A6%7D%5D%2C%22filterState%22%3A%7B%22sort%22%3A%7B%22value%22%3A%22days%22%7D%7D%2C%22isListVisible%22%3Atrue%2C%22mapZoom%22%3A9%2C%22usersSearchTerm%22%3A%22Chicago%20IL%22%7D"
    result_location = await zillow.scrape_search(url=url, max_scrape_pages=1)
    output.joinpath("search.json").write_text(json.dumps(result_location, indent=2, ensure_ascii=False))

    url = "https://www.zillow.com/homedetails/800-N-Michigan-Ave-APT-3203-Chicago-IL-60611/60202083_zpid/"
    result_property = await zillow.scrape_properties([url,])
    output.joinpath("property.json").write_text(json.dumps(result_property[0], indent=2, ensure_ascii=False))


if __name__ == "__main__":
    asyncio.run(run())
