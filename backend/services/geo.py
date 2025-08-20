from typing import Tuple, List
from haversine import haversine

def simple_route(start: Tuple[float,float], end: Tuple[float,float], mode: str = "walk"):
    # dummy polyline as straight line with two points
    dist_km = haversine(start, end)
    speed_kmh = {"walk": 4, "bike": 12, "transit": 25, "car": 30}.get(mode, 4)
    eta_min = round((dist_km / speed_kmh) * 60, 1)
    path = [start, end]
    return path, round(dist_km, 2), eta_min
