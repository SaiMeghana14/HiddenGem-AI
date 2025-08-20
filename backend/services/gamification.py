import os, json
from typing import Dict, List

STORE = os.path.abspath(os.path.join(os.path.dirname(os.path.dirname(__file__)), "..", "badges.json"))

DEFAULT = {"visited": [], "upvotes": 0, "contributions": 0, "badges": []}

def _load() -> Dict:
    if os.path.exists(STORE):
        try:
            return json.load(open(STORE, encoding="utf-8"))
        except Exception:
            return DEFAULT.copy()
    return DEFAULT.copy()

def _save(data: Dict):
    json.dump(data, open(STORE, "w", encoding="utf-8"), indent=2)

def _grant(data: Dict):
    v = len(set(data["visited"]))
    if v >= 5 and "Explorer" not in data["badges"]:
        data["badges"].append("Explorer")
    if data["upvotes"] >= 10 and "Community Champ" not in data["badges"]:
        data["badges"].append("Community Champ")
    if data["contributions"] >= 3 and "Trailblazer" not in data["badges"]:
        data["badges"].append("Trailblazer")
    # Thematic badges by categories (best-effort heuristic)
    if v >= 2 and "Foodie" not in data["badges"]:
        data["badges"].append("Foodie")
    if v >= 2 and "Culture Vulture" not in data["badges"]:
        data["badges"].append("Culture Vulture")
    return data["badges"]

def add_visit(place_id: int) -> List[str]:
    data = _load()
    data["visited"].append(place_id)
    badges = _grant(data)
    _save(data)
    return badges

def add_upvote():
    data = _load()
    data["upvotes"] += 1
    _grant(data)
    _save(data)

def add_contribution(city: str):
    data = _load()
    data["contributions"] += 1
    _grant(data)
    _save(data)

def status() -> Dict:
    return _load()
