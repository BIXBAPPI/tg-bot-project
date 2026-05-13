from flask import Flask
import sqlite3

app = Flask(__name__)

conn = sqlite3.connect("bot.db", check_same_thread=False)
cur = conn.cursor()

@app.route("/")
def home():

    cur.execute(
        "SELECT username, xp, submits, streak FROM users ORDER BY xp DESC LIMIT 10"
    )

    users = cur.fetchall()

    html = """

    <html>

    <head>

    <title>Dashboard</title>

    <meta name='viewport' content='width=device-width, initial-scale=1.0'>

    <style>

    body{
        background:#0f172a;
        color:white;
        font-family:Arial;
        padding:20px;
    }

    .card{
        background:#1e293b;
        padding:20px;
        border-radius:20px;
        margin-top:15px;
    }

    </style>

    </head>

    <body>

    <h1>😭🔥 Dashboard</h1>

    """

    rank = 1

    for u in users:

        html += f"""

        <div class='card'>

        <h2>#{rank} @{u[0]}</h2>

        <p>🔥 XP: {u[1]}</p>

        <p>📩 Submits: {u[2]}</p>

        <p>📅 Streak: {u[3]}</p>

        </div>

        """

        rank += 1

    html += """

    </body>

    </html>

    """

    return html

app.run(
    host="0.0.0.0",
    port=5000
)
