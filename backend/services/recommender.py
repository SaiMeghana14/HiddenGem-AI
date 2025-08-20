import csv, os, glob
from typing import List, Dict, Any, Optional

DATA_DIR = os.path.abspath(os.path.join(os.path.dirname(os.path.dirname(__file__)), "..", "data"))
# v1-compatible, no header: id,name,city,lat,lon,category,tag1,tag2,tag3,cost,rating,safety,sustainability,wheelchair,family_friendly,photogenic,hours,closed_days

def _files() -> List[str]:
    # Support multi-city: places_*.csv
    return sorted(glob.glob(os.path.join(DATA_DIR, "places_*.csv")))

def _parse(row: List[str]) -> Dict[str, Any]:
    return {
        "id": int(row[0]),
        "name": row[1],
        "city": row[2],
        "lat": float(row[3]),
        "lon": float(row[4]),
        "category": row[5],
        "tags": [row[6], row[7], row[8]],
        "cost": int(row[9]),
        "rating": float(row[10]),
        "safety": float(row[11]),
        "sustainability": bool(int(row[12])),
        "wheelchair": bool(int(row[13])),
        "family_friendly": bool(int(row[14])),
        "photogenic": bool(int(row[15])),
        "hours": row[16],
        "closed_days": row[17]
    }

def _load() -> List[Dict[str, Any]]:
    out: List[Dict[str, Any]] = []
    for f in _files():
        with open(f, encoding="utf-8") as fh:
            r = csv.reader(fh)
            for row in r:
                if not row or len(row) < 18:
                    continue
                out.append(_parse(row))
    return out

PLACES = _load()

def list_cities() -> List[str]:
    return sorted(list({p["city"] for p in PLACES}))

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
        items = [p for p in items if p["category"] in ["adventure","nature","photo"] or "hike" in p["tags"] or "kayak" in p["tags"]]
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
    items = sorted(items, key=lambda x: (x["rating"] + x["safety"] + (0.1 if x["photogenic"] else 0)), reverse=True)
    return items[:20]
