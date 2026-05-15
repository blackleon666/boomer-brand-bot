import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from telegram import Update
from telegram.ext import ContextTypes
from db.repo import SessionLocal, get_or_create_user, create_order, get_order_status
from config import WHATSAPP_LINK

async def order(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    args = context.args
    
    if not args:
        await update.message.reply_text(
            "⚠️ Sipariş vermek için: `/siparis <urun_id>`\n\n"
            f"Ürün listesi için /katalog komutunu kullanın.\n\n"
            f"Direkt sipariş için: {WHATSAPP_LINK}",
            parse_mode='Markdown'
        )
        return
    
    try:
        product_id = int(args[0])
    except ValueError:
        await update.message.reply_text("❌ Geçersiz ürün ID!")
        return

    db = SessionLocal()
    try:
        user_db = get_or_create_user(db, user.id, user.username, user.first_name)
        order = create_order(db, user_db.id, product_id, 1)
        
        await update.message.reply_text(
            f"✅ *Sipariş Alındı!*\n\n"
            f"Sipariş No: `{order.id}`\n"
            f"Ürün ID: {product_id}\n\n"
            f"Siparişiniz yöneticiye iletildi. En kısa sürede WhatsApp üzerinden size dönüş yapılacak.\n\n"
            f"📱 Sipariş takip: {WHATSAPP_LINK}",
            parse_mode='Markdown'
        )
    except Exception as e:
        await update.message.reply_text(
            f"❌ Hata: {str(e)}\n\nDetaylı sipariş için: {WHATSAPP_LINK}"
        )
    finally:
        db.close()

async def order_status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    args = context.args
    if not args:
        await update.message.reply_text("Kullanım: `/durum <siparis_no>`")
        return
    
    try:
        order_id = int(args[0])
    except ValueError:
        await update.message.reply_text("❌ Geçersiz sipariş ID!")
        return

    db = SessionLocal()
    try:
        status = get_order_status(db, order_id)
        if status:
            await update.message.reply_text(f"📦 Sipariş `{order_id}` durumu: *{status}*", parse_mode='Markdown')
        else:
            await update.message.reply_text(f"❌ Sipariş `{order_id}` bulunamadı", parse_mode='Markdown')
    finally:
        db.close()