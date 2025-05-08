import os
import json
import requests
from dotenv import load_dotenv

load_dotenv()
CORE_API_KEY = os.getenv("CORE_API_KEY")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

def core_search(query):
    """
    Searches CORE for academic literature related to the given query.
    Returns a JSON string with title, link, and description.
    """
    try:
        headers = {"Authorization": f"Bearer {CORE_API_KEY}"}
        params = {
            "q": query,
            "page": 1,
            "pageSize": 1
        }

        response = requests.get(
            "https://api.core.ac.uk/v3/search/works",
            headers=headers,
            params=params,
            timeout=10
        )
        response.raise_for_status()
        results = response.json().get("results", [])

        if not results:
            return json.dumps({
                "title": "No results found",
                "link": "",
                "description": f"No academic results for '{query}'"
            })

        doc = results[0]
        return json.dumps({
            "title": doc.get("title", "No title available"),
            "link": doc.get("url", "#"),
            "description": doc.get("description", "No abstract provided.")
        })

    except Exception as e:
        return json.dumps({
            "title": "CORE search failed",
            "link": "",
            "description": str(e)
        })

def tavily_search(query, max_results=3, search_depth="basic"):
    """
    Performs a web search using Tavily.
    Returns a JSON string with the top result’s title, link, and description.
    """
    try:
        headers = {
            "Authorization": f"Bearer {TAVILY_API_KEY}",
            "Content-Type": "application/json"
        }

        payload = {
            "query": query,
            "max_results": max_results,
            "search_depth": search_depth,
            "include_answer": True
        }

        response = requests.post(
            "https://api.tavily.com/search",
            headers=headers,
            json=payload,
            timeout=10
        )
        response.raise_for_status()
        data = response.json()

        if not data.get("results"):
            return json.dumps({
                "title": "No web results",
                "link": "",
                "description": f"No web articles found for '{query}'"
            })

        doc = data["results"][0]
        return json.dumps({
            "title": doc.get("title", "No title"),
            "link": doc.get("url", "#"),
            "description": doc.get("content", "No content preview.")
        })

    except Exception as e:
        return json.dumps({
            "title": "Tavily search failed",
            "link": "",
            "description": str(e)
        })
