
from typing import Dict, List
from ..db import get_conn

def get_user(user_id: int):
    conn = get_conn()
    r = conn.execute("SELECT id, first_name, last_name, city, diet, conditions FROM users WHERE id=?", (user_id,)).fetchone()
    return r

def build_meal_plan(user_id: int) -> Dict:
    user = get_user(user_id)
    if not user:
        return {"user_id": user_id, "meals": []}
    diet = user["diet"]
    conds = (user["conditions"] or "").lower()

    # very simple rules
    diabetic = "diabetes" in conds
    hypert = "hypertension" in conds

    breakfast = "Oats porridge + nuts + berries" if diabetic else "Veggie omelette + toast" if diet != "vegan" else "Tofu scramble + avocado toast"
    if diet == "vegan":
        lunch = "Quinoa bowl with chickpeas, greens, and tahini"
        dinner = "Lentil curry with brown rice"
    elif diet == "vegetarian":
        lunch = "Dal + 2 chapatis + salad"
        dinner = "Paneer stir-fry + brown rice"
    else:
        lunch = "Grilled chicken + quinoa + salad"
        dinner = "Fish curry + rice + sautéed veggies"

    snacks = "Apple / nuts; avoid sugary drinks" if diabetic else "Fruit + yogurt" if diet != "vegan" else "Fruit + hummus"

    if hypert:
        lunch += " (low-salt)"
        dinner += " (low-salt)"

    return {
        "user_id": user_id,
        "meals": [
            {"type": "breakfast", "items": breakfast},
            {"type": "lunch", "items": lunch},
            {"type": "snacks", "items": snacks},
            {"type": "dinner", "items": dinner},
        ]
    }
