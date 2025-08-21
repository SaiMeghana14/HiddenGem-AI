from fastapi import APIRouter, Query
from data import attractions, stays, food, events
import random

router = APIRouter(prefix="/recommend", tags=["recommendations"])

@router.get("/attractions")
def recommend_attractions(city: str = Query(..., description="City name")):
    items = [a for a in attractions.get_attractions() if a["city"].lower() == city.lower()]
    return random.sample(items, min(3, len(items))) if items else []

@router.get("/stays")
def recommend_stays(city: str):
    items = [s for s in stays.get_stays() if s["city"].lower() == city.lower()]
    return random.sample(items, min(3, len(items))) if items else []

@router.get("/food")
def recommend_food(city: str):
    items = [f for f in food.get_food() if f["city"].lower() == city.lower()]
    return random.sample(items, min(3, len(items))) if items else []

@router.get("/events")
def recommend_events(city: str):
    items = [e for e in events.get_events() if e["city"].lower() == city.lower()]
    return random.sample(items, min(3, len(items))) if items else []
