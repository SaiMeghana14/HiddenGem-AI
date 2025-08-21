from fastapi import APIRouter, Query
from guides.itinerary import build_itinerary

router = APIRouter()

@router.post("/plan")
def plan(city: str, days: int = 2, budget_per_day: int = 1000, preferences: list[str] = Query(default=[])):
    return build_itinerary(city, days, budget_per_day, preferences)
