from fastapi import APIRouter, Query
import pandas as pd
import random
import os

router = APIRouter()

# Paths to CSV files (adjust if needed)
DATA_DIR = os.path.join(os.path.dirname(__file__), "../../data")
CITIES_CSV = os.path.join(DATA_DIR, "cities.csv")
ATTRACTIONS_CSV = os.path.join(DATA_DIR, "attractions.csv")
FOOD_CSV = os.path.join(DATA_DIR, "food.csv")
PHRASEBOOK_CSV = os.path.join(DATA_DIR, "phrasebook.csv")
STAYS_CSV = os.path.join(DATA_DIR, "stays.csv")
EVENTS_CSV = os.path.join(DATA_DIR, "events.csv")

# Load datasets
def safe_load_csv(path):
    try:
        return pd.read_csv(path)
    except Exception as e:
        print(f"⚠️ Error loading {path}: {e}")
        return pd.DataFrame()

cities_df = safe_load_csv(CITIES_CSV)
attractions_df = safe_load_csv(ATTRACTIONS_CSV)
food_df = safe_load_csv(FOOD_CSV)
phrasebook_df = safe_load_csv(PHRASEBOOK_CSV)
stays_df = safe_load_csv(STAYS_CSV)
events_df = safe_load_csv(EVENTS_CSV)


@router.get("/search_stay")
def search_stay(city: str = "Hyderabad", budget: int = 1500):
    """
    Returns stays/hotels based on city and budget.
    Uses stays.csv, falls back to mock if not found.
    """
    if not stays_df.empty:
        city_stays = stays_df[
            (stays_df["city"].str.lower() == city.lower()) &
            (stays_df["price"] <= budget)
        ]
        results = city_stays.to_dict(orient="records")
        if results:
            return {"city": city, "results": results}

    # fallback mock
    stays = [
        {"name": f"{city} Budget Inn", "price": max(300, budget // 3), "url": "#"},
        {"name": f"{city} Heritage Homestay", "price": budget, "url": "#"},
        {"name": f"{city} Luxury Suites", "price": budget * 2, "url": "#"},
    ]
    return {"city": city, "results": stays}


@router.get("/search_events")
def search_events(city: str = "Hyderabad"):
    """
    Returns events for a city.
    Uses events.csv, falls back to attractions.csv.
    """
    if not events_df.empty:
        city_events = events_df[events_df["city"].str.lower() == city.lower()]
        results = city_events.to_dict(orient="records")
        if results:
            return {"city": city, "results": results}

    # fallback: attractions as events
    city_attractions = attractions_df[attractions_df["city"] == city]
    results = []
    for _, row in city_attractions.iterrows():
        results.append({
            "title": row["name"],
            "type": row.get("type", "Event/Attraction"),
            "price": random.choice([0, 200, 300, 500]),
            "description": row.get("description", ""),
        })
    return {"city": city, "results": results}


@router.get("/search_food")
def search_food(city: str = "Hyderabad"):
    """
    Returns popular foods for a city.
    Uses food.csv
    """
    city_food = food_df[food_df["city"] == city]

    if city_food.empty:
        return {"city": city, "results": []}

    results = []
    for _, row in city_food.iterrows():
        results.append({
            "dish": row["dish"],
            "description": row.get("description", ""),
            "price": random.choice([100, 150, 200, 250]),
        })
    return {"city": city, "results": results}


@router.get("/phrasebook")
def phrasebook(language: str = "Hindi"):
    """
    Returns travel phrasebook for a language.
    Uses phrasebook.csv
    """
    lang_phrases = phrasebook_df[phrasebook_df["language"] == language]

    if lang_phrases.empty:
        return {"language": language, "results": []}

    results = []
    for _, row in lang_phrases.iterrows():
        results.append({
            "english": row["english"],
            "translation": row["translation"],
        })
    return {"language": language, "results": results}
