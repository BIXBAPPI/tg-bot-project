TOKEN ="8760980789:AAH5EyTwRbLADjr52CL-IvoBGtQUo9TVS6Q"
GROUP_ID = -1003509548150
PUBLISH_TIME = "10:00"
import os
from dotenv import load_dotenv

load_dotenv()

# Telegram Bot Configuration
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN', 'your-telegram-token-here')

# Flask Configuration
FLASK_SECRET_KEY = os.getenv('FLASK_SECRET_KEY', 'your-secret-key-here')

# Database Configuration
DATABASE_PATH = os.getenv('DATABASE_PATH', 'bot_database.db')

# Environment
DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'
