import sqlite3

conn = sqlite3.connect("bot.db")
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER,
    username TEXT,
    account TEXT,
    link TEXT,
    engaged INTEGER DEFAULT 0,
    xp INTEGER DEFAULT 0
)
""")

conn.commit()
conn.close()
def init_db():
    conn = sqlite3.connect("bot.db")
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER,
        username TEXT,
        account TEXT,
        link TEXT,
        engaged INTEGER DEFAULT 0,
        xp INTEGER DEFAULT 0
    )
    """)

    conn.commit()
    conn.close()

init_db()
