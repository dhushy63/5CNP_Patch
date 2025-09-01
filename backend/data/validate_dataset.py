
import os, sqlite3
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
DB_PATH = os.path.join(BASE_DIR, "data", "app.db")
conn = sqlite3.connect(DB_PATH)
c = conn.cursor()

users = c.execute("SELECT COUNT(*) FROM users").fetchone()[0]
cgm = c.execute("SELECT COUNT(*) FROM cgm").fetchone()[0]
mood = c.execute("SELECT COUNT(*) FROM mood").fetchone()[0]
print("Users:", users, "CGM rows:", cgm, "Mood rows:", mood)
