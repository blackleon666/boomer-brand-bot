import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from db.repo import SessionLocal, get_active_campaigns, add_campaign
from config import WHATSAPP_LINK, ADMIN_USER_IDS

async def campaign(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    
    if user.id not in ADMIN_USER_IDS:
        await update.message.reply_text(
            "⛔ Bu komutu kullanmak için yetkiniz yok.\n\n"
            "Bu komut sadece yöneticiler için geçerlidir."
        )
        return

    if context.args:
        campaign_message = ' '.join(context.args)
        db = SessionLocal()
        try:
            add_campaign(db, campaign_message)
            await update.message.reply_text(
                f"✅ *Yeni kampanya eklendi!*\n\n"
                f"📢 {campaign_message}\n\n"
                "Kampanya artık aktif ve tüm kullanıcılara gösterilecek.",
                parse_mode='Markdown'
            )
        except Exception as e:
            await update.message.reply_text(
                f"❌ Kampanya eklenirken bir hata oluştu: {str(e)}"
            )
        finally:
            db.close()
    else:
        db = SessionLocal()
        try:
            campaigns = get_active_campaigns(db)
        finally:
            db.close()

        if not campaigns:
            await update.message.reply_text(
                "📢 Şu anda aktif kampanya bulunmamaktadır.\n\n"
                "Yeni kampanya eklemek için:\n`/kampanya <kampanya mesajınız>`"
            )
            return

        message = "🎉 *Aktif Kampanyalar*\n\n"
        for idx, camp in enumerate(campaigns, 1):
            message += f"{idx}. {camp.message}\n\n"

        await update.message.reply_text(message, parse_mode='Markdown')