
def answer(query: str, user_profile: dict | None = None) -> str:
    # Local stub so app works without keys
    base = "I’m a local helper (LLM disabled)"
    if user_profile:
        who = f'{user_profile.get("first_name","User")} from {user_profile.get("city","your city")}'
        return f"{base}. You asked: '{query}'. {who}, here’s a generic suggestion: stay hydrated and choose balanced meals."
    return f"{base}. You asked: '{query}'."
