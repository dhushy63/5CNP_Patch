# backend/app/agents/interrupt_agno.py
import os

try:
    from agno.agent import Agent
    from agno.models.openai import OpenAIChat
    _AGNO_AVAILABLE = True
except Exception:
    _AGNO_AVAILABLE = False

SYSTEM_PROMPT = (
    "You are a concise, friendly health Q&A assistant. "
    "Prefer low-GI, heart-healthy guidance. If advice could be medical, "
    "add a short caution to consult a professional."
)

def respond(query: str, user_id: int | None = None) -> str:
    # Only run if both Agno and OPENAI_API_KEY exist
    if not _AGNO_AVAILABLE or not os.getenv("OPENAI_API_KEY"):
        return "(LLM disabled) I answered your question. Re-run with OPENAI_API_KEY to enable LLM."

    # Model name can be changed to your provider’s supported option
    model = OpenAIChat(model="gpt-4o-mini")

    agent = Agent(
        model=model,
        instructions=SYSTEM_PROMPT,
    )

    # Agno's Agent.run(...) returns a response object printable as text
    try:
        result = agent.run(query)
        return str(result)
    except Exception as e:
        # Never break the API; degrade gracefully
        return f"(LLM error) {e.__class__.__name__}: {e}"
