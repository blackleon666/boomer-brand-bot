import logging
import os
import sys
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import telegram
from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes

from config import TELEGRAM_TOKEN, WHATSAPP_LINK, INSTAGRAM_LINK
from handlers import start, catalog, order, complaint, marketing, analytics
from handlers.catalog import product_detail
from handlers.order import order_status
from handlers.complaint import complaint_start, complaint_receive, complaint_cancel
from handlers.marketing import campaign
from handlers.analytics import stats
from llm.inference import generate

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

class HealthCheckHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(b'Boomer Brand Bot is running!')
    
    def log_message(self, format, *args):
        pass

def run_health_check_server():
    port = int(os.getenv("PORT", 10000))
    server = HTTPServer(('0.0.0.0', port), HealthCheckHandler)
    logger.info(f"Health check on port {port}")
    server.serve_forever()

async def chat_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text:
        return
    
    user_message = update.message.text.strip()
    user = update.effective_user
    
    await update.message.chat.send_action("typing")
    
    try:
        response = generate(user_message)
        await update.message.reply_text(response)
        logger.info(f"Chat response to user {user.id}")
    except Exception as e:
        logger.error(f"Chat error: {e}")
        await update.message.reply_text(
            f"Uzgunum, su anda bir sorun oldu. Lutfen daha sonra deneyin.\n\nYardim icin: {WHATSAPP_LINK}"
        )

async def unknown_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text:
        return
    
    user_message = update.message.text.strip()
    
    if user_message.startswith('/'):
        await update.message.chat.send_action("typing")
        response = generate(f"Kullanici su komutu gonderdi: {user_message}. Bu komutu tanimadim.")
        await update.message.reply_text(response)

def main():
    if not TELEGRAM_TOKEN or TELEGRAM_TOKEN == "your_telegram_token_here":
        logger.error("Telegram token not set!")
        print("HATA: TELEGRAM_TOKEN ayarlanmadi!")
        return
    
    health_thread = threading.Thread(target=run_health_check_server, daemon=True)
    health_thread.start()
    
    application = Application.builder().token(TELEGRAM_TOKEN).build()

    application.add_handler(CommandHandler("start", start.start))
    application.add_handler(CommandHandler("help", start.help_command))
    application.add_handler(CommandHandler("katalog", catalog.catalog))
    application.add_handler(CallbackQueryHandler(catalog.product_detail, pattern="^product_"))
    application.add_handler(CallbackQueryHandler(order.order, pattern="^order_"))
    application.add_handler(CommandHandler("siparis", order.order))
    application.add_handler(CommandHandler("durum", order.order_status))
    application.add_handler(CommandHandler("sikayet", complaint.complaint_start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, complaint.complaint_receive))
    application.add_handler(CommandHandler("cancel", complaint.complaint_cancel))
    application.add_handler(CommandHandler("kampanya", marketing.campaign))
    application.add_handler(CommandHandler("stats", analytics.stats))

    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat_handler))
    application.add_handler(MessageHandler(filters.COMMAND, unknown_handler))

    print(f"🤖 Boomer Brand Bot basladi!")
    print(f"   Telegram API: {telegram.__version__}")
    application.run_polling()

if __name__ == '__main__':
    main()
