from __future__ import annotations
from pathlib import Path
from functools import lru_cache
import os
import pandas as pd
from typing import List, Dict, Any

def _data_dir() -> Path:
    env = os.getenv("HIDDENGEM_DATA_DIR")
    if env and Path(env).exists(): return Path(env)
    here = Path(__file__).resolve()
    for c in [here.parent.parent/"data", here.parent/"data", Path.cwd()/"data"]:
        if c.exists(): return c
    return Path("data")

DATA_DIR = _data_dir()
FOOD_CSV = DATA_DIR / "food.csv"

@lru_cache(maxsize=1)
def _food_df() -> pd.DataFrame:
    try:
        return pd.read_csv(FOOD_CSV)
    except Exception:
        return pd.DataFrame(columns=["city","name","type","authentic","veg","price","rating","description","lat","lon","tags"])

def food_spots(city: str, authentic: bool=True, veg: bool|None=None, max_price: int|None=None) -> List[Dict[str, Any]]:
    df = _food_df()
    if df.empty: return []
    q = df[df["city"].str.lower() == city.lower()]
    if authentic:
        q = q[(q["authentic"]==True) | (q["tags"].fillna("").str.contains("authentic|local|family", case=False))]
    if veg is not None:
        q = q[q["veg"]==bool(veg)]
    if max_price is not None and "price" in q:
        q = q[q["price"].fillna(10**9) <= max_price]
    cols = [c for c in ["name","type","price","rating","description","lat","lon","veg","authentic","tags"] if c in q.columns]
    return q[cols].to_dict(orient="records")

def cultural_experiences(city: str) -> List[Dict[str, Any]]:
    # A simple stub: recommend entries from food tagged with 'class|workshop|music|dance' as cultural pointers
    df = _food_df()
    if df.empty: return []
    q = df[(df["city"].str.lower()==city.lower()) & (df["tags"].fillna("").str.contains("class|workshop|music|dance|festival", case=False))]
    cols = [c for c in ["name","type","description","price","lat","lon","tags"] if c in q.columns]
    return q[cols].to_dict(orient="records")
