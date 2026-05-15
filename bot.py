import logging
import os
import sys
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from telegram import Update, __version__ as TG_VER
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes
from config import TELEGRAM_TOKEN, WHATSAPP_LINK, INSTAGRAM_LINK
from handlers import start, catalog, order, complaint, marketing, analytics
from handlers.catalog import product_detail
from handlers.order import order_status
from handlers.complaint import complaint_start, complaint_receive, complaint_cancel
from handlers.marketing import campaign
from handlers.analytics import stats
from llm.inference import generate

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Health check handler for Render
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
    logger.info(f"Health check server running on port {port}")
    server.serve_forever()

# ============================================
# SOHBET HANDLER - YAPAY ZEKA DESTEĞİ
# ============================================
async def chat_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """AI Sohbet Handler - Tüm komut dışı mesajları işler"""
    if not update.message or not update.message.text:
        return
    
    user_message = update.message.text.strip()
    user = update.effective_user
    
    # Kullanıcıya yazıyor göster
    await update.message.chat.send_action("typing")
    
    try:
        # AI'dan yanıt al
        response = generate(user_message)
        
        # Yanıtı gönder
        await update.message.reply_text(response)
        
        logger.info(f"Chat response sent to user {user.id}")
        
    except Exception as e:
        logger.error(f"Chat error: {e}")
        await update.message.reply_text(
            f"Üzgünüm, şu anda bir sorun oluştu. Lütfen daha sonra tekrar deneyin.\n\n"
            f"Detaylı yardım için: {WHATSAPP_LINK}"
        )

# ============================================
# BİLİNMEYEN KOMUT HANDLER
# ============================================
async def unknown_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Bilinmeyen komutlar için AI'a yönlendir"""
    if not update.message or not update.message.text:
        return
    
    user_message = update.message.text.strip()
    user = update.effective_user
    
    # "/" ile başlayan ama tanımadığımız komutları AI'a yönlendir
    if user_message.startswith('/'):
        await update.message.chat.send_action("typing")
        response = generate(f"Kullanıcı şu komutu gönderdi: {user_message}. Bu komutu tanımadım. Uygun komutları açıkla.")
        await update.message.reply_text(response)
        return
    
    # Normalde buraya gelmez, ama güvenlik için
    await chat_handler(update, context)

# ============================================
# ANA FONKSİYON
# ============================================
def main():
    """Start the bot."""
    # Check if token is set
    if not TELEGRAM_TOKEN or TELEGRAM_TOKEN == "your_telegram_token_here":
        logger.error("Telegram token not set! Please configure .env file")
        print("HATA: Lütfen .env dosyasında TELEGRAM_TOKEN ayarlayın!")
        return
    
    # Start health check server in a separate thread
    health_thread = threading.Thread(target=run_health_check_server, daemon=True)
    health_thread.start()
    
    # Create the Application
    application = Application.builder().token(TELEGRAM_TOKEN).build()

    # ===== KOMUT HANDLERS =====
    # /start ve /help
    application.add_handler(CommandHandler("start", start.start))
    application.add_handler(CommandHandler("help", start.help_command))
    
    # /katalog - Ürün kataloğu
    application.add_handler(CommandHandler("katalog", catalog.catalog))
    application.add_handler(CallbackQueryHandler(catalog.product_detail, pattern="^product_"))
    application.add_handler(CallbackQueryHandler(order.order, pattern="^order_"))
    
    # /siparis ve /durum
    application.add_handler(CommandHandler("siparis", order.order))
    application.add_handler(CommandHandler("durum", order.order_status))
    
    # /sikayet - Şikayet
    application.add_handler(CommandHandler("sikayet", complaint.complaint_start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, complaint.complaint_receive))
    application.add_handler(CommandHandler("cancel", complaint.complaint_cancel))
    
    # /kampanya - Pazarlama
    application.add_handler(CommandHandler("kampanya", marketing.campaign))
    
    # /stats - İstatistikler
    application.add_handler(CommandHandler("stats", analytics.stats))
    
    # ===== SOHBET HANDLER - EN SON EKLE =====
    # Bu, diğer handler'lar eşleşmezse çalışır
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat_handler))

    # ===== UNKNOWN HANDLER =====
    # Bilinmeyen komutlar için
    application.add_handler(MessageHandler(filters.COMMAND, unknown_handler))

    # Start the Bot
    logger.info("Boomer Brand bot başlatıldı!")
    print(f"🤖 Boomer Brand Bot çalışıyor... (Telegram API v{TG_VER})")
    print(f"💬 Sohbet özelliği aktif!")
    application.run_polling()

if __name__ == '__main__':
    main()