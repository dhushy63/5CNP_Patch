from __future__ import annotations
from typing import Dict, List, Optional

def _fallback(user_id: int, diet: str) -> Dict:
    diet = (diet or "veg").lower()
    if diet == "vegan":
        meals = [
            {"type":"breakfast","items":"Tofu bhurji + multigrain toast"},
            {"type":"lunch","items":"Brown rice + dal + salad"},
            {"type":"snacks","items":"Roasted chana + fruit"},
            {"type":"dinner","items":"Millet khichdi + veggies"},
        ]
    elif diet == "non-vegetarian":
        meals = [
            {"type":"breakfast","items":"Masala omelette + whole-wheat toast"},
            {"type":"lunch","items":"Grilled chicken + roti + salad"},
            {"type":"snacks","items":"Yogurt + nuts"},
            {"type":"dinner","items":"Fish curry + brown rice"},
        ]
    else:
        meals = [
            {"type":"breakfast","items":"Poha with peanuts + sprouts"},
            {"type":"lunch","items":"Roti + dal + sabzi + salad"},
            {"type":"snacks","items":"Buttermilk + nuts"},
            {"type":"dinner","items":"Vegetable pulao + raita"},
        ]
    return {"user_id": user_id, "meals": meals}

def build_meal_plan(user_id: int) -> Dict:
    """
    ALWAYS returns a dict with 4 meals.
    Tries Agno JSON first; on ANY error, returns deterministic fallback.
    """
    try:
        # Lazy imports so a missing module never crashes the route
        from ..db import get_conn
        from ..services.mood import list_recent_mood
        from ..services.cgm import latest_cgm

        # profile
        conn = get_conn()
        row = conn.execute(
            "SELECT id, first_name, last_name, city, diet, conditions FROM users WHERE id=?",
            (user_id,)
        ).fetchone()
        if not row:
            return _fallback(user_id, "veg")
        profile = dict(row)
        diet = (profile.get("diet") or "veg")

        # latest signals
        cgm = latest_cgm(user_id) if "latest_cgm" in dir() or True else None  # guard anyway
        mood_list = list_recent_mood(user_id) or []
        latest_mood = mood_list[-1]["label"] if mood_list else None
        latest_cgm_val = cgm["value"] if (isinstance(cgm, dict) and "value" in cgm) else None

        # Try Agno planner (optional)
        try:
            from ..agents.mealplanner_agno import plan_meals as agno_plan
            ag = agno_plan(profile, latest_cgm_val, latest_mood)
            if ag and isinstance(ag, dict) and ag.get("meals"):
                # Ensure 4 meals shape
                types = {m.get("type") for m in ag["meals"] if isinstance(m, dict)}
                needed = ["breakfast","lunch","snacks","dinner"]
                if all(t in types for t in needed):
                    return ag
        except Exception:
            # swallow and fall through to fallback
            pass

        # Deterministic fallback
        return _fallback(user_id, diet)
    except Exception:
        # absolutely never 500: ultimate fallback
        return _fallback(user_id, "veg")
