from fastapi import APIRouter
from ..services import recommender

router = APIRouter()

@router.get("/food_spots")
def food_spots(city: str = "Hyderabad", authentic: bool = True):
    return {"items": recommender.filter_by(city, category="food", authentic=authentic)}

@router.get("/cultural")
def cultural(city: str = "Hyderabad"):
    return {"items": recommender.filter_by(city, category="culture")}
