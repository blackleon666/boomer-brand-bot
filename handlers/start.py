import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from config import WHATSAPP_LINK, INSTAGRAM_LINK

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    
    welcome_message = (
        f"👋 Merhaba {user.first_name}!\n\n"
        "🤖 *Boomer Brand müşteri temsilcisi* olarak size yardımcı olmaktan mutluluk duyorum!\n\n"
        "📋 *Komutlar:*\n"
        "• /start - Botu başlat\n"
        "• /help - Yardım menüsü\n"
        "• /katalog - Ürün kataloğu\n"
        "• /siparis <id> - Sipariş ver\n"
        "• /durum <no> - Sipariş takibi\n"
        "• /sikayet - Şikayet bildir\n"
        "• /stats - İstatistikler\n\n"
        "💬 *Sohbet:* Bana herhangi bir şey sorabilirsiniz, size yardımcı olacağım!\n\n"
        f"📱 *İletişim:*\n"
        f"WhatsApp: {WHATSAPP_LINK}\n"
        f"Instagram: {INSTAGRAM_LINK}\n"
        f"Telegram: @Boomerbrandd\n\n"
        "Hoş geldiniz! 👋"
    )
    
    keyboard = [
        [InlineKeyboardButton("🛍️ Ürün Kataloğu", callback_data='catalog')],
        [InlineKeyboardButton("📱 WhatsApp", url=WHATSAPP_LINK)],
        [InlineKeyboardButton("📸 Instagram", url=INSTAGRAM_LINK)]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(welcome_message, reply_markup=reply_markup, parse_mode='Markdown')

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await start(update, context)