from fastapi import APIRouter, Query
import pandas as pd
import random
import os

router = APIRouter()

DATA_DIR = os.path.join(os.path.dirname(__file__), "../../data")
CITIES_CSV = os.path.join(DATA_DIR, "cities.csv")
ATTRACTIONS_CSV = os.path.join(DATA_DIR, "attractions.csv")

def safe_load_csv(path):
    try:
        return pd.read_csv(path)
    except Exception as e:
        print(f"⚠️ Error loading {path}: {e}")
        return pd.DataFrame()

cities_df = safe_load_csv(CITIES_CSV)
attractions_df = safe_load_csv(ATTRACTIONS_CSV)

@router.get("/recommend_city")
def recommend_city(region: str = "India", budget: int = 2000):
    if not cities_df.empty:
        filtered = cities_df[cities_df["region"].str.lower() == region.lower()]
        if not filtered.empty:
            return {"region": region, "results": filtered.to_dict(orient="records")}

    fallback = [
        {"city": "Hyderabad", "region": "India", "budget": 1500},
        {"city": "Delhi", "region": "India", "budget": 2000},
        {"city": "Mumbai", "region": "India", "budget": 2500},
    ]
    return {"region": region, "results": fallback}

@router.get("/recommend_attractions")
def recommend_attractions(city: str = "Hyderabad"):
    if not attractions_df.empty:
        city_atts = attractions_df[attractions_df["city"].str.lower() == city.lower()]
        if not city_atts.empty:
            return {"city": city, "results": city_atts.to_dict(orient="records")}

    fallback = [
        {"name": f"{city} Fort", "type": "Historic", "rating": 4.5},
        {"name": f"{city} Lake", "type": "Nature", "rating": 4.3},
        {"name": f"{city} Museum", "type": "Cultural", "rating": 4.1},
    ]
    return {"city": city, "results": fallback}

@router.get("/hidden_gems")
def hidden_gems(city: str, budget_per_day: int, solo_mode: bool = False, sustainability: bool = False,
                family: bool = False, accessible: bool = False):
    return {
        "city": city,
        "budget": budget_per_day,
        "filters": {
            "solo": solo_mode,
            "sustainability": sustainability,
            "family": family,
            "accessible": accessible,
        },
        "recommendations": ["Place A", "Place B", "Place C"]
    }

@router.get("/mood")
def recommend_by_mood(q: str):
    # Mocked recommendations based on mood
    if q.lower() == "adventurous":
        recs = ["Trekking at Ananthagiri Hills", "Kayaking at Hussain Sagar"]
    elif q.lower() == "relax":
        recs = ["Charminar evening lights", "Necklace Road sunset walk"]
    else:
        recs = ["Explore local markets", "Try street food tour"]

    return {"recommendations": recs}
