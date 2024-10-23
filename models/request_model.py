from pydantic import BaseModel


class ScrapeRequest(BaseModel):
    url: str
    prompt: str
    instructions: str = "Scrape relevant information from the website"
    use_selenium: bool = False