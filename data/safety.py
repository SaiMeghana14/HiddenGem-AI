# guides/safety.py
from __future__ import annotations
from pathlib import Path
from functools import lru_cache
import os, random, pandas as pd
from typing import List, Dict, Any

def _dd() -> Path:
    env = os.getenv("HIDDENGEM_DATA_DIR")
    if env and Path(env).exists(): return Path(env)
    here = Path(__file__).resolve()
    for p in [here.parent.parent/"data", here.parent/"data", Path.cwd()/"data"]:
        if p.exists(): return p
    return Path("data")

DATA_DIR = _dd()
CITIES_CSV = DATA_DIR / "cities.csv"
EVENTS_CSV = DATA_DIR / "events.csv"

@lru_cache(maxsize=1)
def _cities() -> pd.DataFrame:
    try: return pd.read_csv(CITIES_CSV)
    except Exception: return pd.DataFrame(columns=["city","state","safety_rating"])

@lru_cache(maxsize=1)
def _events() -> pd.DataFrame:
    try: return pd.read_csv(EVENTS_CSV)
    except Exception: return pd.DataFrame(columns=["city","title","when","price","tags"])

def safety_summary(city: str) -> Dict[str, Any]:
    c = _cities()
    base = {"city": city, "rating": 3.0, "wheelchair_accessible": True, "family_safe": True}
    if not c.empty:
        row = c[c["city"].str.lower()==city.lower()].head(1)
        if not row.empty:
            base["rating"] = float(row.iloc[0].get("safety_rating", 3.0) or 3.0)
    return base

def live_alerts(city: str) -> List[Dict[str, str]]:
    # demo alerts: crowd near events; weather etc can be added later
    e = _events()
    out: List[Dict[str,str]] = []
    if not e.empty:
        evs = e[e["city"].str.lower()==city.lower()].head(2)
        for _, r in evs.iterrows():
            out.append({"type":"crowd", "msg": f"High footfall expected near '{r['title']}' ({r['when']})."})
    # occasional generic alert
    if random.random() < 0.2:
        out.append({"type":"advisory", "msg":"Stay hydrated and keep valuables secure in crowded areas."})
    return out
