import requests

def wikipedia_summary(query: str) -> str:
    try:
        # Simple REST summary
        url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{requests.utils.quote(query)}"
        r = requests.get(url, timeout=6)
        if r.status_code == 200:
            data = r.json()
            return data.get("extract") or "No summary available."
        return "No summary available."
    except Exception:
        return "No summary available."
