from __future__ import annotations
from pathlib import Path
from functools import lru_cache
import os, pandas as pd
from typing import Dict, Any

def _dd() -> Path:
    env = os.getenv("HIDDENGEM_DATA_DIR")
    if env and Path(env).exists(): return Path(env)
    here = Path(__file__).resolve()
    for p in [here.parent.parent/"data", here.parent/"data", Path.cwd()/"data"]:
        if p.exists(): return p
    return Path("data")

DATA_DIR = _dd()
PHRASEBOOK_CSV = DATA_DIR / "phrasebook.csv"

@lru_cache(maxsize=1)
def _pb() -> pd.DataFrame:
    try: return pd.read_csv(PHRASEBOOK_CSV)
    except Exception: return pd.DataFrame(columns=["language","english","translation","topic"])

def translate(text: str, dest: str, src: str="auto") -> Dict[str, Any]:
    """
    Lightweight translator using phrasebook as offline fallback.
    Returns original if not found.
    """
    if not text: return {"source": src, "translated": "", "offline": True}
    df = _pb()
    if df.empty: 
        return {"source": src, "translated": text, "offline": True}
    # exact english → dest language
    hit = df[(df["language"].str.lower()==dest.lower()) & (df["english"].str.lower()==text.lower())]
    if not hit.empty:
        return {"source": "phrasebook", "translated": hit.iloc[0]["translation"], "offline": True}
    # otherwise return original
    return {"source": "auto", "translated": text, "offline": True}

def phrasebook_lookup(english: str, dest: str) -> str|None:
    df = _pb()
    if df.empty: return None
    hit = df[(df["language"].str.lower()==dest.lower()) & (df["english"].str.lower()==english.lower())]
    return None if hit.empty else hit.iloc[0]["translation"]
