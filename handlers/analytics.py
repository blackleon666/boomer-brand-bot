import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from telegram import Update
from telegram.ext import ContextTypes
from db.repo import SessionLocal
from db.models import User, Order, Complaint, Product
from config import WHATSAPP_LINK

async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    db = SessionLocal()
    try:
        user_count = db.query(User).count()
        order_count = db.query(Order).count()
        complaint_count = db.query(Complaint).count()
        product_count = db.query(Product).count()
        
        # Aktif kullanıcılar (son 24 saatte)
        from datetime import datetime, timedelta
        yesterday = datetime.now() - timedelta(days=1)
        active_users = db.query(User).filter(User.last_interaction >= yesterday).count()
    finally:
        db.close()

    await update.message.reply_text(
        f"📊 *Boomer Brand İstatistikleri*\n\n"
        f"👥 Toplam Kullanıcı: {user_count}\n"
        f"⏰ Aktif Kullanıcılar: {active_users}\n"
        f"📦 Toplam Sipariş: {order_count}\n"
        f"📝 Toplam Şikayet: {complaint_count}\n"
        f"🛍️ Toplam Ürün: {product_count}\n\n"
        f"Detaylı bilgi: {WHATSAPP_LINK}",
        parse_mode='Markdown'
    )