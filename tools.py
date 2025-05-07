import json

def core_search(query):
    return json.dumps({
        "title": f"Academic result for {query}",
        "link": f"https://core.ac.uk/search?q={query}",
        "description": f"Example academic article discussing {query}."
    })

def web_search(query):
    return json.dumps({
        "title": f"Web article for {query}",
        "link": f"https://example.com?q={query}",
        "description": f"Example web content about {query}."
    })
