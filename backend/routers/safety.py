from fastapi import APIRouter
from guides.safety import safety_summary, live_alerts

router = APIRouter()

@router.get("/summary")
def summary(city: str):
    return safety_summary(city)

@router.get("/alerts")
def alerts(city: str):
    return {"alerts": live_alerts(city)}
