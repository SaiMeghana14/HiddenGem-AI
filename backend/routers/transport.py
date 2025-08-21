from __future__ import annotations
import math
from typing import Dict, Any, List

def _haversine_km(lat1, lon1, lat2, lon2):
    R = 6371.0
    dlat = math.radians(lat2-lat1); dlon = math.radians(lon2-lon1)
    a = math.sin(dlat/2)**2 + math.cos(math.radians(lat1))*math.cos(math.radians(lat2))*math.sin(dlon/2)**2
    return 2*R*math.asin(min(1, math.sqrt(a)))

def eta_minutes(distance_km: float, mode: str="walk") -> int:
    speeds = {"walk": 4.5, "bike": 15, "car": 30, "transit": 22}  # km/h demo
    v = speeds.get(mode, 4.5)
    mins = (distance_km / v) * 60.0
    return max(1, int(round(mins)))

def route_polyline_stub(start_lat: float, start_lon: float, end_lat: float, end_lon: float) -> List[Dict[str, float]]:
    # straight-line demo polyline with midpoints
    mid1 = ((2*start_lat + end_lat)/3, (2*start_lon + end_lon)/3)
    mid2 = ((start_lat + 2*end_lat)/3, (start_lon + 2*end_lon)/3)
    return [
        {"lat": start_lat, "lon": start_lon},
        {"lat": mid1[0], "lon": mid1[1]},
        {"lat": mid2[0], "lon": mid2[1]},
        {"lat": end_lat, "lon": end_lon},
    ]

def compute_route(start_lat: float, start_lon: float, end_lat: float, end_lon: float, mode: str="walk") -> Dict[str, Any]:
    d = _haversine_km(start_lat, start_lon, end_lat, end_lon)
    return {
        "distance_km": round(d, 2),
        "mode": mode,
        "eta_min": eta_minutes(d, mode),
        "polyline": route_polyline_stub(start_lat, start_lon, end_lat, end_lon)
    }
