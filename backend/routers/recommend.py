from fastapi import APIRouter, Query
from guides.recommend import recommend_hidden_gems, detect_mood_and_intents

router = APIRouter()

@router.get("/hidden_gems")
def hidden_gems(city: str, budget_per_day: int = 1000,
                preferences: list[str] = Query(default=[]),
                mood: str | None = None, solo_mode: bool=False,
                sustainability: bool=False, family: bool=False, accessible: bool=False):
    items = recommend_hidden_gems(city, budget_per_day, preferences, mood, solo_mode, sustainability, family, accessible)
    return {"items": items}

@router.get("/mood")
def mood_detect(q: str = ""):
    mood, intents = detect_mood_and_intents(q)
    return {"mood": mood, "intents": intents}
