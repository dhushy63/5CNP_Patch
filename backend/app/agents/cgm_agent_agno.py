# backend/app/agents/cgm_agent_agno.py
from ._agno_common import make_agent

SYS = (
    "You are a CGM (glucose) coach. If values are out of 80–300 mg/dL, "
    "flag gently. One sentence only; not medical advice."
)

def summarize(values: list[tuple[str, float]]) -> str:
    """
    values: list of (iso_ts, glucose_mgdl)
    """
    agent = make_agent(SYS)
    sample = values[:20] if values else []
    return str(agent.run(f"Summarize CGM values briefly (ts,value): {sample}"))
