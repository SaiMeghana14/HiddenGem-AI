from fastapi import APIRouter, Query
from data import attractions, food, events
import random

router = APIRouter(prefix="/itinerary", tags=["itinerary"])

@router.get("/")
def generate_itinerary(city: str = Query(...), days: int = 2):
    atts = [a for a in attractions.get_attractions() if a["city"].lower() == city.lower()]
    foods = [f for f in food.get_food() if f["city"].lower() == city.lower()]
    evs = [e for e in events.get_events() if e["city"].lower() == city.lower()]

    plan = []
    for d in range(days):
        day_plan = {
            "day": d + 1,
            "morning": random.choice(atts) if atts else None,
            "afternoon": random.choice(evs) if evs else None,
            "evening": random.choice(foods) if foods else None,
        }
        plan.append(day_plan)
    return {"city": city, "days": days, "plan": plan}
