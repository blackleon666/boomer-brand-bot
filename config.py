import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
HF_API_KEY = os.getenv("HF_API_KEY")
ENCRYPTION_KEY = os.getenv("ENCRYPTION_KEY")
DB_PATH = os.getenv("DB_PATH", os.path.join(basedir, "data", "boomer_bot.db"))
LOG_PATH = os.getenv("LOG_PATH", os.path.join(basedir, "logs", "chat.log.enc"))

# Admin IDs - hem numeric ID hem username destekler
admin_str = os.getenv("ADMIN_USER_IDS", "")
if admin_str:
    # Sayı olanları int olarak, username olanları string olarak tut
    ADMIN_USER_IDS = []
    ADMIN_USERNAMES = []
    for item in admin_str.split(","):
        item = item.strip()
        if item.isdigit():
            ADMIN_USER_IDS.append(int(item))
        elif item:
            ADMIN_USERNAMES.append(item.lower())
else:
    ADMIN_USER_IDS = []
    ADMIN_USERNAMES = []

WHATSAPP_LINK = os.getenv("WHATSAPP_LINK", "https://wa.me/boomermerter")
TELEGRAM_GROUP_ID = os.getenv("TELEGRAM_GROUP_ID", "@Boomerbrandd")
INSTAGRAM_LINK = os.getenv("INSTAGRAM_LINK", "https://www.instagram.com/boomermerter/")

# Admin kontrol fonksiyonu
def is_admin(user_id, username):
    """Kullanıcı admin mi kontrol eder"""
    if user_id in ADMIN_USER_IDS:
        return True
    if username and username.lower() in ADMIN_USERNAMES:
        return True
    return False