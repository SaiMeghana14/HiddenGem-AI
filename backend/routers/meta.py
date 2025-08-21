from fastapi import APIRouter

router = APIRouter(prefix="/meta", tags=["meta"])

@router.get("/")
def meta_info():
    return {
        "app": "Travel Assistant Backend",
        "version": "1.0.0",
        "author": "Team HiddenGem",
        "description": "API backend serving travel recommendations, itineraries, and cultural insights."
    }
