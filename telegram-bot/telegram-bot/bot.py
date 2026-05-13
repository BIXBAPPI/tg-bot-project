import requests
import time
import sqlite3
from datetime import datetime

TOKEN = "8760980789:AAE0iOE1G3Qbv5AD9uC-22Pz0g6butYalUU"
GROUP_ID = -1003509548150
PUBLISH_TIME = "10:00"

URL = f"https://api.telegram.org/bot{"8760980789:AAE0iOE1G3Qbv5AD9uC-22Pz0g6butYalUU"}"

# DB setup
conn = sqlite3.connect("bot.db", check_same_thread=False)
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


def send_message(chat_id, text):
    requests.post(URL + "/sendMessage", data={
        "chat_id": chat_id,
        "text": text
    })


def get_updates(offset=None):
    r = requests.get(URL + "/getUpdates", params={"offset": offset})
    return r.json()


def handle_message(msg):
    text = msg.get("text", "")
    user_id = msg["from"]["id"]

    if text == "/start":
        send_message(user_id, "Bot working 😭🔥\nUse:\n/submit name|account|link")

    elif text.startswith("/submit"):
        try:
            data = text.replace("/submit", "").strip().split("|")
            username = data[0].strip()
            account = data[1].strip()
            link = data[2].strip()

            cur.execute("INSERT INTO users VALUES (?,?,?,?,0,0)",
                        (user_id, username, account, link))
            conn.commit()

            send_message(user_id, "Saved 😭🔥")

        except:
            send_message(user_id, "Wrong format!\n/submit name|account|link")

    elif text == "/engaged":
        cur.execute("UPDATE users SET engaged=1, xp=xp+10 WHERE user_id=?", (user_id,))
        conn.commit()
        send_message(user_id, "XP +10 added 🔥")


def publish():
    cur.execute("SELECT username, account, link FROM users")
    rows = cur.fetchall()

    if not rows:
        return

    msg = "🔥 DAILY POSTS 🔥\n\n"

    for r in rows:
        msg += f"👤 {r[0]}\n📛 {r[1]}\n🔗 {r[2]}\n\n"

    send_message(-1003509548150, msg)


def check_time():
    now = datetime.now().strftime("%H:%M")
    if now == PUBLISH_TIME:
        publish()
        time.sleep(60)  # avoid duplicate


def main():
    offset = None

    while True:
        try:
            updates = get_updates(offset)

            for u in updates["result"]:
                offset = u["update_id"] + 1

                if "message" in u:
                    handle_message(u["message"])

            check_time()
            time.sleep(2)

        except Exception as e:
            print("Error:", e)
            time.sleep(5)


main()
