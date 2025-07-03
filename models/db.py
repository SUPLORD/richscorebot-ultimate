import sqlite3
def init_db():
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute("""
      CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY, name TEXT, goal TEXT,
        amount INTEGER, monthly INTEGER, risk TEXT
      )""")
    conn.commit()
    conn.close()
