from fastapi import APIRouter, Query
from typing import List, Optional
from ..services import recommender, nlp

router = APIRouter()

@router.get("/hidden_gems")
def hidden_gems(city: str = "Hyderabad",
                mood: Optional[str] = None,
                preferences: Optional[List[str]] = Query(default=[]),
                budget_per_day: Optional[int] = None,
                solo_mode: bool = False,
                sustainability: bool = False):
    items = recommender.recommend(city=city, mood=mood, preferences=preferences,
                                  budget=budget_per_day, solo_mode=solo_mode,
                                  sustainability=sustainability)
    return {"city": city, "count": len(items), "items": items}

@router.get("/mood")
def detect_mood(q: str):
    mood = nlp.detect_mood(q)
    intents = nlp.detect_intents(q)
    return {"mood": mood, "intents": intents}
