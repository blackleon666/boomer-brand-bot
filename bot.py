import logging
import os
import sys
import threading
import time
from http.server import HTTPServer, BaseHTTPRequestHandler

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes

from config import TELEGRAM_TOKEN, WHATSAPP_LINK
from handlers import start, catalog, order, complaint, marketing, analytics
from handlers.catalog import product_detail
from handlers.order import order_status
from llm.inference import generate
import db.repo as db_repo

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

print("="*50)
print("BOOMER BRAND BOT")
print("="*50)

# Health server
class HealthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(b'OK')
    def log_message(self, *args):
        pass

def run_health():
    try:
        port = int(os.getenv("PORT", 10000))
        HTTPServer(('0.0.0.0', port), HealthHandler).serve_forever()
    except:
        pass

threading.Thread(target=run_health, daemon=True).start()

# ============================================================
# SOHBET HANDLER - ANA MESAJ ISLEYICI
# ============================================================
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """TUM metin mesajlarini yakalar"""
    
    if not update.message or not update.message.text:
        return
    
    msg = update.message.text.strip()
    user = update.effective_user
    
    print(f"[{user.id}] {msg}")
    
    # Sikayet modunda mi?
    if context.user_data.get('awaiting_complaint'):
        await complaint.complaint_receive(update, context)
        return
    
    # Yaziyor göster
    try:
        await update.message.chat.send_action("typing")
    except:
        pass
    
    # AI yanit - Markdown destekli
    try:
        response = generate(msg, user_id=user.id)
        await update.message.reply_text(response, parse_mode='Markdown')
        print(f"[BOT] {response[:30]}...")
    except Exception as e:
        print(f"[ERROR] {e}")
        await update.message.reply_text(f"Su anda calismiyor. WhatsApp: {WHATSAPP_LINK}")

# ============================================================
# MAIN
# ============================================================
def main():
    if not TELEGRAM_TOKEN:
        print("HATA: Token yok!")
        return
    
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    
    # Command handlers
    app.add_handler(CommandHandler("start", start.start))
    app.add_handler(CommandHandler("help", start.help_command))
    app.add_handler(CommandHandler("katalog", catalog.catalog))
    app.add_handler(CommandHandler("siparis", order.order))
    app.add_handler(CommandHandler("durum", order.order_status))
    app.add_handler(CommandHandler("sikayet", complaint.complaint_start))
    app.add_handler(CommandHandler("cancel", complaint.complaint_cancel))
    app.add_handler(CommandHandler("kampanya", marketing.campaign))
    app.add_handler(CommandHandler("stats", analytics.stats))
    
    # Callback
    app.add_handler(CallbackQueryHandler(product_detail, pattern="^product_"))
    app.add_handler(CallbackQueryHandler(order.order, pattern="^order_"))
    
    # MESAJ HANDLER - EN ONEMLI!
    # filters.TEXT & ~filters.COMMAND ile komut olmayan tum mesajlari yakala
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    print("="*50)
    print("BOT AKTIF!")
    print("="*50)
    
    app.run_polling()

if __name__ == '__main__':
    main()