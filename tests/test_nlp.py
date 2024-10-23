from utils.scraper import Scraper
import pytest

def test():
  content = Scraper().scrape(url="https://www.uta.edu/",keywords=["Admissions"])
  print(content)
  print(type(content))

  assert "Admissions" in content["extracted_data"], 'Expected text not found in the page content'
