from pydantic import BaseModel


class ScrapeRequest(BaseModel):
    url: str
    instructions: str
    use_selenium: bool = False