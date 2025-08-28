# backend/app/agents/mealplan_agent_agno.py
from ._agno_common import make_agent

SYS = (
    "You are a diet planner. Given dietary preference, medical conditions, "
    "and hints (like latest CGM), output exactly 3 lines: Breakfast, Lunch, Dinner. "
    "Low-GI bias if diabetes is present. Keep each line concise."
)

def plan(diet: str, conditions: list[str], hints: dict) -> list[str]:
    agent = make_agent(SYS)
    text = str(agent.run(
        f"Preference: {diet}\n"
        f"Conditions: {conditions}\n"
        f"Hints: {hints}\n"
        "Return exactly three bullet points: Breakfast, Lunch, Dinner."
    ))
    lines = [ln.strip("-• ").strip() for ln in text.splitlines() if ln.strip()]
    meals = [ln for ln in lines if ln][:3]
    if len(meals) < 3:
        meals = meals + ["Oats with nuts", "Dal + roti + salad", "Grilled paneer + veggies"][: 3 - len(meals)]
    return meals
