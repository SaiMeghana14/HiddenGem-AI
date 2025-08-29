from fastapi import APIRouter
import random

router = APIRouter()

@router.get("/generate_itinerary")
def generate_itinerary(city: str = "Hyderabad", days: int = 2):
    mock_places = [
        f"{city} Fort", f"{city} Museum", f"{city} Lake",
        f"{city} Market", f"{city} Garden"
    ]
    itinerary = {}
    for d in range(1, days+1):
        itinerary[f"Day {d}"] = random.sample(mock_places, k=min(2, len(mock_places)))
    return {"city": city, "days": days, "plan": itinerary}

@router.get("/plan")
def plan_itinerary(city: str, days: int, budget_per_day: int):
    # Dummy sample plan
    plan = []
    for d in range(1, days + 1):
        plan.append({
            "day": d,
            "activities": [
                f"Explore highlights of {city} (Day {d})",
                f"Enjoy local food (Budget: ₹{budget_per_day})"
            ]
        })
    return {"plan": plan}
