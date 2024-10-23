from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from tenacity import retry, stop_after_attempt, wait_exponential

'''@retry(stop=stop_after_attempt(3),wait=wait_exponential(multiplier=1,min=2,max=10))
def fetch_page_content(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        
        if "application/json" in response.headers.get('Content-Type', ''):
            return response.json(), 'json'

        if use_selenium:
            return fetch_dynamic_page(url), 'html'
        return response.text, 'html'
    
    except requests.exceptions.RequestException as e:
        raise Exception(f"Failed to fetch content from {url}: {e}") 
        return response.text
    
def fetch_dynamic_content(url):
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(options = chrome_options)
    driver.get(url)
    page_source = driver.page_source
    driver.quit()
    try:
        driver.get(url)
        return driver.page_source
    finally:
        driver.quit()

def selective_scrape(html_content, instruction):

    soup = BeautifulSoup(html_content, 'html.parser')

    if instruction == 'heading':
        return [heading.get_text(strip=True) for heading in soup.find_all(['h1', 'h2', 'h3'])]
    elif instruction == 'paragraph':
        return [p.get_text(strip=True) for p in soup.find_all('p')]
    elif instruction == 'link':
        return [a['href'] for a in soup.find_all('a', href=True)]
    elif instruction == 'image':
        return [img['src'] for img in soup.find_all('img', src=True)]
    else:
        return [p.get_text(strip=True) for p in soup.find_all('p')]


def interpret_json(json_data, prompt):
    if 'title' in prompt.lower():
        return [item.get('title') for item in json_data if 'title' in item]
    elif 'name' in prompt.lower():
        return [item.get('name') for item in json_data if 'name' in item]
    elif 'price' in prompt.lower():
        return [item.get('price') for item in json_data if 'price' in item]
    else:
        return json_data'''
'''def extract_relevant_data(page_content,instructions):
    soup = BeautifulSoup(page_content,"html.parser")
    return process_instructions(soup,instructions)'''

def scrape_website(url: str, keywords: list, use_selenium: bool = False):
    """
    Scrapes the website based on the provided URL and keywords.
    Supports both JSON and HTML files. Uses Selenium for dynamic content.
    :param url: The target URL to scrape
    :param keywords: A list of keywords to search for in the page content
    :param use_selenium: Set to True if the page needs to be rendered using Selenium
    :return: A dictionary with extracted data or an error message
    """
    try:
        if use_selenium:
            # Step 1: Use Selenium for JavaScript-rendered pages
            driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
            driver.get(url)
            page_source = driver.page_source
            driver.quit()
            return scrape_html_content(page_source, keywords)
        
        else:
            # Step 2: Use Requests for static HTML or JSON
            response = requests.get(url)
            response.raise_for_status()
            
            content_type = response.headers.get('Content-Type')
            
            if 'application/json' in content_type:
                # If the response is JSON
                return scrape_json_content(response.json(), keywords)
            else:
                # If the response is HTML
                return scrape_html_content(response.text, keywords)
    
    except requests.exceptions.RequestException as e:
        return {"error": f"An error occurred: {e}"}
    except Exception as e:
        return {"error": f"An unexpected error occurred: {e}"}

def scrape_html_content(html_content: str, keywords: list):
    """
    Scrapes relevant data from HTML content using BeautifulSoup.
    :param html_content: The HTML content as a string
    :param keywords: A list of keywords to search for in the HTML content
    :return: Extracted data in JSON format
    """
    soup = BeautifulSoup(html_content, 'html.parser')
    
    relevant_data = []
    for keyword in keywords:
        # Search for the keyword in the HTML content (searching paragraphs, headers, etc.)
        keyword_related_sections = soup.find_all(text=lambda text: text and keyword.lower() in text.lower())
        for section in keyword_related_sections:
            relevant_data.append(section.strip())
    
    return {"type": "html", "keywords": keywords, "extracted_data": relevant_data[:5]}

def scrape_json_content(json_data: dict, keywords: list):
    """
    Scrapes relevant data from JSON content.
    :param json_data: The JSON content as a dictionary
    :param keywords: A list of keywords to search for in the JSON data
    :return: Extracted data in JSON format
    """
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
    for keyword in keywords:
        find_in_json(json_data, keyword)
    
    return {"type": "json", "keywords": keywords, "extracted_data": relevant_data[:5]}