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

# Debug logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

print("="*50)
print("BOOMER BRAND BOT YUKLENIYOR...")
print("="*50)

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
# ANA CHAT HANDLER - TUM MESAJLARI YANITLAR
# ============================================
async def chat_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Tüm metin mesajlarını işleyen ana AI handler"""
    
    # Mesaj kontrolü
    if not update.message or not update.message.text:
        return
    
    message_text = update.message.text.strip()
    user = update.effective_user
    
    print(f"[CHAT] User {user.id} (@{user.username}): {message_text}")
    
    # Önce kullanıcıyı kaydet
    db = db_repo.SessionLocal()
    try:
        db_user = db_repo.get_or_create_user(db, user.id, user.username, user.first_name)
        db_repo.update_user_context(db, user.id, message_text)
        print(f"[DB] User saved/updated: {user.id}")
    except Exception as e:
        print(f"[DB] Error: {e}")
    finally:
        db.close()
    
    # Kullanıcıya yazıyor göster
    try:
        await update.message.chat.send_action("typing")
    except:
        pass
    
    # AI'dan yanıt al
    try:
        response = generate(message_text, user_id=user.id)
        print(f"[AI] Response: {response[:100]}...")
        
        # Yanıtı gönder
        await update.message.reply_text(response)
        print(f"[SENT] Response to user {user.id}")
        
        # Yöneticiye rapor (önemli mesajlar)
        await report_to_admin(update, user, message_text, response)
        
    except Exception as e:
        print(f"[ERROR] Chat error: {e}")
        logger.error(f"Chat error: {e}")
        try:
            await update.message.reply_text(
                f"🤖 Boomer Brand olarak şu anda size yanıt veremiyorum.\n\n"
                f"Detaylı yardım için: {WHATSAPP_LINK}"
            )
        except:
            pass

async def report_to_admin(update: Update, user, user_message: str, response: str):
    """Önemli mesajları yöneticiye raporla"""
    important_keywords = ["sipariş", "satın", "fiyat", "kampanya", "indirim", "şikayet", "iade", "yardım", "bilgi", "alabilir", "almak", "vermek"]
    is_important = any(kw in user_message.lower() for kw in important_keywords)
    
    if is_important:
        try:
            report = f"""📢 *Yeni Lead/Rapor*

👤 *Kullanıcı:* {user.first_name or 'Bilinmiyor'} (@{user.username or 'yok'})
🆔 ID: `{user.id}`

💬 *Mesaj:* {user_message}

📝 *Yanıt:* {response[:200]}..."""

            await update.bot.send_message(
                chat_id=TELEGRAM_GROUP_ID,
                text=report,
                parse_mode='Markdown'
            )
            print(f"[REPORT] Sent to admin")
        except Exception as e:
            print(f"[REPORT] Error: {e}")

# ============================================
# BİLİNMEYEN KOMUT HANDLER
# ============================================
async def unknown_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Bilinmeyen komutları AI'a yönlendir"""
    if not update.message or not update.message.text:
        return
    
    message_text = update.message.text.strip()
    if message_text.startswith('/'):
        await update.message.chat.send_action("typing")
        response = generate(f"Kullanıcı şu komutu gönderdi: {message_text}. Bu komutu tanımıyorum. Uygun komutları açıkla.")
        await update.message.reply_text(response)

# ============================================
# BOT ÇALIŞTIRMA
# ============================================
def run_bot():
    while True:
        try:
            if not TELEGRAM_TOKEN or TELEGRAM_TOKEN == "your_telegram_token_here":
                logger.error("Telegram token not set!")
                print("❌ HATA: TELEGRAM_TOKEN ayarlanmadi!")
                print("   Lütfen .env dosyasını düzenleyin")
                time.sleep(10)
                continue
            
            print("✅ Telegram token ok")
            
            application = Application.builder().token(TELEGRAM_TOKEN).build()
            print("✅ Application oluşturuldu")

            # ===== HANDLER SIRALAMASI ÖNEMLI! =====
            # Önce command handler'lar
            application.add_handler(CommandHandler("start", start.start))
            application.add_handler(CommandHandler("help", start.help_command))
            application.add_handler(CommandHandler("katalog", catalog.catalog))
            application.add_handler(CommandHandler("siparis", order.order))
            application.add_handler(CommandHandler("durum", order.order_status))
            application.add_handler(CommandHandler("sikayet", complaint.complaint_start))
            application.add_handler(CommandHandler("cancel", complaint.complaint_cancel))
            application.add_handler(CommandHandler("kampanya", marketing.campaign))
            application.add_handler(CommandHandler("stats", analytics.stats))
            
            # Callback query handler
            application.add_handler(CallbackQueryHandler(catalog.product_detail, pattern="^product_"))
            application.add_handler(CallbackQueryHandler(order.order, pattern="^order_"))
            
            # Mesaj handler - şikayet akışı
            application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, complaint.complaint_receive))
            
            # ANA AI CHAT HANDLER - EN SONDA
            application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat_handler))
            
            # Bilinmeyen komutlar
            application.add_handler(MessageHandler(filters.COMMAND, unknown_handler))

            print("="*50)
            print("🤖 BOOMER BRAND BOT AKTIF!")
            print("   Telegram API: {}".format(telegram.__version__))
            print("   AI: HuggingFace Mistral/Llama")
            print("   Mode: 24/7 Polling")
            print("="*50)
            
            application.run_polling()
            
        except Exception as e:
            logger.error(f"Bot crashed: {e}")
            print(f"❌ Bot hata verdi: {e}")
            print("   5 saniye içinde yeniden başlatılacak...")
            time.sleep(5)

def main():
    # Health check
    health_thread = threading.Thread(target=run_health_check_server, daemon=True)
    health_thread.start()
    print("✅ Health check server başlatıldı")
    
    # Bot
    run_bot()

if __name__ == '__main__':
    main()