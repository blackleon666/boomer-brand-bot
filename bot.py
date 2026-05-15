import logging
import os
import sys
import threading
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
from db.repo import get_or_create_user, update_user_context

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

# ============================================
# ASIL SOHBET HANDLER - TÜM MESAJLARI YANITLAR
# ============================================
async def chat_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Tüm komut dışı mesajları işler - Ana AI Sohbet"""
    if not update.message or not update.message.text:
        return
    
    user_message = update.message.text.strip()
    user = update.effective_user
    
    # Kullanıcıyı veritabanına kaydet ve bağlamı güncelle
    try:
        db_user = get_or_create_user(
            context.bot.db_session, 
            user.id, 
            user.username, 
            user.first_name
        )
        # Kullanıcının konuşma geçmişini güncelle
        update_user_context(context.bot.db_session, user.id, user_message)
    except Exception as e:
        logger.warning(f"User update error: {e}")
    
    # Yazıyor göster
    await update.message.chat.send_action("typing")
    
    try:
        response = generate(user_message, user_id=user.id)
        await update.message.reply_text(response)
        logger.info(f"Chat response to user {user.id}")
        
        # Önemli mesajları yöneticiye raporla
        await report_to_admin(context, user, user_message, response)
        
    except Exception as e:
        logger.error(f"Chat error: {e}")
        await update.message.reply_text(
            f"🤖 Boomer Brand olarak şu anda size yanıt veremiyorum.\n\n"
            f"Detaylı yardım için: {WHATSAPP_LINK}"
        )

# ============================================
# YÖNETİCİYE RAPORLAMA
# ============================================
async def report_to_admin(context: ContextTypes.DEFAULT_TYPE, user, user_message: str, response: str):
    """Önemli mesajları @boomerbranddd kullanıcısına raporla"""
    # Sipariş, şikayet, potansiyel müşteri gibi anahtar kelimeler
    keywords = ["sipariş", "satın", "almak", "fiyat", "kampanya", "indirim", 
                "şikayet", "iade", "sorun", "yardım", "bilgi", "alabilir"]
    
    is_important = any(kw in user_message.lower() for kw in keywords)
    
    if is_important:
        try:
            report_text = f"""📢 *Yeni Lead/Rapor*
            
👤 *Kullanıcı:* {user.first_name or 'Bilinmiyor'} (@{user.username or 'yok'})
🆔 ID: `{user.id}`

💬 *Mesaj:* {user_message}

📝 *Yanıt:* {response[:200]}...

🔗 *WhatsApp:* {WHATSAPP_LINK}"""
            
            await context.bot.send_message(
                chat_id=TELEGRAM_GROUP_ID,
                text=report_text,
                parse_mode='Markdown'
            )
            logger.info(f"Report sent to admin for user {user.id}")
        except Exception as e:
            logger.error(f"Admin report error: {e}")

# ============================================
# BİLİNMEYEN KOMUT HANDLER
# ============================================
async def unknown_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Bilinmeyen komutlar için AI'a yönlendir"""
    if not update.message or not update.message.text:
        return
    
    user_message = update.message.text.strip()
    
    if user_message.startswith('/'):
        await update.message.chat.send_action("typing")
        response = generate(f"Kullanıcı şu komutu gönderdi: {user_message}. Bu komutu tanımadım. Uygun komutları açıkla.")
        await update.message.reply_text(response)

def main():
    if not TELEGRAM_TOKEN or TELEGRAM_TOKEN == "your_telegram_token_here":
        logger.error("Telegram token not set!")
        print("HATA: TELEGRAM_TOKEN ayarlanmadi!")
        return
    
    health_thread = threading.Thread(target=run_health_check_server, daemon=True)
    health_thread.start()
    
    # Application oluştur
    application = Application.builder().token(TELEGRAM_TOKEN).build()
    
    # Veritabanı için session oluştur
    from db.repo import SessionLocal
    db = SessionLocal()
    application.bot.db_session = db

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
    application.add_handler(CommandHandler("cancel", complaint.complaint_cancel))
    
    # /kampanya - Pazarlama
    application.add_handler(CommandHandler("kampanya", marketing.campaign))
    
    # /stats - İstatistikler
    application.add_handler(CommandHandler("stats", analytics.stats))
    
    # ===== MESAJ HANDLERS =====
    # Şikayet mesajlarını yakala (önce)
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, complaint.complaint_receive))
    
    # Ana sohbet handler (son)
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat_handler))
    
    # Bilinmeyen komutlar
    application.add_handler(MessageHandler(filters.COMMAND, unknown_handler))

    print(f"🤖 Boomer Brand Bot başladı!")
    print(f"   Telegram API: {telegram.__version__}")
    print(f"   Sohbet özelliği: AKTİF")
    print(f"   Yönetici raporu: {TELEGRAM_GROUP_ID}")
    
    application.run_polling()

if __name__ == '__main__':
    main()