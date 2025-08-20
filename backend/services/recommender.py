import csv, os
from typing import List, Dict, Any, Optional
from haversine import haversine

DATA_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "..", "data", "places.csv")
DATA_PATH = os.path.abspath(DATA_PATH)

def _load():
    rows = []
    with open(DATA_PATH, encoding="utf-8") as f:
        r = csv.reader(f)
        for row in r:
            if not row: continue
            rows.append({
                "id": int(row[0]),
                "name": row[1],
                "city": row[2],
                "lat": float(row[3]),
                "lon": float(row[4]),
                "category": row[5],
                "tags": row[6].split(","),
                "cost": int(row[7]),
                "rating": float(row[8]),
                "safety": float(row[9]),
                "sustainability": bool(int(row[10])),
                "wheelchair": bool(int(row[11])),
                "family_friendly": bool(int(row[12])),
                "photogenic": bool(int(row[13])),
                "hours": row[14],
                "closed_days": row[15]
            })
    return rows

PLACES = _load()

def filter_by(city: str, category: Optional[str] = None, authentic: Optional[bool] = None) -> List[Dict[str, Any]]:
    items = [p for p in PLACES if p["city"].lower()==city.lower()]
    if category:
        items = [p for p in items if p["category"]==category]
    if authentic:
        items = [p for p in items if ("local" in p["tags"] or "authentic" in p["tags"])]
    return items

def recommend(city: str, mood: Optional[str], preferences: List[str], budget: Optional[int],
              solo_mode: bool, sustainability: bool) -> List[Dict[str, Any]]:
    items = [p for p in PLACES if p["city"].lower()==city.lower()]
    if preferences:
        items = [p for p in items if any(pref in p["tags"] or pref==p["category"] for pref in preferences)]
    if mood == "adventurous":
        items = [p for p in items if p["category"] in ["adventure","nature","photo"] or "hike" in p["tags"]]
    if mood == "calm":
        items = [p for p in items if "calm" in p["tags"] or p["category"] in ["nature","food"]]
    if mood == "foodie":
        items = [p for p in items if p["category"]=="food"]
    if mood == "nightlife":
        items = [p for p in items if p["category"]=="nightlife"]
    if mood == "culture":
        items = [p for p in items if p["category"]=="culture"]
    if budget is not None:
        items = [p for p in items if p["cost"] <= budget]
    if sustainability:
        items = [p for p in items if p["sustainability"]]
    if solo_mode:
        items = [p for p in items if p["safety"]>=0.75]
    # sort by rating + safety + photogenic bonus
    items = sorted(items, key=lambda x: (x["rating"] + x["safety"] + (0.1 if x["photogenic"] else 0)), reverse=True)
    return items[:20]
