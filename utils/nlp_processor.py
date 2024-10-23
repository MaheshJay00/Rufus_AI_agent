from urllib.parse import urljoin

import spacy

nlp = spacy.load("en_core_web_sm")

def process_instructions(soup,instructions):
    data = {"instructions":instructions,"scraped_data":{}}
    doc = nlp(instructions)
    
    if "FAQ" in instructions or any(token.lemma_ == 'FAQ' for token in doc):
        data['scraped_data']['faqs'] = scrape_faqs(soup)
    if "pricing" in instructions or any(token.lemma_ == 'price' for token in doc):
        data['scraped_data']['pricing']=scrape_pricing(soup)
    if 'application' in instructions or any(token.lemma_=='apply' for token in doc):
        data['scraped_data']['application_forms'] = scrape_application_forms(soup)
        
    return data
    
def scrape_faqs(soup):
    faqs = []
    faq_sections = soup.find_all("section", {"id": "faq"})
    for section in faq_sections:
        questions = section.find_all("h2")
        answers = section.find_all("p")
        for q, a in zip(questions, answers):
            faqs.append({"question": q.get_text(), "answer": a.get_text()})
    return faqs
    
def scrape_pricing(soup):
    pricing = []
    price_sections = soup.find_all("section", {"class": "pricing"})
    for section in price_sections:
        price_items = section.find_all("div", class_="price-item")
        for item in price_items:
            name = item.find("h3").get_text()
            price = item.find("span", class_="price").get_text()
            pricing.append({"name": name, "price": price})
    return pricing
    
def scrape_application_forms(soup):
    forms = []
    form_links = soup.find_all("a", href=True, text="Apply")
    for link in form_links:
        forms.append({"application_form": urljoin(soup.base_url, link['href'])})
    return forms