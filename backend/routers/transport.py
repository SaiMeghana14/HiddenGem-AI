from fastapi import APIRouter
from ..services import geo

router = APIRouter()

@router.get("/route")
def route(start_lat: float, start_lon: float, end_lat: float, end_lon: float, mode: str = "walk"):
    path, dist_km, eta_min = geo.simple_route((start_lat, start_lon), (end_lat, end_lon), mode)
    return {"mode": mode, "distance_km": dist_km, "eta_min": eta_min, "polyline": path}
