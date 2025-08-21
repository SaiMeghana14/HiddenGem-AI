# backend/routers/facts.py
from fastapi import APIRouter
from guides.facts import quick_city_fact, landmark_fun_fact

router = APIRouter()

@router.get("/summary")
def city_summary(query: str):
    return {"fact": quick_city_fact(query)}

@router.get("/landmark")
def landmark(query: str):
    return {"fact": landmark_fun_fact(query)}
