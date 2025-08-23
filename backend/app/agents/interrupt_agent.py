
from ..db import get_conn
from ..services.llm_stub import answer

def respond(user_id: int, query: str):
    conn = get_conn()
    row = conn.execute("SELECT first_name, last_name, city, conditions FROM users WHERE id=?", (user_id,)).fetchone()
    profile = dict(row) if row else {}
    return {"reply": answer(query, profile)}
