import os
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

SYSTEM_INTERRUPTER = """You are a concise, friendly healthcare Q&A assistant.
- Respect user profile (name, city, dietary preference, conditions) if provided.
- If a question is medical, provide general guidance and a safety disclaimer (not a diagnosis).
- Keep answers short and actionable. Route the user back to their main task in one closing line."""

def _build_agent() -> Optional["Agent"]:
    if not AGNO_ENABLED:
        return None
    model_name = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    return Agent(model=OpenAIChat(id=model_name), instructions=SYSTEM_INTERRUPTER, markdown=False)

def run_interrupt(query: str, profile: dict) -> Optional[str]:
    try:
        agent = _build_agent()
        if not agent:
            return None
        context = f"User profile: {profile}\n" if profile else ""
        prompt = context + "Answer the user's question:\n" + query
        return str(agent.run(prompt))
    except Exception:
        return None
