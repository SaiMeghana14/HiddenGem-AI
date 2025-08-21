from fastapi import APIRouter, Query
from data import cities
import random

router = APIRouter(prefix="/facts", tags=["facts"])

@router.get("/city")
def city_fact(city: str = Query(...)):
    facts = [c for c in cities.get_cities() if c["city"].lower() == city.lower()]
    return random.choice(facts)["fact"] if facts else {"message": "No fact found"}
