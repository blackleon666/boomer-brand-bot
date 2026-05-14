import logging
import os
import sys

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from telegram import __version__ as TG_VER
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters
from config import TELEGRAM_TOKEN, WHATSAPP_LINK
from handlers import start, catalog, order, complaint, marketing, analytics
from handlers.catalog import product_detail
from handlers.order import order_status
from handlers.complaint import complaint_start, complaint_receive, complaint_cancel
from handlers.marketing import campaign
from handlers.analytics import stats

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

async def unknown(update, context):
    await update.message.reply_text(
        "Üzgünüm, bu komutu anlayamadım. Kullanabileceğiniz komutlar:\n"
        "/start - Botu başlat\n"
        "/help - Yardım\n"
        "/katalog - Ürün kataloğu\n"
        "/siparis <ürün_id> [miktar] - Sipariş ver\n"
        "/durum <siparis_no> - Sipariş durumu\n"
        "/sikayet - Şikayet bildir\n"
        "/kampanya - Kampanyaları görüntüle / yeni kampanya ekle (yöneticiler)\n"
        "/stats - İstatistikler\n"
        f"Detaylı bilgi için WhatsApp'tan iletişime geçebilirsiniz: {WHATSAPP_LINK}"
    )

def main():
    """Start the bot."""
    # Check if token is set
    if not TELEGRAM_TOKEN or TELEGRAM_TOKEN == "your_telegram_token_here":
        logger.error("Telegram token not set! Please configure .env file")
        print("HATA: Lütfen .env dosyasında TELEGRAM_TOKEN ayarlayın!")
        return
    
    # Create the Application
    application = Application.builder().token(TELEGRAM_TOKEN).build()

    # Add handlers
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

    # Handle unknown commands
    application.add_handler(MessageHandler(filters.COMMAND, unknown))

    # Start the Bot
    logger.info("Boomer Brand bot başlatıldı!")
    print(f"🤖 Boomer Brand Bot çalışıyor... (Telegram API v{TG_VER})")
    application.run_polling()

if __name__ == '__main__':
    main()