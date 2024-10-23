from utils.scraper import Scraper
if __name__ == "__main__":
    url = "https://www.uta.edu/"
    prompt = "Extract all links and headings"

    # Fetch the page content and determine whether it's JSON or HTML
    content, content_type = fetch_page_content(url, dynamic=False)

    if content_type == 'json':
        # Interpret the prompt and extract relevant data from the JSON
        results = interpret_json(content, prompt)
    elif content_type == 'html':
        # Use the AI-driven NLP model to interpret the prompt
        instruction = interpret_prompt(prompt)

        # Perform selective scraping based on the interpreted instruction
        results = selective_scrape(content, instruction)

    # Print or save the results
    print("Extracted Data:", results)
