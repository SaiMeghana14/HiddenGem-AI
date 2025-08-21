from __future__ import annotations
from pathlib import Path
from functools import lru_cache
import os
import pandas as pd
from typing import Dict, Any

def _dd():
    env = os.getenv("HIDDENGEM_DATA_DIR")
    if env and Path(env).exists(): return Path(env)
    here = Path(__file__).resolve()
    for p in [here.parent.parent/"data", here.parent/"data", Path.cwd()/"data"]:
        if p.exists(): return p
    return Path("data")

DATA_DIR = _dd()
CITIES_CSV = DATA_DIR / "cities.csv"
ATTRACTIONS_CSV = DATA_DIR / "attractions.csv"
EVENTS_CSV = DATA_DIR / "events.csv"

@lru_cache(maxsize=1)
def _cities() -> pd.DataFrame:
    try: return pd.read_csv(CITIES_CSV)
    except Exception: return pd.DataFrame(columns=["city","state","region","population","notes"])

@lru_cache(maxsize=1)
def _attractions() -> pd.DataFrame:
    try: return pd.read_csv(ATTRACTIONS_CSV)
    except Exception: return pd.DataFrame(columns=["city","name","type","description","lat","lon","tags","photogenic"])

@lru_cache(maxsize=1)
def _events() -> pd.DataFrame:
    try: return pd.read_csv(EVENTS_CSV)
    except Exception: return pd.DataFrame(columns=["city","title","when","price","tags"])

def quick_city_fact(city: str) -> str:
    c = _cities()
    if c.empty: return "No city data available."
    row = c[c["city"].str.lower()==city.lower()].head(1)
    if row.empty: return f"No facts for {city}."
    bits = []
    if "state" in row: bits.append(f"{row.iloc[0].get('city')} is in {row.iloc[0].get('state')}.")
    if "population" in row and pd.notna(row.iloc[0].get("population")):
        bits.append(f"Approx. population: {int(row.iloc[0]['population']):,}.")
    if "notes" in row and pd.notna(row.iloc[0].get("notes")):
        bits.append(str(row.iloc[0]["notes"]))
    # add a notable attraction
    a = _attractions()
    sample = a[a["city"].str.lower()==city.lower()].head(1)
    if not sample.empty:
        bits.append(f"Notable spot: {sample.iloc[0].get('name')} ({sample.iloc[0].get('type')}).")
    # add an event
    e = _events()
    ev = e[e["city"].str.lower()==city.lower()].head(1)
    if not ev.empty:
        bits.append(f"Upcoming event: {ev.iloc[0].get('title')} — {ev.iloc[0].get('when')}.")
    return " ".join(bits) if bits else f"{city} is a vibrant destination."

def landmark_fun_fact(query: str) -> str:
    a = _attractions()
    if a.empty: return "No attractions data available."
    row = a[a["name"].str.lower()==query.lower()].head(1)
    if row.empty:
        # try contains
        row = a[a["name"].str.lower().str.contains(query.lower())].head(1)
    if row.empty: return "No facts found. Try another landmark."
    desc = row.iloc[0].get("description") or "A notable local spot."
    city = row.iloc[0].get("city")
    t = row.iloc[0].get("type")
    return f"{query} in {city} is a {t}. {desc}"
