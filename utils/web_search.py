# great-ideas/utils/web_search.py
import os
import requests
from dotenv import load_dotenv

load_dotenv()

def web_search(query, num_results=5):
    api_key = os.getenv("SERPAPI_API_KEY")
    url = "https://serpapi.com/search.json"
    
    params = {
        "q": query,
        "api_key": api_key,
        "num": num_results
    }
    
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        results = response.json().get("organic_results", [])
        return [{"title": r["title"], "snippet": r["snippet"], "link": r["link"]} for r in results]
    else:
        return []