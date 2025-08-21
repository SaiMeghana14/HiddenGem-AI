from __future__ import annotations
from pathlib import Path
from functools import lru_cache
import os, pandas as pd
from typing import List, Dict, Any, Optional

def _dd() -> Path:
    env = os.getenv("HIDDENGEM_DATA_DIR")
    if env and Path(env).exists(): return Path(env)
    here = Path(__file__).resolve()
    for p in [here.parent.parent/"data", here.parent/"data", Path.cwd()/"data"]:
        if p.exists(): return p
    return Path("data")

DATA_DIR = _dd()
CITIES_CSV = DATA_DIR / "cities.csv"

@lru_cache(maxsize=1)
def _cities() -> pd.DataFrame:
    try: return pd.read_csv(CITIES_CSV)
    except Exception: return pd.DataFrame(columns=["city","state","region","lat","lon","population","timezone","notes"])

def cities() -> List[str]:
    df = _cities()
    return [] if df.empty else sorted(df["city"].dropna().unique().tolist())

def city_meta(city: str) -> Dict[str, Any]:
    df = _cities()
    if df.empty: return {}
    row = df[df["city"].str.lower()==city.lower()].head(1)
    return row.to_dict(orient="records")[0] if not row.empty else {}

def city_guide_text(city: str) -> Optional[str]:
    """
    Reads optional rich guide text from data/guides/<city>.py if present (expects GUIDE string).
    """
    path = DATA_DIR / "guides" / f"{city.lower().replace(' ','_')}.py"
    if not path.exists(): 
        return None
    scope: Dict[str, Any] = {}
    try:
        exec(path.read_text(encoding="utf-8"), scope)
        return scope.get("GUIDE") or None
    except Exception:
        return None
