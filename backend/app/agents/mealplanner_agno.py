import os, json
from typing import Optional

try:
    from dotenv import load_dotenv
    load_dotenv()
except Exception:
    pass

AGNO_ENABLED = False
try:
    from agno.agent import Agent
    from agno.models.openai import OpenAIChat
    AGNO_ENABLED = True
except Exception:
    AGNO_ENABLED = False

SYSTEM_MEAL_PLANNER = """You are a meal-planning assistant for Indian context.
- Respect diet (veg / non-veg / vegan) and medical conditions (e.g., hypertension).
- Favor low-GI choices if glucose is high.
- Output STRICT JSON with keys: breakfast, lunch, snacks, dinner. Each value is a short string of items.
- Do not include explanations or markdown. Only return JSON."""

def _agent() -> Optional["Agent"]:
    if not AGNO_ENABLED:
        return None
    model_name = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    return Agent(model=OpenAIChat(id=model_name), instructions=SYSTEM_MEAL_PLANNER, markdown=False)

def _safe_parse(json_text: str) -> Optional[dict]:
    try:
        data = json.loads(json_text)
        # normalize and validate keys
        out = {}
        for k in ("breakfast","lunch","snacks","dinner"):
            v = data.get(k) or data.get(k.capitalize()) or ""
            out[k] = v if isinstance(v, str) else ""
        # require at least breakfast + one more
        if out["breakfast"] or out["lunch"]:
            return out
        return None
    except Exception:
        return None

def plan_meals(profile: dict, latest_cgm: float|None, latest_mood: str|None) -> Optional[dict]:
    """
    Returns {"user_id": id, "meals":[{"type":..,"items":..}, ...]} or None if Agno unavailable.
    """
    try:
        agent = _agent()
        if not agent:
            return None
        # Compact context to stay under token limits
        ctx = {
            "diet": profile.get("diet"),
            "conditions": profile.get("conditions"),
            "city": profile.get("city"),
            "latest_cgm": latest_cgm,
            "latest_mood": latest_mood
        }
        prompt = (
            "Create a 1-day meal plan given this context:\n"
            f"{ctx}\n"
            "Return STRICT JSON only: {\"breakfast\":\"...\", \"lunch\":\"...\", \"snacks\":\"...\", \"dinner\":\"...\"}"
        )
        resp = agent.run(prompt)
        # Extract text from Agno response across versions
        text = None
        for attr in ("content", "output_text", "text"):
            if hasattr(resp, attr) and getattr(resp, attr):
                text = str(getattr(resp, attr))
                break
        if text is None:
            text = str(resp)

        parsed = _safe_parse(text)
        if not parsed:
            return None

        meals = [
            {"type":"breakfast","items": parsed["breakfast"]},
            {"type":"lunch","items": parsed["lunch"]},
            {"type":"snacks","items": parsed["snacks"]},
            {"type":"dinner","items": parsed["dinner"]},
        ]
        return {"user_id": profile.get("id"), "meals": meals}
    except Exception:
        return None
