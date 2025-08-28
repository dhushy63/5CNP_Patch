"""
Interrupt Agent (Agno-backed with graceful fallback)

- If Agno + OPENAI_API_KEY are available, answers with an LLM via Agno.
- Otherwise, returns a deterministic local stub so the API never breaks.

Usage from FastAPI route:
    from .agents.interrupt_agent import respond as interrupt_respond

    @app.post("/interrupt")
    def interrupt(in_: InterruptIn = Body(...)):
        text = interrupt_respond(in_.query, in_.user_id)
        return {"reply": text}
"""

from __future__ import annotations

import os
import re
from typing import Optional

# Try importing Agno + OpenAI adapter. If not present, we fall back.
try:
    from agno.agent import Agent
    from agno.models.openai import OpenAIChat  # Agno 1.7.12: use id= or positional for model name
    _AGNO_IMPORTED = True
    _AGNO_IMPORT_ERR: Optional[Exception] = None
except Exception as _e:
    _AGNO_IMPORTED = False
    _AGNO_IMPORT_ERR = _e

# A concise system prompt that biases answers toward safe, helpful health guidance.
SYSTEM_PROMPT = (
    "You are a concise, friendly health Q&A assistant for a demo app. "
    "Prefer low-glycemic and heart-healthy suggestions when relevant. "
    "Avoid definitive medical diagnoses; add a short caution to consult a professional "
    "when advice could be medical. Keep answers brief and actionable."
)

# --------- helpers ---------

def _env(key: str) -> str:
    """Get env var trimmed; returns '' if missing."""
    v = os.getenv(key)
    return (v or "").strip()

def _have_llm() -> bool:
    """True if Agno is importable and we have a non-empty OPENAI_API_KEY."""
    if not _AGNO_IMPORTED:
        return False
    return bool(_env("OPENAI_API_KEY"))

def _clean(s: str) -> str:
    """Normalize whitespace to avoid weird formatting in UI."""
    s = (s or "").strip()
    s = re.sub(r"\s+\n", "\n", s)
    s = re.sub(r"\n{3,}", "\n\n", s)
    return s

def _stub_answer(query: str) -> str:
    """Deterministic local fallback if LLM is not available."""
    q = (query or "").strip().lower()
    if not q:
        return "Please type a question (e.g., 'low-GI breakfast ideas?')."

    # Very tiny, safe canned guidance so the demo still looks intelligent.
    if any(k in q for k in ["low-gi", "low gi", "low glycemic", "breakfast"]):
        return (
            "Try a veggie omelette, paneer bhurji with sautéed spinach, or Greek yogurt with nuts. "
            "Prefer whole grains (e.g., oats), add protein, and limit added sugar. "
            "For personal advice, consult a healthcare professional."
        )
    if "meal" in q and "plan" in q:
        return (
            "Aim for balanced plates: half veggies, a quarter lean protein, a quarter whole grains. "
            "Hydrate well and keep snacks fiber-rich. For tailored plans, consult a professional."
        )
    return (
        "Here’s a quick tip: prefer minimally processed foods, balance carbs with protein and fiber, "
        "and stay hydrated. For personalized guidance, consult a healthcare professional."
    )

def _diagnose_env() -> str:
    """
    Quick diagnostics for common misconfig:
    - Missing Agno
    - Empty key
    - Suspicious whitespace
    - Project/Org hints
    """
    notes = []
    if not _AGNO_IMPORTED:
        notes.append("Agno not installed")
    raw_key = os.getenv("OPENAI_API_KEY")
    key = _env("OPENAI_API_KEY")
    if not key:
        notes.append("OPENAI_API_KEY not set or empty")
    elif raw_key and raw_key != key:
        notes.append("OPENAI_API_KEY had leading/trailing whitespace; trimmed")

    if _env("OPENAI_PROJECT"):
        notes.append("OPENAI_PROJECT set")
    if _env("OPENAI_ORG_ID"):
        notes.append("OPENAI_ORG_ID set")
    return "; ".join(notes) if notes else "env looks OK"

