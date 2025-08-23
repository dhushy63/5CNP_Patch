
from pydantic import BaseModel
from typing import List, Optional

class GreetResponse(BaseModel):
    name: str
    city: str
    diet: str = ""
    conditions: List[str] = []
    latest_cgm: Optional[float] = None
    message: str

class CGMPoint(BaseModel):
    ts: str
    value: float

class MoodPoint(BaseModel):
    label: str
    score: int

class FoodLogIn(BaseModel):
    user_id: int
    description: str

class InterruptIn(BaseModel):
    user_id: int
    query: str
