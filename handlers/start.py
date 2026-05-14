import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from config import WHATSAPP_LINK

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    welcome_message = (
        f"👋 Merhaba {user.first_name}!\n\n"
        "Boomer Brand müşteri temsilcisi olarak size nasıl yardımcı olabilirim? 🤖\n\n"
        "📋 *Kullanılabilir Komutlar:*\n\n"
        "/start - Botu başlat\n"
        "/help - Yardım menüsü\n"
        "/katalog - Ürün kataloğunu görüntüle\n"
        "/siparis <ürün_id> - Ürün siparişi ver\n"
        "/durum <siparis_no> - Sipariş durumunu sorgula\n"
        "/sikayet - Şikayet veya iade bildir\n"
        "/kampanya - Kampanyaları görüntüle (yöneticiler)\n"
        "/stats - İstatistikleri görüntüle\n\n"
        f"💡 *Fiyat, stok ve kampanya detayları için WhatsApp'tan iletişime geçebilirsiniz:*\n{WHATSAPP_LINK}"
    )
    keyboard = [
        [InlineKeyboardButton("🛍️ Ürün Kataloğu", callback_data='catalog')],
        [InlineKeyboardButton("📱 WhatsApp ile İletişim", url=WHATSAPP_LINK)]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(welcome_message, reply_markup=reply_markup, parse_mode='Markdown')

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await start(update, context)