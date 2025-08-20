import os, requests, random
from .recommender import PLACES

OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")

def score_place(place_id: int):
    for p in PLACES:
        if p["id"] == place_id:
            return round(min(1.0, max(0.0, p["safety"] + random.uniform(-0.05,0.05))), 2)
    return 0.7

def _owm_alerts(lat: float, lon: float):
    if not OPENWEATHER_API_KEY:
        return []
    try:
        url = f"https://api.openweathermap.org/data/3.0/onecall?lat={lat}&lon={lon}&appid={OPENWEATHER_API_KEY}"
        r = requests.get(url, timeout=6)
        data = r.json()
        alerts = data.get("alerts", [])
        out = [{"type":"weather", "msg": a.get("event", "Weather alert")} for a in alerts]
        return out
    except Exception:
        return []

def city_alerts(city: str):
    # Demo baseline alerts (existing behavior)
    base = [
        {"type":"info","msg":"Crowded near Charminar during evenings."},
        {"type":"advisory","msg":"Carry water for morning hikes; rocky terrain."}
    ]
    # Try to enrich with one place's coords for weather alerts
    p = next((x for x in PLACES if x["city"].lower()==city.lower()), None)
    if p:
        return base + _owm_alerts(p["lat"], p["lon"])
    return base
