from fastapi import APIRouter

router = APIRouter(prefix="/safety", tags=["safety"])

safety_tips = [
    "Keep your belongings secure in crowded areas.",
    "Avoid isolated places late at night.",
    "Use only licensed taxis or ride-sharing apps.",
    "Stay hydrated and beware of heat in summers.",
    "Respect local customs and dress codes."
]

@router.get("/tips")
def get_safety_tips():
    return safety_tips
