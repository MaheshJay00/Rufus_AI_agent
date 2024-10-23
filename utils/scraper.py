from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from utils.nlp_processor import process_instructions


def fetch_page_content(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except Exception as e:
        raise e
    
def fetch_dynamic_content(url):
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    #driver_path = "/path/to/chromedriver"  #replace path
    service = Service(driver_path)
    driver = webdriver.Chrome(service = service , options = chrome_options)
    driver.get(url)
    page_source = driver.page_source
    driver.quit()
    return page_source

def extract_relevant_data(page_content,instructions):
    soup = BeautifulSoup(page_content,"html.parser")
    return process_instructions(soup,instructions)