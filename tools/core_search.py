
import requests
import os
from dotenv import load_dotenv
load_dotenv()

CORE_API_KEY = os.getenv("CORE_API_KEY")

def search_core(query, limit=5):
    url = f"https://core.ac.uk:443/api-v2/search/{query}"
    params = {
        "apiKey": CORE_API_KEY,
        "page": 1,
        "pageSize": limit
    }
    r = requests.get(url, params=params)
    if r.status_code == 200:
        return [
            {
                "title": doc.get("title"),
                "authors": doc.get("authors"),
                "year": doc.get("publishedDate", "")[:4],
                "url": doc.get("fullTextLink"),
                "summary": doc.get("description")
            }
            for doc in r.json().get("data", [])
        ]
    return []
