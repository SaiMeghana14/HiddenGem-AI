from .recommender import PLACES
import random

def score_place(place_id: int):
    for p in PLACES:
        if p["id"] == place_id:
            # combine stored safety with small randomness for demo
            return round(min(1.0, max(0.0, p["safety"] + random.uniform(-0.05,0.05))), 2)
    return 0.7

def city_alerts(city: str):
    # demo alerts
    return [
        {"type":"info","msg":"Crowded near Charminar during evenings."},
        {"type":"advisory","msg":"Carry water for morning hikes; rocky terrain."}
    ]
