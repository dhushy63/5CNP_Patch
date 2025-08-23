
from typing import List, Dict
from datetime import datetime, timedelta
from ..db import get_conn

def list_recent_cgm(user_id: int) -> List[Dict]:
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
        SELECT ts, value FROM cgm
        WHERE user_id=?
        ORDER BY ts DESC
        LIMIT 42
    """, (user_id,))
    rows = cur.fetchall()
    # Return ascending by time
    points = [{"ts": r["ts"], "value": float(r["value"])} for r in rows][::-1]
    return points

def latest_cgm(user_id: int):
    conn = get_conn()
    row = conn.execute("SELECT value FROM cgm WHERE user_id=? ORDER BY ts DESC LIMIT 1", (user_id,)).fetchone()
    return float(row["value"]) if row else None
