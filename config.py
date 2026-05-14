import os
from dotenv import load_dotenv

# Get the directory of this file
basedir = os.path.abspath(os.path.dirname(__file__))
# Load .env from the project root
load_dotenv(os.path.join(basedir, '.env'))

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
HF_API_KEY = os.getenv("HF_API_KEY")
ENCRYPTION_KEY = os.getenv("ENCRYPTION_KEY")
DB_PATH = os.getenv("DB_PATH", os.path.join(basedir, "data", "boomer_bot.db"))
LOG_PATH = os.getenv("LOG_PATH", os.path.join(basedir, "logs", "chat.log.enc"))
ADMIN_USER_IDS = [int(x) for x in os.getenv("ADMIN_USER_IDS", "").split(",") if x.strip().isdigit()]
WHATSAPP_LINK = os.getenv("WHATSAPP_LINK", "https://wa.me/boomermerter")
TELEGRAM_GROUP_ID = os.getenv("TELEGRAM_GROUP_ID", "@Boomerbrandd")