from __future__ import annotations
import os
from pathlib import Path
from functools import lru_cache
import pandas as pd
from typing import Dict, List, Any

def _find_data_dir() -> Path:
    # try env var first
    env = os.getenv("HIDDENGEM_DATA_DIR")
    if env and Path(env).exists():
        return Path(env)
    # walk common relative locations
    here = Path(__file__).resolve()
    candidates = [
        here.parent.parent / "data",  # project_root/data
        here.parent / "data",         # guides/data
        here.parent.parent.parent / "data",  # backend/*/data
        Path.cwd() / "data",
    ]
    for c in candidates:
        if c.exists():
            return c
    return Path("data")

DATA_DIR = _find_data_dir()
CITIES_CSV = DATA_DIR / "cities.csv"
PHRASEBOOK_CSV = DATA_DIR / "phrasebook.csv"

@lru_cache(maxsize=1)
def _cities_df() -> pd.DataFrame:
    try:
        df = pd.read_csv(CITIES_CSV)
        # normalize columns expected: city,state,region,lat,lon,population,timezone,notes
        return df
    except Exception:
        return pd.DataFrame(columns=["city","state","region","lat","lon","population","timezone","notes"])

@lru_cache(maxsize=1)
def _phrasebook_df() -> pd.DataFrame:
    try:
        df = pd.read_csv(PHRASEBOOK_CSV)
        # expected: language,english,translation,topic(optional)
        return df
    except Exception:
        return pd.DataFrame(columns=["language","english","translation","topic"])

def list_cities() -> List[str]:
    df = _cities_df()
    if df.empty: return []
    return sorted(df["city"].dropna().unique().tolist())

def city_exists(city: str) -> bool:
    df = _cities_df()
    if df.empty: return False
    return city.lower() in (df["city"].str.lower().tolist())

def get_city_info(city: str) -> Dict[str, Any]:
    df = _cities_df()
    if df.empty: return {}
    row = df[df["city"].str.lower() == city.lower()].head(1)
    return row.to_dict(orient="records")[0] if not row.empty else {}

def phrasebook(language: str) -> List[Dict[str, str]]:
    df = _phrasebook_df()
    if df.empty: return []
    sub = df[df["language"].str.lower() == language.lower()]
    return sub[["english","translation","language"]].to_dict(orient="records")

def search_phrase(english: str, language: str) -> Dict[str, str] | None:
    df = _phrasebook_df()
    if df.empty: return None
    hit = df[(df["language"].str.lower()==language.lower()) & (df["english"].str.lower()==english.lower())]
    return hit[["english","translation","language"]].to_dict(orient="records")[0] if not hit.empty else None
