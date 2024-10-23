from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from tenacity import retry, stop_after_attempt, wait_exponential

class Scraper:
    def __init__(self):
        
        self.use_selenium = False

    def scrape(self, url: str, keywords: list = None):
        
        use_selenium = False
        if use_selenium:
            return self.scrape_with_selenium(url, keywords)
        else:
            return self.scrape_with_requests(url, keywords)

    def scrape_with_requests(self, url: str, keywords: list = None):
        
        try:
            response = requests.get(url)
            response.raise_for_status()  # Check if the request was successful
            
            content_type = response.headers.get('Content-Type')
            
            if 'application/json' in content_type:
                return self.scrape_json(response.json(), keywords)
            else:
                return self.scrape_html(response.text, keywords)
        
        except requests.exceptions.RequestException as e:
            return {"error": f"An error occurred: {e}"}
    
    def scrape_with_selenium(self, url: str, keywords: list = None):
        
        try:
            # Setup Selenium WebDriver (Chrome in this case)
            options = webdriver.ChromeOptions()
            options.add_argument("--headless")  # Run in headless mode
            driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
            
            # Open the URL
            driver.get(url)
            page_source = driver.page_source
            
            # Close the driver
            driver.quit()

            # Scrape the HTML using BeautifulSoup
            return self.scrape_html(page_source, keywords)
        
        except Exception as e:
            return {"error": f"An error occurred while using Selenium: {e}"}

    def scrape_html(self, html_content: str, keywords: list = None):
        
        soup = BeautifulSoup(html_content, 'html.parser')
        
        relevant_data = []
        if keywords:
            # Find relevant sections of the page based on the provided keywords
            for keyword in keywords:
                keyword_related_sections = soup.find_all(text=lambda text: text and keyword.lower() in text.lower())
                for section in keyword_related_sections:
                    relevant_data.append(section.strip())
        else:
            # Return the first 5 paragraphs by default
            paragraphs = [p.get_text() for p in soup.find_all('p')][:5]
            relevant_data.extend(paragraphs)
        
        return {"type": "html", "keywords": keywords, "extracted_data": relevant_data}

    def scrape_json(self, json_data: dict, keywords: list = None):
        
        relevant_data = []

        def find_in_json(data, keyword):
            if isinstance(data, dict):
                for key, value in data.items():
                    if keyword.lower() in key.lower() or (isinstance(value, str) and keyword.lower() in value.lower()):
                        relevant_data.append({key: value})
                    find_in_json(value, keyword)
            elif isinstance(data, list):
                for item in data:
                    find_in_json(item, keyword)

        # Search for each keyword in the JSON data
        if keywords:
            for keyword in keywords:
                find_in_json(json_data, keyword)
        else:
            relevant_data.append(json_data)

        return {"type": "json", "keywords": keywords, "extracted_data": relevant_data[:5]}