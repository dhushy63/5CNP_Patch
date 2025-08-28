# backend/app/agents/_agno_common.py
import os
from agno.agent import Agent
from agno.models.openai import OpenAIChat

def make_agent(instructions: str) -> Agent:
    model_name = os.getenv("AGNO_MODEL", "gpt-4o-mini")
    return Agent(
        model=OpenAIChat(model=model_name),
        instructions=instructions,
    )
