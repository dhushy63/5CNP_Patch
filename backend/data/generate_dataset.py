
import os, random, sqlite3
from datetime import datetime, timedelta
from faker import Faker

BASE_DIR = os.path.dirname(os.path.dirname(__file__))  # backend/
DB_PATH = os.path.join(BASE_DIR, "data", "app.db")

fake = Faker()

def ensure_db():
    os.makedirs(os.path.join(BASE_DIR, "data"), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
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
    conn.close()

def seed_users(n=100):
    diets = ["vegetarian", "non-vegetarian", "vegan"]
    cities = ["Chennai", "Mumbai", "Delhi", "Bengaluru", "Hyderabad", "Pune", "Kolkata"]
    conditions_list = [
        "Type 2 Diabetes", "Hypertension", "PCOS",
        "Hypothyroidism", "High Cholesterol", "Swallowing difficulties", "None"
    ]
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("DELETE FROM users")
    for i in range(1, n+1):
        fn = fake.first_name()
        ln = fake.last_name()
        city = random.choice(cities)
        diet = random.choice(diets)
        conds = random.sample(conditions_list, k=random.randint(1,2))
        if "None" in conds and len(conds) > 1:
            conds.remove("None")
        conditions = ", ".join(conds)
        cur.execute("INSERT INTO users(id, first_name, last_name, city, diet, conditions) VALUES(?,?,?,?,?,?)",
                    (i, fn, ln, city, diet, conditions))
    conn.commit(); conn.close()

def seed_cgm(n_users=100, days=7):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("DELETE FROM cgm")
    now = datetime.utcnow()
    for uid in range(1, n_users+1):
        for d in range(days):
            # 6 points per day
            for p in range(6):
                ts = (now - timedelta(days=(days-1-d), hours=(6-p))).isoformat()
                value = random.randint(80, 190)
                cur.execute("INSERT INTO cgm(user_id, ts, value) VALUES(?,?,?)", (uid, ts, value))
    conn.commit(); conn.close()

def seed_mood(n_users=100, entries=6):
    labels_cycle = ["calm", "tired", "happy", "focus", "stressed", "relaxed"]
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("DELETE FROM mood")
    now = datetime.utcnow()
    for uid in range(1, n_users+1):
        for i in range(entries):
            ts = (now - timedelta(hours=(entries-i))).isoformat()
            label = labels_cycle[i % len(labels_cycle)]
            score = random.randint(3, 9)
            cur.execute("INSERT INTO mood(user_id, ts, label, score) VALUES(?,?,?,?)", (uid, ts, label, score))
    conn.commit(); conn.close()

def main():
    ensure_db()
    seed_users(100)
    seed_cgm(100, 7)
    seed_mood(100, 6)
    print("Database seeded at", DB_PATH)

if __name__ == "__main__":
    main()
