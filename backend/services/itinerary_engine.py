from typing import List, Tuple, Dict, Any
from .recommender import PLACES
from haversine import haversine

def build_itinerary(city: str, days: int, budget_per_day: int, prefs: List[str], start: Tuple[float,float]) -> Dict[str, Any]:
    items = [p for p in PLACES if p["city"].lower()==city.lower() and p["cost"] <= budget_per_day]
    if prefs:
        items = [p for p in items if any(pref in p["tags"] or pref==p["category"] for pref in prefs)]
    items = sorted(items, key=lambda p: haversine(start, (p["lat"], p["lon"])))
    per_day = max(2, min(6, len(items)//max(1,days)))
    days_plan = []
    idx = 0
    for d in range(days):
        chunk = items[idx:idx+per_day]
        idx += per_day
        day_budget = sum(p["cost"] for p in chunk)
        day_plan = {
            "day": d+1,
            "stops": [{"id":p["id"], "name":p["name"], "lat":p["lat"], "lon":p["lon"], "category":p["category"], "cost":p["cost"]} for p in chunk],
            "est_budget": day_budget
        }
        days_plan.append(day_plan)
    return {"city": city, "days": days, "plan": days_plan, "notes":"Auto-generated route; optimize with live data if online."}

def dynamic_update(plan: Dict[str, Any], weather: str, closures: List[int]) -> Dict[str, Any]:
    for day in plan.get("plan", []):
        day["stops"] = [s for s in day["stops"] if s["id"] not in closures]
        if weather and ("rain" in weather.lower() or "storm" in weather.lower()):
            day["stops"] = [s for s in day["stops"] if s["category"] in ["food","culture","stay"]]
            day.setdefault("notes","")
            day["notes"] += " Weather suggests indoor activities."
    return plan
