# backend/routers/culture_food.py
from fastapi import APIRouter
from guides.culture_food import food_spots, cultural_experiences

router = APIRouter()

@router.get("/food_spots")
def food(city: str, authentic: bool = True):
    return {"items": food_spots(city, authentic)}

@router.get("/cultural")
def cultural(city: str):
    return {"items": cultural_experiences(city)}
