import json

from utils.scraper import Scraper
from utils.nlp_processor import extract_keywords
from utils.error_handler import handle_error


class RufusClient:

    def __init__(self, api_key=None, use_selenium=False):
         
        self.api_key = api_key
        self.scraper = Scraper(use_selenium=use_selenium)

    def scrape(self, url: str, instructions: str = "Scrape relevant data"):
        
        # Extract keywords from instructions (you can enhance this part)
        keywords = extract_keywords(instructions)

        # Use the Scraper class to perform the actual scraping
        scraped_data = self.scraper.scrape(url, keywords)
        return scraped_data
   