def _friendly_error_hint(err: Exception) -> str:
    """
    Map common provider errors to actionable hints, without leaking stack traces.
    """
    msg = f"{err}"
    low = msg.lower()
    if "invalid_api_key" in low or "unauthorized" in low:
        return ("Invalid API key. Check OPENAI_API_KEY inside the container "
                "(no quotes/newlines) and ensure it belongs to the intended project/org. "
                "If you use Projects, consider setting OPENAI_PROJECT.")
    if "quota" in low or "insufficient_quota" in low or "exceeded your current quota" in low:
        return ("Project/account has no usable credits or a zero usage cap. "
                "Add billing or raise the project/org usage limit; a new key in the same unfunded project "
                "won't help. If you have multiple projects, set OPENAI_PROJECT to one with billing.")
    if "project" in low and ("not found" in low or "missing" in low):
        return ("OPENAI_PROJECT seems invalid or not visible to this key. "
                "Create/select a billed project and set OPENAI_PROJECT to its ID.")
    return "Unexpected LLM error."

def _extract_text(result) -> str:
    """
    Robustly extract text from Agno's agent.run(...) result.
    Prefers RunResponse.content, but falls back gracefully.
    """
    if isinstance(result, str):
        return result
    # Try common attributes in order
    for attr in ("content", "output_text", "text"):
        val = getattr(result, attr, None)
        if isinstance(val, str) and val.strip():
            return val
    # Last resort: stringification
    return str(result or "")

# --------- main entry ---------

def respond(query: str, user_id: Optional[int] = None) -> str:
    """
    Main entry point used by the FastAPI route.
    - Attempts Agno+LLM if available.
    - Falls back to a local stub on any error or when key/packages are missing.

    Compatible with Agno 1.7.12 — uses OpenAIChat(id=<model_name>).
    Also provides clearer diagnostics for invalid key vs quota issues.
    """
    q = (query or "").strip()
    if not q:
        return "Please type a question (e.g., 'low-GI breakfast ideas?')."

    # Early preflight: catch most common misconfigs up front.
    if not _AGNO_IMPORTED:
        return _stub_answer(q) + " (LLM disabled: Agno not installed)"
    api_key = _env("OPENAI_API_KEY")
    if not api_key:
        return _stub_answer(q) + " (LLM disabled: OPENAI_API_KEY not set or empty)"

    # Optionally surface that we trimmed whitespace
    raw_key = os.getenv("OPENAI_API_KEY")
    trimmed_note = ""
    if raw_key and raw_key != api_key:
        trimmed_note = " (note: OPENAI_API_KEY had whitespace; auto-trimmed)"

    # Use Agno + OpenAI (Agno 1.7.12 signature)
    try:
        model_name = _env("AGNO_MODEL") or "gpt-4o-mini"

        # Agno respects OpenAI SDK envs (OPENAI_PROJECT, OPENAI_ORG_ID) if you set them.
        # IMPORTANT for 1.7.12: pass model via id= or positionally (not model=)
        agent = Agent(
            model=OpenAIChat(id=model_name),
            instructions=SYSTEM_PROMPT,
        )
        result = agent.run(q)  # returns a RunResponse-like object
        text = _clean(_extract_text(result))
        if not text:
            return _stub_answer(q) + " (LLM returned empty output)"
        return (text[:1600].rstrip()) + trimmed_note
    except Exception as e:
        hint = _friendly_error_hint(e)
        env_note = _diagnose_env()
        # Never break the app; degrade gracefully and surface a concise hint.
        return f"{_stub_answer(q)} (LLM error: {type(e).__name__}: {e}. {hint}. {_clean(env_note)})"

# Simple CLI for quick local testing:
#   python backend/app/agents/interrupt_agent.py "low-GI breakfast ideas?"
if __name__ == "__main__":
    import sys
    sample = " ".join(sys.argv[1:]) or "low-GI breakfast ideas?"
    print(respond(sample, user_id=1))