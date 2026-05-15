import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from telegram import Update
from telegram.ext import ContextTypes
from db.repo import SessionLocal, get_active_campaigns, add_campaign
from config import WHATSAPP_LINK, is_admin

async def campaign(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    
    # Admin kontrolü - hem ID hem username ile
    if not is_admin(user.id, user.username):
        await update.message.reply_text("⛔ Bu komut sadece yöneticiler için!")
        return

    args = context.args
    if args:
        campaign_message = ' '.join(args)
        db = SessionLocal()
        try:
            add_campaign(db, campaign_message)
            await update.message.reply_text(f"✅ Kampanya eklendi:\n\n{campaign_message}")
        finally:
            db.close()
    else:
        db = SessionLocal()
        try:
            campaigns = get_active_campaigns(db)
        finally:
            db.close()

        if not campaigns:
            await update.message.reply_text("📢 Aktif kampanya yok.")
        else:
            msg = "🎉 *Aktif Kampanyalar*\n\n"
            for c in campaigns:
                msg += f"• {c.message}\n"
            await update.message.reply_text(msg, parse_mode='Markdown')