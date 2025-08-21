from fastapi import APIRouter
from data import transport

router = APIRouter()

@router.get("/route")
def get_route(
    start_lat: float, start_lon: float, 
    end_lat: float, end_lon: float, 
    mode: str = "walk"
):
    return transport.compute_route(start_lat, start_lon, end_lat, end_lon, mode)
