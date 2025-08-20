from fastapi import APIRouter
from typing import Optional, List
from ..services import itinerary_engine

router = APIRouter()

@router.post("/plan")
def plan(city: str = "Hyderabad",
         days: int = 2,
         budget_per_day: int = 500,
         preferences: Optional[List[str]] = None,
         start_lat: float = 17.3850, start_lon: float = 78.4867):
    plan = itinerary_engine.build_itinerary(city, days, budget_per_day, preferences or [], (start_lat, start_lon))
    return plan

@router.post("/update")
def update(plan: dict, weather: Optional[str] = None, closures: Optional[List[int]] = None):
    updated = itinerary_engine.dynamic_update(plan, weather=weather, closures=closures or [])
    return updated
