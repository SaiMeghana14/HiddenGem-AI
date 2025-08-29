from fastapi import APIRouter

router = APIRouter()

@router.get("/safety_tips")
def safety_tips(city: str = "Hyderabad"):
    tips = [
        "Avoid isolated areas at night.",
        "Keep your belongings safe.",
        "Use registered transport services.",
        "Respect local culture and traditions."
    ]
    return {"city": city, "results": tips}

@router.get("/alerts")
def get_alerts(city: str):
    return {
        "city": city,
        "alerts": [
            {"type": "Weather", "message": "Heavy rain expected today."},
            {"type": "Health", "message": "Carry mosquito repellent."}
        ]
    }
