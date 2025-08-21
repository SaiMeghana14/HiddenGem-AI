from fastapi import APIRouter
from guides.meta import cities, city_guide_text

router = APIRouter()

@router.get("/cities")
def list_cities():
    return {"cities": cities()}

@router.get("/guide")
def guide(city: str):
    return {"guide": city_guide_text(city)}
