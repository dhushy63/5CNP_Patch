
from ..db import get_conn

def greet(user_id: int):
    conn = get_conn()
    row = conn.execute("SELECT first_name, last_name, city, diet, conditions FROM users WHERE id=?", (user_id,)).fetchone()
    if not row:
        return {"name": "User", "city": "Unknown", "diet": "", "conditions": [], "message": "Hello!"}
    name = f"{row['first_name']} {row['last_name']}"
    conds = [c.strip() for c in (row["conditions"] or "").split(",") if c.strip()]
    message = f"Hello, {name} from {row['city']}! How can I assist you today?"
    return {"name": name, "city": row["city"], "diet": row["diet"], "conditions": conds, "message": message}
