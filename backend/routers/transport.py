from fastapi import APIRouter, Query
from guides.transport import compute_route

router = APIRouter(prefix="/transport", tags=["transport"])

@router.get("/route")
def get_route(
    start_lat: float = Query(...),
    start_lon: float = Query(...),
    end_lat: float = Query(...),
    end_lon: float = Query(...),
    mode: str = Query("walk", enum=["walk", "bike", "car", "transit"])
):
    return compute_route(start_lat, start_lon, end_lat, end_lon, mode)
