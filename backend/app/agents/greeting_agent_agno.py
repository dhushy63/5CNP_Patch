# backend/app/agents/greeting_agent_agno.py
from ._agno_common import make_agent

SYS = (
    "You greet the user briefly by name and city. "
    "Keep it 1–2 sentences. Friendly, concise."
)

def respond(name: str | None, city: str | None) -> str:
    # Graceful fallback if context missing
    if not name or not city:
        return "Hi! I couldn’t find your profile details yet, but welcome 🙂"
    agent = make_agent(SYS)
    return str(agent.run(f"Greet the user named {name} from {city}. One or two sentences only."))
