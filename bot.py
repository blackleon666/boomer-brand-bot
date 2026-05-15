import logging
import os
import sys
import threading
import time
from http.server import HTTPServer, BaseHTTPRequestHandler

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import telegram
from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes

from config import TELEGRAM_TOKEN, WHATSAPP_LINK, INSTAGRAM_LINK, TELEGRAM_GROUP_ID
from handlers import start, catalog, order, complaint, marketing, analytics
from handlers.catalog import product_detail
from handlers.order import order_status
from handlers.complaint import complaint_start, complaint_receive, complaint_cancel
from handlers.marketing import campaign
from handlers.analytics import stats
from llm.inference import generate
import db.repo as db_repo

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# ============================================
# HEALTH CHECK SERVER
# ============================================
class HealthCheckHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(b'Boomer Brand Bot running 24/7!')
    
    def log_message(self, format, *args):
        pass

def run_health_check_server():
    port = int(os.getenv("PORT", 10000))
    while True:
        try:
            server = HTTPServer(('0.0.0.0', port), HealthCheckHandler)
            logger.info(f"Health check on port {port}")
            server.serve_forever()
        except Exception as e:
            logger.error(f"Health check error: {e}")
            time.sleep(5)

# ============================================
# SOHBET HANDLER
# ============================================
async def chat_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text:
        return
    
    user_message = update.message.text.strip()
    user = update.effective_user
    
    # Her istek için yeni session oluştur
    db = db_repo.SessionLocal()
    try:
        db_user = db_repo.get_or_create_user(db, user.id, user.username, user.first_name)
        db_repo.update_user_context(db, user.id, user_message)
    except Exception as e:
        logger.warning(f"User update error: {e}")
    finally:
        db.close()
    
    await update.message.chat.send_action("typing")
    
    try:
        response = generate(user_message, user_id=user.id)
        await update.message.reply_text(response)
        logger.info(f"Chat response to user {user.id}")
        
        # Yöneticiye rapor
        await report_to_admin(update, user, user_message, response)
        
    except Exception as e:
        logger.error(f"Chat error: {e}")
        await update.message.reply_text(f"🤖 Boomer Brand olarak şu anda yanıt veremiyorum.\n\nDetaylı yardım: {WHATSAPP_LINK}")

async def report_to_admin(update: Update, user, user_message: str, response: str):
    keywords = ["sipariş", "satın", "fiyat", "kampanya", "şikayet", "iade", "yardım", "bilgi", "alabilir"]
    is_important = any(kw in user_message.lower() for kw in keywords)
    
    if is_important:
        try:
            report_text = f"""📢 *Yeni Lead/Rapor*
            
👤 *Kullanıcı:* {user.first_name or 'Bilinmiyor'} (@{user.username or 'yok'})
🆔 ID: `{user.id}`

💬 *Mesaj:* {user_message}

📝 *Yanıt:* {response[:200]}..."""

            await update.bot.send_message(
                chat_id=TELEGRAM_GROUP_ID,
                text=report_text,
                parse_mode='Markdown'
            )
        except Exception as e:
            logger.error(f"Admin report error: {e}")

async def unknown_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text:
        return
    
    user_message = update.message.text.strip()
    if user_message.startswith('/'):
        await update.message.chat.send_action("typing")
        response = generate(f"Kullanıcı şu komutu gönderdi: {user_message}")
        await update.message.reply_text(response)

# ============================================
# RUN BOT
# ============================================
def run_bot():
    while True:
        try:
            if not TELEGRAM_TOKEN or TELEGRAM_TOKEN == "your_telegram_token_here":
                logger.error("Telegram token not set!")
                print("HATA: TELEGRAM_TOKEN ayarlanmadi!")
                time.sleep(10)
                continue
            
            application = Application.builder().token(TELEGRAM_TOKEN).build()

            # Handlers
            application.add_handler(CommandHandler("start", start.start))
            application.add_handler(CommandHandler("help", start.help_command))
            application.add_handler(CommandHandler("katalog", catalog.catalog))
            application.add_handler(CallbackQueryHandler(catalog.product_detail, pattern="^product_"))
            application.add_handler(CallbackQueryHandler(order.order, pattern="^order_"))
            application.add_handler(CommandHandler("siparis", order.order))
            application.add_handler(CommandHandler("durum", order.order_status))
            application.add_handler(CommandHandler("sikayet", complaint.complaint_start))
            application.add_handler(CommandHandler("cancel", complaint.complaint_cancel))
            application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, complaint.complaint_receive))
            application.add_handler(CommandHandler("kampanya", marketing.campaign))
            application.add_handler(CommandHandler("stats", analytics.stats))
            application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat_handler))
            application.add_handler(MessageHandler(filters.COMMAND, unknown_handler))

            print(f"🤖 Boomer Brand Bot başladı! (24/7 Mode)")
            print(f"   Telegram API: {telegram.__version__}")
            
            application.run_polling()
            
        except Exception as e:
            logger.error(f"Bot crashed: {e}")
            print(f"Bot hata verdi! 5 saniye içinde yeniden başlatılacak...")
            time.sleep(5)

def main():
    health_thread = threading.Thread(target=run_health_check_server, daemon=True)
    health_thread.start()
    run_bot()

if __name__ == '__main__':
    main()