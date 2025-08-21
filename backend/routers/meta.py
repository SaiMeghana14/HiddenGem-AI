from fastapi import APIRouter

router = APIRouter()

@router.get("/health")
def health_check():
    return {"status": "ok", "service": "Travel Assistant API"}

@router.get("/about")
def about():
    return {
        "project": "Travel Assistant",
        "version": "1.0",
        "description": "Smart travel assistant with recommendations, bookings, and cultural insights."
    }
