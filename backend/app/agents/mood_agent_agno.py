# backend/app/agents/mood_agent_agno.py
from ._agno_common import make_agent

SYS = (
    "You summarize mood trends briefly and positively. "
    "One short sentence. Not medical advice."
)

def summarize(trend_points: list[tuple[str,int]]) -> str:
    """
    trend_points: list of (iso_ts, score) where score is an int, e.g., 1-5.
    """
    agent = make_agent(SYS)
    sample = trend_points[:20] if trend_points else []
    return str(agent.run(f"Summarize this mood series in one short, friendly sentence: {sample}"))

def confirm_log(label: str) -> str:
    agent = make_agent(SYS)
    return str(agent.run(f"Confirm that we logged mood='{label}' in one sentence."))
