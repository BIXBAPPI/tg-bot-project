import requests
import time
import sqlite3
from datetime import datetime
from flask import Flask
from threading import Thread


# Flask keep alive
app = Flask('')

@app.route('/')
def home():
    return "Bot Alive 🔥"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

# CONFIG

TOKEN = "8760980789:AAH5EyTwRbLADjr52CL-IvoBGtQUo9TVS6Q"

URL = f"https://api.telegram.org/bot{TOKEN}"

PUBLISH_GROUP = -1003509548150

# DATABASE

conn = sqlite3.connect("bot.db", check_same_thread=False)
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY,
    username TEXT,
    xp INTEGER DEFAULT 0,
    submits INTEGER DEFAULT 0,
    streak INTEGER DEFAULT 0,
    last_daily TEXT DEFAULT ''
)
""")

conn.commit()

# FUNCTIONS

def send_message(chat_id, text):

    requests.post(
        URL + "/sendMessage",
        data={
            "chat_id": chat_id,
            "text": text
        }
    )

def get_updates(offset=None):

    return requests.get(
        URL + "/getUpdates",
        params={"offset": offset}
    ).json()

def add_user(user_id, username):

    cur.execute(
        "INSERT OR IGNORE INTO users (user_id, username) VALUES (?, ?)",
        (user_id, username)
    )

    conn.commit()


# BOT START


print("Bot running 😭🔥")

offset = None

while True:

    updates = get_updates(offset)

    print(updates)

    if "result" in updates:

        for u in updates["result"]:

            offset = u["update_id"] + 1

            if "message" not in u:
                continue

            msg = u["message"]

            text = msg.get("text", "")
            chat_id = msg["chat"]["id"]

            user_id = msg["from"]["id"]

            username = msg["from"].get(
                "username",
                "NoUsername"
            )

            add_user(user_id, username)

            # START

            if text == "/start":

                send_message(
                    chat_id,
                    "🔥 Engagement Bot Active\n\nCommands:\n/start\n/submit LINK\n/me\n/leaderboard\n/daily"
                )

            # SUBMIT

            elif text.startswith("/submit"):

                parts = text.split(" ", 1)

                if len(parts) < 2:

                    send_message(
                        chat_id,
                        "❌ Use:\n/submit LINK"
                    )

                else:

                    link = parts[1]

                    cur.execute(
                        "UPDATE users SET xp = xp + 10, submits = submits + 1 WHERE user_id=?",
                        (user_id,)
                    )

                    conn.commit()

                    send_message(
                        PUBLISH_GROUP,
                        f"🔥 NEW SUBMISSION\n\n👤 @{username}\n🔗 {link}"
                    )

                    send_message(
                        chat_id,
                        "✅ Submission Added\n🔥 +10 XP"
                    )

            # PROFILE

            elif text == "/me":

                cur.execute(
                    "SELECT xp, submits, streak FROM users WHERE user_id=?",
                    (user_id,)
                )

                data = cur.fetchone()

                xp = data[0]
                submits = data[1]
                streak = data[2]

                send_message(
                    chat_id,
                    f"👤 @{username}\n\n🔥 XP: {xp}\n📩 Submits: {submits}\n📅 Streak: {streak}"
                )

            # LEADERBOARD

            elif text == "/leaderboard":

                cur.execute(
                    "SELECT username, xp FROM users ORDER BY xp DESC LIMIT 10"
                )
                rows = cur.fetchall()

                board = "🏆 LEADERBOARD\n\n"

                rank = 1

                for r in rows:

                    board += f"{rank}. @{r[0]} — {r[1]} XP\n"

                    rank += 1

                send_message(chat_id, board)

            # DAILY

            elif text == "/daily":

                today = str(datetime.now().date())

                cur.execute(
                    "SELECT last_daily, streak FROM users WHERE user_id=?",
                    (user_id,)
                )

                data = cur.fetchone()

                last_daily = data[0]
                streak = data[1]

                if last_daily == today:

                    send_message(
                        chat_id,
                        "❌ Daily already claimed today"
                    )

                else:

                    streak += 1

                    cur.execute(
                        "UPDATE users SET xp = xp + 20, streak=?, last_daily=? WHERE user_id=?",
                        (streak, today, user_id)
                    )

                    conn.commit()

                    send_message(
                        chat_id,
                        f"🔥 Daily Claimed\n+20 XP\n📅 Streak: {streak}"
                    )

    time.sleep(2)

if __name__ == "__main__":
    keep_alive()

import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from config import TELEGRAM_TOKEN
from db import Database

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

db = Database()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    db.add_user(user.id, user.first_name, user.username)
    await update.message.reply_html(
        rf"Hi {user.mention_html()}! Welcome to the bot."
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    help_text = """
    /start - Start the bot
    /help - Show this help message
    /stats - Show your statistics
    """
    await update.message.reply_text(help_text)

async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Show user statistics."""
    user_id = update.effective_user.id
    stats = db.get_user_stats(user_id)
    await update.message.reply_text(f"Your stats: {stats}")

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Echo the user message."""
    await update.message.reply_text(update.message.text)

def main() -> None:
    """Start the bot."""
    application = Application.builder().token(TELEGRAM_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("stats", stats))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()
 
