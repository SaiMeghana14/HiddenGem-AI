import os, sqlite3, json
from typing import List, Dict, Any

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "..", "community.db")
DB_PATH = os.path.abspath(DB_PATH)

def _ensure_db():
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS community (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT, city TEXT, lat REAL, lon REAL, category TEXT, tags TEXT, notes TEXT, votes INTEGER DEFAULT 0
    )""")
    con.commit()
    con.close()

def add_community_place(name, city, lat, lon, category, tags, notes) -> int:
    _ensure_db()
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    cur.execute("INSERT INTO community (name, city, lat, lon, category, tags, notes, votes) VALUES (?,?,?,?,?,?,?,0)",
                (name, city, lat, lon, category, tags, notes))
    con.commit()
    pid = cur.lastrowid
    con.close()
    return pid

def vote_place(place_id: int, delta: int) -> bool:
    _ensure_db()
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    cur.execute("UPDATE community SET votes = votes + ? WHERE id = ?", (delta, place_id))
    ok = cur.rowcount > 0
    con.commit()
    con.close()
    return ok

def list_community_places(city: str) -> List[Dict[str, Any]]:
    _ensure_db()
    con = sqlite3.connect(DB_PATH)
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("SELECT * FROM community WHERE city = ? ORDER BY votes DESC", (city,))
    rows = [dict(r) for r in cur.fetchall()]
    con.close()
    return rows
