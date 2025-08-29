from fastapi import APIRouter
import random

router = APIRouter()

@router.get("/culture")
def get_culture(city: str = "Hyderabad"):
    mock_culture = [
        {"aspect": "Festival", "detail": "Diwali celebrations"},
        {"aspect": "Clothing", "detail": "Traditional sarees & sherwanis"},
        {"aspect": "Language", "detail": "Telugu, Urdu, Hindi, English"},
    ]
    return {"city": city, "results": mock_culture}

@router.get("/food")
def get_food(city: str = "Hyderabad"):
    mock_food = [
        {"dish": "Biryani", "price": 250},
        {"dish": "Haleem", "price": 200},
        {"dish": "Irani Chai", "price": 50},
    ]
    return {"city": city, "results": mock_food}

@router.get("/food_spots")
def food_spots(city: str, authentic: bool = True):
    return {
        "city": city,
        "authentic": authentic,
        "spots": [
            {"name": "Spicy Andhra Mess", "type": "local", "rating": 4.7},
            {"name": "Old City Biryani House", "type": "local", "rating": 4.8}
        ]
    }

@router.get("/cultural")
def cultural(city: str):
    return {
        "city": city,
        "events": [
            {"name": "Classical Dance Festival", "date": "2025-08-30"},
            {"name": "Crafts Fair", "date": "2025-09-05"}
        ]
    }
