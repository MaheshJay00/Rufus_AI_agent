import os

from fastapi import FastAPI, HTTPException
from models.request_model import ScrapeRequest
from rufus_client import RufusClient

app = FastAPI()

key = 'your-api-key'
client = RufusClient(api_key=key)

@app.post('/scrape/')
def scrape_website(request: ScrapeRequest):
    try: 
        result = client.scrape(request.url,request.instructions,request.use_selenium)
        if result:
            return result
        else:
            raise HTTPException(status_code=500,detail='Failed to scrape the website.')
    except Exception as e:
        raise HTTPException(status_code=500,detail=f"Error occurred: {str(e)}")
    
@app.get("/")
def root():
    return {"message": "Welcome to the Rufus AI Agent API!"}

