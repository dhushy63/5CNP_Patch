from typing import Optional
from .greeting_agent_agno import respond as greet_llm
from .mood_agent_agno import summarize as mood_sum
from .cgm_agent_agno import summarize as cgm_sum
from .mealplan_agent_agno import plan as meal_plan
from .interrupt_agent import respond as interrupt_llm

def route(query: str, ctx: dict) -> str:
    q = (query or "").strip().lower()
    name: Optional[str] = ctx.get("name")
    city: Optional[str] = ctx.get("city")
    mood_series = ctx.get("mood_series", [])
    cgm_series = ctx.get("cgm_series", [])
    diet = ctx.get("diet", "vegetarian")
    conditions = ctx.get("conditions", [])
    hints = ctx.get("hints", {})

    if any(k in q for k in ("hello","hi","hey","greet","welcome")):
        return greet_llm(name, city)
    if "mood" in q:
        return mood_sum(mood_series)
    if any(k in q for k in ("cgm","glucose","sugar","blood sugar")):
        return cgm_sum(cgm_series)
    if any(k in q for k in ("meal","plan","diet","menu","food plan","meal plan")):
        meals = meal_plan(diet, conditions, hints)
        return " • " + "\n • ".join(meals)
    return interrupt_llm(query, ctx.get("user_id"))
