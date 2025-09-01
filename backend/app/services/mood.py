
from typing import List, Dict
from ..db import get_conn

def list_recent_mood(user_id: int) -> List[Dict]:
    conn = get_conn()
    rows = conn.execute("""
        SELECT label, score, ts FROM mood
        WHERE user_id=?
        ORDER BY ts DESC
        LIMIT 12
    """, (user_id,)).fetchall()
    # Keep order inserted (latest last)
    rows = rows[::-1]
    return [{"label": r["label"], "score": int(r["score"])} for r in rows]
