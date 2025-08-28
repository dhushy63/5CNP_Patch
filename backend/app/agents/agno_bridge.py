import os
from typing import Optional, Dict

def is_enabled() -> bool:
    return bool(os.getenv("OPENAI_API_KEY"))

def ask_llm(query: str, user_profile: Optional[Dict] = None) -> str:
    from openai import OpenAI
    client = OpenAI()  # reads OPENAI_API_KEY from env
    model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

    profile_bits = []
    if user_profile:
        fn = user_profile.get("first_name") or ""
        ln = user_profile.get("last_name") or ""
        city = user_profile.get("city") or ""
        diet = user_profile.get("diet") or ""
        conds = user_profile.get("conditions") or ""
        profile_bits.append(f"Name: {fn} {ln}".strip())
        if city: profile_bits.append(f"City: {city}")
        if diet: profile_bits.append(f"Diet: {diet}")
        if conds: profile_bits.append(f"Health conditions: {conds}")
    profile_text = "; ".join([p for p in profile_bits if p])

    system = (
        "You are a helpful nutrition & lifestyle assistant. "
        "Avoid medical diagnosis. Prefer low-GI ideas for diabetes, low-salt for hypertension, "
        "and soft/easy-to-swallow options if swallowing difficulties are present."
    )
    if profile_text:
        system += f" User profile: {profile_text}."

    resp = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": query.strip()}
        ],
        temperature=0.6,
        max_tokens=250,
    )
    return resp.choices[0].message.content.strip()

