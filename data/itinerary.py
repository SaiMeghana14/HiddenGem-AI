from __future__ import annotations
from pathlib import Path
from functools import lru_cache
import os, math, pandas as pd
from typing import List, Dict, Any

def _dd():
    env = os.getenv("HIDDENGEM_DATA_DIR")
    if env and Path(env).exists(): return Path(env)
    here = Path(__file__).resolve()
    for p in [here.parent.parent/"data", here.parent/"data", Path.cwd()/"data"]:
        if p.exists(): return p
    return Path("data")

DATA_DIR = _dd()
ATTRACTIONS_CSV = DATA_DIR / "attractions.csv"
FOOD_CSV = DATA_DIR / "food.csv"
STAYS_CSV = DATA_DIR / "stays.csv"

@lru_cache(maxsize=1)
def _attractions() -> pd.DataFrame:
    try: 
        df = pd.read_csv(ATTRACTIONS_CSV)
        return df
    except Exception: 
        return pd.DataFrame(columns=["city","name","type","cost","lat","lon","tags","photogenic","sustainability","safety"])

@lru_cache(maxsize=1)
def _food() -> pd.DataFrame:
    try: return pd.read_csv(FOOD_CSV)
    except Exception: return pd.DataFrame(columns=["city","name","price","lat","lon","tags"])

@lru_cache(maxsize=1)
def _stays() -> pd.DataFrame:
    try: return pd.read_csv(STAYS_CSV)
    except Exception: return pd.DataFrame(columns=["city","name","price","url","lat","lon"])

def _haversine(a: tuple[float,float], b: tuple[float,float]) -> float:
    # distance in km
    lat1, lon1 = a; lat2, lon2 = b
    R = 6371.0
    dlat = math.radians(lat2-lat1); dlon = math.radians(lon2-lon1)
    x = math.sin(dlat/2)**2 + math.cos(math.radians(lat1))*math.cos(math.radians(lat2))*math.sin(dlon/2)**2
    return 2*R*math.asin(min(1, math.sqrt(x)))

def _closest_route(points: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    # simple nearest-neighbor ordering
    if not points: return []
    remaining = points.copy()
    ordered = [remaining.pop(0)]
    while remaining:
        last = ordered[-1]
        remaining.sort(key=lambda p: _haversine((last["lat"], last["lon"]), (p["lat"], p["lon"])))
        ordered.append(remaining.pop(0))
    return ordered

def build_itinerary(city: str, days: int=2, budget_per_day: int=1000, preferences: List[str]|None=None) -> Dict[str, Any]:
    preferences = preferences or []
    a = _attractions()
    f = _food()
    s = _stays()

    acity = a[a["city"].str.lower()==city.lower()].copy()
    if not acity.empty and preferences:
        # content-based: prefer rows whose tags contain any preference
        m = acity["tags"].fillna("").str.contains("|".join([p for p in preferences]), case=False)
        acity = pd.concat([acity[m], acity[~m]]).drop_duplicates()

    # cost fallback
    if "cost" not in acity.columns: acity["cost"] = 200
    acity["lat"] = acity["lat"].fillna(method="ffill").fillna(method="bfill").fillna(0.0)
    acity["lon"] = acity["lon"].fillna(method="ffill").fillna(method="bfill").fillna(0.0)

    # split across days
    per_day = max(1, len(acity)//days) if len(acity) >= days else 1
    chunks = [acity.iloc[i:i+per_day] for i in range(0, len(acity), per_day)]
    chunks = (chunks + [pd.DataFrame()]*days)[:days]

    plan = []
    for i, dfday in enumerate(chunks, start=1):
        stops = []
        if not dfday.empty:
            pts = dfday[["name","type","cost","lat","lon","tags"]].to_dict(orient="records")
            # ensure all have lat/lon
            pts = [p for p in pts if "lat" in p and "lon" in p and (p["lat"] or p["lon"])]
            ordered = _closest_route(pts) if pts else []
            stops.extend(ordered)

        # insert one local food spot if available
        fcity = f[f["city"].str.lower()==city.lower()]
        if not fcity.empty:
            fd = fcity.sample(1).iloc[0]
            stops.append({
                "name": fd["name"], "category": "food", "cost": fd.get("price", 200),
                "lat": float(fd.get("lat", 0.0)), "lon": float(fd.get("lon", 0.0)), "tags": fd.get("tags", "")
            })

        # compute budget for the day
        est_budget = int(sum([int(x.get("cost", 200)) for x in stops]))
        # clamp to budget_per_day by pruning last items if needed
        while est_budget > budget_per_day and len(stops) > 1:
            rm = stops.pop()  # drop last
            est_budget -= int(rm.get("cost", 0))

        # normalise fields for frontend
        norm = []
        for spt in stops:
            norm.append({
                "name": spt.get("name"),
                "category": spt.get("type","spot") if spt.get("type") else spt.get("category","spot"),
                "cost": int(spt.get("cost", 200)),
                "lat": float(spt.get("lat", 0.0)),
                "lon": float(spt.get("lon", 0.0)),
                "tags": spt.get("tags","")
            })

        plan.append({"day": i, "stops": norm, "est_budget": est_budget})

    # attach a stay suggestion
    stay = None
    if not s.empty:
        srow = s[s["city"].str.lower()==city.lower()]
        if not srow.empty:
            sr = srow.sort_values(by="price").head(1).iloc[0]
            stay = {"name": sr["name"], "price": int(sr["price"]), "url": sr.get("url","#")}

    return {"city": city, "days": days, "plan": plan, "stay": stay}
