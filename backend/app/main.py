
from fastapi import FastAPI, Body
from fastapi.middleware.cors import CORSMiddleware
from typing import Dict
from .schemas import GreetResponse, FoodLogIn, InterruptIn
from .agents.greet_agent import greet
from .agents.interrupt_agent import respond as interrupt_respond
from .services.cgm import list_recent_cgm, latest_cgm
from .services.mood import list_recent_mood
from .services.food import add_food, list_recent_food
from .services.mealplan import build_meal_plan
from .db import get_conn

app = FastAPI(title="dhushy63AI API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health():
    return {"ok": True}

@app.get("/greet", response_model=GreetResponse)
def route_greet(user_id: int = 1):
    info = greet(user_id)
    info["latest_cgm"] = latest_cgm(user_id)
    return info

@app.get("/cgm/recent")
def cgm_recent(user_id: int = 1):
    return {"series": list_recent_cgm(user_id)}

@app.get("/mood/recent")
def mood_recent(user_id: int = 1):
    return {"series": list_recent_mood(user_id)}

@app.post("/food")
def log_food(item: FoodLogIn):
    return add_food(item.user_id, item.description)

@app.get("/food/recent")
def food_recent(user_id: int = 1):
    return {"items": list_recent_food(user_id)}

@app.get("/meal-plan")
def meal_plan(user_id: int = 1):
    return build_meal_plan(user_id)

@app.post("/interrupt")
def interrupt(payload: InterruptIn):
    return interrupt_respond(payload.user_id, payload.query)

# --- create tables if missing (idempotent) ---
@app.on_event("startup")
def init_db():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY,
        first_name TEXT, last_name TEXT, city TEXT,
        diet TEXT, conditions TEXT
    )""")
    cur.execute("""CREATE TABLE IF NOT EXISTS cgm(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER, ts TEXT, value REAL
    )""")
    cur.execute("""CREATE TABLE IF NOT EXISTS mood(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER, ts TEXT, label TEXT, score INTEGER
    )""")
    cur.execute("""CREATE TABLE IF NOT EXISTS food(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER, ts TEXT, description TEXT
    )""")
    conn.commit()
"""
Run data/generate_dataset.py once to seed the DB.
"""

