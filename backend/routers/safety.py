from fastapi import APIRouter
from ..services import safety_model

router = APIRouter()

@router.get("/score")
def score(place_id: int):
    return {"place_id": place_id, "safety": safety_model.score_place(place_id)}

@router.get("/alerts")
def alerts(city: str = "Hyderabad"):
    return {"city": city, "alerts": safety_model.city_alerts(city)}
