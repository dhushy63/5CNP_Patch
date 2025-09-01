
from typing import List, Dict
from datetime import datetime
from ..db import get_conn

def add_food(user_id: int, description: str) -> Dict:
    conn = get_conn()
    ts = datetime.utcnow().isoformat()
    conn.execute("INSERT INTO food(user_id, description, ts) VALUES(?,?,?)", (user_id, description, ts))
    conn.commit()
    return {"ok": True, "ts": ts}

def list_recent_food(user_id: int) -> List[Dict]:
    conn = get_conn()
    rows = conn.execute("""
        SELECT description, ts FROM food
        WHERE user_id=?
        ORDER BY ts DESC
        LIMIT 10
    """, (user_id,)).fetchall()
    return [{"description": r["description"], "ts": r["ts"]} for r in rows]
