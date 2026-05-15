import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from telegram import Update
from telegram.ext import ContextTypes
from db.repo import SessionLocal, get_or_create_user, log_complaint
from config import WHATSAPP_LINK

async def complaint_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📝 *Şikayet veya İade Bildirimi*\n\n"
        "Şikayetinizi yazın, yöneticiye iletilecektir.\n\n"
        "İptal etmek için /cancel kullanabilirsiniz.",
        parse_mode='Markdown'
    )
    context.user_data['awaiting_complaint'] = True

async def complaint_receive(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.user_data.get('awaiting_complaint'):
        return

    user = update.effective_user
    complaint_text = update.message.text

    db = SessionLocal()
    try:
        user_db = get_or_create_user(db, user.id, user.username, user.first_name)
        complaint_id = log_complaint(db, user_db.id, complaint_text)
        
        await update.message.reply_text(
            f"✅ *Şikayetiniz Alındı!*\n\n"
            f"Takip No: `{complaint_id}`\n\n"
            f"En kısa sürede yönetici tarafından incelenecektir.\n\n"
            f"Detaylı destek için: {WHATSAPP_LINK}",
            parse_mode='Markdown'
        )
    except Exception as e:
        await update.message.reply_text(f"❌ Hata: {str(e)}")
    finally:
        db.close()
        context.user_data['awaiting_complaint'] = False

async def complaint_cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.user_data.get('awaiting_complaint'):
        await update.message.reply_text("❌ Şikayet iptal edildi.")
        context.user_data['awaiting_complaint'] = False
    else:
        await update.message.reply_text("ℹ️ İptal edilecek işlem yok.")