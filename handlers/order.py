import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from db.repo import SessionLocal, get_or_create_user, create_order, get_order_status
from config import WHATSAPP_LINK

async def order(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    args = context.args
    if not args:
        await update.message.reply_text(
            "⚠️ Lütfen sipariş vermek istediğiniz ürün ID'sini belirtin.\n\n"
            "Örnek: `/siparis 1`\n"
            "📦 Ürün listesini görmek için `/katalog` komutunu kullanabilirsiniz."
        )
        return
    try:
        product_id = int(args[0])
    except ValueError:
        await update.message.reply_text("❌ Ürün ID'si bir sayı olmalıdır.")
        return

    quantity = 1
    if len(args) > 1:
        try:
            quantity = int(args[1])
            if quantity <= 0:
                raise ValueError
        except ValueError:
            await update.message.reply_text("❌ Miktar pozitif bir tam sayı olmalıdır.")
            return

    db = SessionLocal()
    try:
        user_db = get_or_create_user(db, user.id, user.username, user.first_name)
        order = create_order(db, user_db.id, product_id, quantity)
        
        await update.message.reply_text(
            f"✅ *Siparişiniz alınmıştır!*\n\n"
            f"📋 Sipariş No: `{order.id}`\n"
            f"🛍️ Ürün ID: {product_id}\n"
            f"📦 Miktar: {quantity}\n"
            f"⏳ Durum: {order.status}\n\n"
            f"Sipariş durumunuzu öğrenmek için: `/durum {order.id}`\n\n"
            f"Detaylı bilgi için WhatsApp'tan iletişime geçebilirsiniz:\n{WHATSAPP_LINK}",
            parse_mode='Markdown'
        )
    except Exception as e:
        await update.message.reply_text(
            f"❌ Sipariş oluşturulurken bir hata oluştu: {str(e)}\n\n"
            f"Lütfen daha sonra tekrar deneyin veya WhatsApp'tan iletişime geçin:\n{WHATSAPP_LINK}"
        )
    finally:
        db.close()

async def order_status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    args = context.args
    if not args:
        await update.message.reply_text(
            "⚠️ Lütfen sorgulamak istediğiniz sipariş ID'sini belirtin.\n\n"
            "Örnek: `/durum 1`"
        )
        return
    try:
        order_id = int(args[0])
    except ValueError:
        await update.message.reply_text("❌ Sipariş ID'si bir sayı olmalıdır.")
        return

    db = SessionLocal()
    try:
        status = get_order_status(db, order_id)
        if status is None:
            await update.message.reply_text(
                f"❌ Sipariş No `{order_id}` bulunamadı.\n\n"
                f"Detaylı bilgi için WhatsApp'tan iletişime geçebilirsiniz:\n{WHATSAPP_LINK}"
            )
        else:
            await update.message.reply_text(
                f"📋 Sipariş No `{order_id}` durumu: *{status}*\n\n"
                f"Detaylı bilgi için WhatsApp'tan iletişime geçebilirsiniz:\n{WHATSAPP_LINK}",
                parse_mode='Markdown'
            )
    finally:
        db.close()