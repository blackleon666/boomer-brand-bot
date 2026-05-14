import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from db.repo import SessionLocal, get_or_create_user, log_complaint
from config import WHATSAPP_LINK

async def complaint_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📝 *Şikayet veya İade Bildirimi*\n\n"
        "Lütfen şikayetinizi veya iade talebinizi yazın.\n\n"
        "Örnek: 'Ürünüm lekeli geldi, iade etmek istiyorum.'\n\n"
        "İptal etmek için /cancel komutunu kullanabilirsiniz.",
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
            f"✅ *Şikayetiniz alınmıştır ve değerlendirilmektedir.*\n\n"
            f"🔖 Şikayet Takip No: `{complaint_id}`\n\n"
            f"Detaylı bilgi için WhatsApp'tan iletişime geçebilirsiniz:\n{WHATSAPP_LINK}\n\n"
            f"Teşekkür ederiz! Boomer Brand olarak size hizmet vermekten mutluluk duyuyoruz. 🙏",
            parse_mode='Markdown'
        )
    except Exception as e:
        await update.message.reply_text(
            f"❌ Şikayet kaydedilirken bir hata oluştu: {str(e)}\n\n"
            f"Lütfen daha sonra tekrar deneyin veya WhatsApp'tan iletişime geçin:\n{WHATSAPP_LINK}"
        )
    finally:
        db.close()
        context.user_data['awaiting_complaint'] = False

async def complaint_cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.user_data.get('awaiting_complaint'):
        await update.message.reply_text("❌ Şikayet bildirimi iptal edildi.")
        context.user_data['awaiting_complaint'] = False
    else:
        await update.message.reply_text("ℹ️ İptal edilecek bir işlem bulunamadı.")