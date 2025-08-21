from fastapi import APIRouter
import random

router = APIRouter()

@router.get("/transport_options")
def transport_options(city: str = "Hyderabad"):
    options = [
        {"mode": "Metro", "avg_cost": 50},
        {"mode": "Bus", "avg_cost": 20},
        {"mode": "Auto Rickshaw", "avg_cost": 100},
        {"mode": "Cab", "avg_cost": 200},
    ]
    return {"city": city, "results": options}
