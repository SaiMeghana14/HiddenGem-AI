from fastapi import APIRouter, HTTPException
from typing import Optional
from ..services import utils, gamification

router = APIRouter()

@router.post("/submit")
def submit(name: str, city: str, lat: float, lon: float, category: str, tags: str, notes: Optional[str] = ""):
    pid = utils.add_community_place(name, city, lat, lon, category, tags, notes or "")
    # Gamification: reward contributor badge (simple demo)
    gamification.add_contribution(city)
    return {"id": pid, "status": "submitted"}

@router.post("/vote")
def vote(place_id: int, up: bool = True):
    ok = utils.vote_place(place_id, 1 if up else -1)
    if not ok:
        raise HTTPException(404, "place not found")
    if up:
        gamification.add_upvote()
    return {"place_id": place_id, "delta": 1 if up else -1}

@router.get("/list")
def list_places(city: str = "Hyderabad"):
    return {"items": utils.list_community_places(city)}

@router.post("/visit")
def visit(place_id: int):
    ok = utils.exists_place(place_id)
    if not ok:
        raise HTTPException(404, "place not found")
    badges = gamification.add_visit(place_id)
    return {"place_id": place_id, "badges": badges}
