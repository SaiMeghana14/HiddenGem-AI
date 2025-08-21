from __future__ import annotations
from pathlib import Path
from functools import lru_cache
import os, re, pandas as pd
from typing import List, Dict, Any, Tuple

def _dd() -> Path:
    env = os.getenv("HIDDENGEM_DATA_DIR")
    if env and Path(env).exists(): return Path(env)
    here = Path(__file__).resolve()
    for p in [here.parent.parent/"data", here.parent/"data", Path.cwd()/"data"]:
        if p.exists(): return p
    return Path("data")

DATA_DIR = _dd()
ATTRACTIONS_CSV = DATA_DIR / "attractions.csv"

@lru_cache(maxsize=1)
def _attr() -> pd.DataFrame:
    try:
        df = pd.read_csv(ATTRACTIONS_CSV)
        # expected cols: city,name,type,cost,lat,lon,tags,rating,safety,sustainability,photogenic
        for col in ["rating","safety"]:
            if col in df: df[col] = pd.to_numeric(df[col], errors="coerce")
        if "sustainability" in df: df["sustainability"] = df["sustainability"].astype(bool)
        if "photogenic" in df: df["photogenic"] = df["photogenic"].astype(bool)
        return df
    except Exception:
        return pd.DataFrame(columns=["city","name","type","cost","lat","lon","tags","rating","safety","sustainability","photogenic"])

def _score_item(row: pd.Series, prefs: List[str], mood: str|None, solo: bool, sustain: bool, family: bool, accessible: bool, budget: int) -> float:
    score = 0.0
    tags = str(row.get("tags","")).lower()
    # preference match
    for p in prefs:
        if re.search(rf"\b{re.escape(p.lower())}\b", tags): score += 2.0
    # mood nudges
    if mood:
        if mood.lower() in tags: score += 1.5
        if mood.lower()=="adventurous" and ("hike" in tags or "trek" in tags or "adventure" in tags): score += 2.0
        if mood.lower()=="calm" and ("calm" in tags or "spa" in tags or "quiet" in tags or "beach" in tags): score += 2.0
    # budget affinity (prefer items under 40% of day budget for variety)
    cost = float(row.get("cost", 200) or 200)
    if cost <= max(100, 0.4*budget): score += 1.0
    # sustainability
    if sustain and bool(row.get("sustainability", False)): score += 1.0
    # safety / solo
    safety = float(row.get("safety", 3) or 3)
    if solo and safety >= 3.5: score += 1.2
    if family and "family" in tags: score += 1.0
    if accessible and ("wheelchair" in tags or "accessible" in tags): score += 1.0
    # quality rating
    rating = float(row.get("rating", 4) or 4)
    score += rating * 0.3
    # photogenic bonus if user likes photos
    if "photo" in [p.lower() for p in prefs] and bool(row.get("photogenic", False)): score += 1.0
    return score

def detect_mood_and_intents(text: str) -> Tuple[str|None, List[str]]:
    if not text or not text.strip(): return None, []
    t = text.lower()
    mood = None
    if any(k in t for k in ["adventure","adventurous","thrill","hike","trek"]): mood = "adventurous"
    elif any(k in t for k in ["calm","relax","chill","peace"]): mood = "calm"
    elif any(k in t for k in ["party","nightlife","club"]): mood = "party"
    intents = []
    if "food" in t or "eat" in t: intents.append("food")
    if "history" in t or "museum" in t: intents.append("history")
    if "photo" in t or "instagram" in t: intents.append("photo")
    if "nature" in t or "park" in t: intents.append("nature")
    return mood, intents

def recommend_hidden_gems(city: str, budget_per_day: int=1000, preferences: List[str]|None=None,
                          mood: str|None=None, solo_mode: bool=False, sustainability: bool=False,
                          family: bool=False, accessible: bool=False, limit: int=20) -> List[Dict[str, Any]]:
    preferences = preferences or []
    df = _attr()
    if df.empty: return []
    q = df[df["city"].str.lower()==city.lower()].copy()
    if q.empty: return []
    # score and sort
    q["__score"] = q.apply(lambda r: _score_item(r, preferences, mood, solo_mode, sustainability, family, accessible, budget_per_day), axis=1)
    q = q.sort_values(by="__score", ascending=False).head(limit)
    # normalize for frontend
    out = []
    for _, r in q.iterrows():
        out.append({
            "name": r.get("name"),
            "category": r.get("type","spot"),
            "cost": int(r.get("cost", 200) or 200),
            "rating": float(r.get("rating", 4) or 4),
            "safety": float(r.get("safety", 3) or 3),
            "sustainability": bool(r.get("sustainability", False)),
            "lat": float(r.get("lat", 0.0) or 0.0),
            "lon": float(r.get("lon", 0.0) or 0.0),
            "photogenic": bool(r.get("photogenic", False)),
            "tags": r.get("tags","")
        })
    return out
