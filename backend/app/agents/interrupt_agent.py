from ..db import get_conn
from ..services.llm_stub import answer
from .agno_bridge import AGNO_ENABLED, run_interrupt

def respond(user_id: int, query: str):
    conn = get_conn()
    row = conn.execute(
        "SELECT first_name, last_name, city, conditions FROM users WHERE id=?",
        (user_id,)
    ).fetchone()
    profile = dict(row) if row else {}

    # Try Agno (safe; returns None on error)
    if AGNO_ENABLED:
        out = run_interrupt(query, profile)
        if out:
            return {"reply": out}

    # Fallback stub (never errors)
    return {"reply": answer(query, profile)}
