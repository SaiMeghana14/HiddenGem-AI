from fastapi import APIRouter
from ..services import recommender

router = APIRouter()

@router.get("/cities")
def cities():
    return {"cities": recommender.list_cities()}
