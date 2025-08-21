from fastapi import APIRouter, Query
from data import food

router = APIRouter(prefix="/culture", tags=["culture-food"])

@router.get("/food")
def get_food_by_city(city: str = Query(...)):
    return [f for f in food.get_food() if f["city"].lower() == city.lower()]

@router.get("/dish")
def get_dish_info(dish: str = Query(...)):
    items = [f for f in food.get_food() if dish.lower() in f["dish"].lower()]
    return items if items else {"message": "Dish not found"}
