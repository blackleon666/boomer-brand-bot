import os
import sys

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from db.repo import SessionLocal, get_products, get_product_by_id
from config import WHATSAPP_LINK

async def catalog(update: Update, context: ContextTypes.DEFAULT_TYPE):
    db = SessionLocal()
    try:
        products = get_products(db)
    finally:
        db.close()

    if not products:
        await update.message.reply_text(
            "📦 Ürün kataloğu şu anda boş.\n\n"
            f"Lütfen daha sonra tekrar kontrol edin veya detaylı bilgi için WhatsApp'tan iletişime geçin:\n{WHATSAPP_LINK}\n\n"
            "ℹ️ Not: Ürün kataloğu, Boomer Brand'ın Telegram ve Instagram hesaplarından alınan gerçek ürünlerle doldurulmalıdır."
        )
        return

    message = "🛍️ *Boomer Brand Ürün Kataloğu*\n\n"
    keyboard = []
    for product in products:
        price_info = f" - {product.price_value} TL" if product.price_visible and product.price_value else " - Fiyat için WhatsApp"
        message += f"• {product.name}{price_info}\n"
        keyboard.append([InlineKeyboardButton(f"{product.name} - Detay", callback_data=f"product_{product.id}")])

    keyboard.append([InlineKeyboardButton("📱 WhatsApp ile İletişim", url=WHATSAPP_LINK)])
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(message, reply_markup=reply_markup, parse_mode='Markdown')

async def product_detail(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    product_id = int(query.data.split('_')[1])
    db = SessionLocal()
    try:
        product = get_product_by_id(db, product_id)
    finally:
        db.close()

    if not product:
        await query.edit_message_text("❌ Ürün bulunamadı.")
        return

    detail_message = f"🛍️ *{product.name}*\n\n"
    detail_message += f"{product.description}\n\n"
    if product.price_visible and product.price_value:
        detail_message += f"💰 Fiyat: {product.price_value} TL\n"
    else:
        detail_message += "💰 Fiyat: Detay için WhatsApp\n"
    detail_message += f"\n📍 Kaynak: {product.source.capitalize()} (Gönderi ID: {product.source_post_id})"

    keyboard = [
        [InlineKeyboardButton("🛒 Sipariş Ver", callback_data=f"order_{product.id}")],
        [InlineKeyboardButton("📱 WhatsApp ile İletişim", url=WHATSAPP_LINK)]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(detail_message, parse_mode='Markdown', reply_markup=reply_markup)