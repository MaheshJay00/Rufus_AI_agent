import json

from utils.error_handler import handle_error
from utils.scraper import (extract_relevant_data, fetch_dynamic_content,
                           fetch_page_content)


class RufusClient:
    def __init__(self,api_key):
        self.api = api_key
        
    def scrape(self,url,instructions,use_selenium=False):
        try:
            if use_selenium:
                content = fetch_dynamic_content(url)
            else:
                content = fetch_page_content(url)
                
            if content:
                return extract_relevant_data(content,instructions)
            return None
        except Exception as e:
            handle_error(e)
            
    def get_results(self,results):
        return json.dumps(results,indent = 4)