"""
BOOMER BRAND TELEGRAM BOT - V4 FINAL
=====================================
Yönetici: @boomerbranddd (ID: 5832042754)
"""

import os
import sys
import logging
import random
import string

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, CallbackQueryHandler
from dotenv import load_dotenv

load_dotenv()

from config import TELEGRAM_TOKEN, is_admin, WHATSAPP_LINK, INSTAGRAM_LINK, TELEGRAM_GROUP_ID
from db.repo import init_db, add_user, add_product, get_product, get_all_products, get_campaign_products, create_order, get_order, get_user_orders, update_order_status, confirm_payment, reject_payment, set_tracking_code, add_feedback, get_new_feedback, mark_feedback_read, add_stat, get_stats

# Initialize database
init_db()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

print(f"Bot baslatiliyor...")

# ============================================================
# SABITLER
# ============================================================

BRAND = {
    "whatsapp": WHATSAPP_LINK,
    "instagram": INSTAGRAM_LINK,
    "telegram": "@Boomerbrandd",
    "telegram_group": TELEGRAM_GROUP_ID
}

PAYMENT_INFO = """
ODEME BILGILERI:

Banka: Ziraat Bankasi
IBAN: TR12 0000 0000 0000 0000 0000
Hesap Sahibi: Boomer Brand

NOT: Aciklama kismina sipariş kodunuzu yazmayin!
"""

# ============================================================
# YARDIMCI FONKSİYONLAR
# ============================================================

def generate_order_id() -> str:
    return "BB" + "".join(random.choices(string.ascii_uppercase + string.digits, k=8))


async def send_to_admin(context: ContextTypes.DEFAULT_TYPE, message: str):
    """Yöneticiye mesaj gönder"""
    from config import ADMIN_USER_IDS
    if ADMIN_USER_IDS:
        try:
            await context.bot.send_message(ADMIN_USER_IDS[0], message, parse_mode="Markdown")
        except Exception as e:
            logger.error(f"Admin mesaj hatasi: {e}")


# ============================================================
# BUTONLAR
# ============================================================

def get_main_keyboard():
    keyboard = [
        [InlineKeyboardButton("Iletisim", callback_data="btn_iletisim"), InlineKeyboardButton("Urunler", callback_data="btn_urunler")],
        [InlineKeyboardButton("Siparis Ver", callback_data="btn_siparis"), InlineKeyboardButton("Siparis Takip", callback_data="btn_siparistakip")],
        [InlineKeyboardButton("Kampanya", callback_data="btn_kampanya"), InlineKeyboardButton("Katalog", callback_data="btn_katalog")],
        [InlineKeyboardButton("Sikayet/Oneri", callback_data="btn_feedback")]
    ]
    return InlineKeyboardMarkup(keyboard)


def get_contact_keyboard():
    keyboard = [
        [InlineKeyboardButton("WhatsApp", url=BRAND["whatsapp"])],
        [InlineKeyboardButton("Instagram", url=BRAND["instagram"])],
        [InlineKeyboardButton("Telegram Grubu", url=BRAND["telegram_group"])],
        [InlineKeyboardButton("Telegram", url="https://t.me/Boomerbrandd")],
        [InlineKeyboardButton("Geri", callback_data="btn_geri")]
    ]
    return InlineKeyboardMarkup(keyboard)


def get_catalog_keyboard():
    products = get_all_products()
    keyboard = []
    for p in products[:6]:
        price = p['campaign_price'] if p.get('is_campaign') and p.get('campaign_price') else p['price']
        keyboard.append(InlineKeyboardButton(f"{p['model']} - {price}TL", callback_data=f"urun_{p['id']}"))
    keyboard.append([InlineKeyboardButton("Geri", callback_data="btn_geri")])
    return InlineKeyboardMarkup(keyboard)


def get_feedback_keyboard():
    keyboard = [
        [InlineKeyboardButton("Sikayet", callback_data="feedback_sikayet")],
        [InlineKeyboardButton("Oneri", callback_data="feedback_oneri")],
        [InlineKeyboardButton("Geri", callback_data="btn_geri")]
    ]
    return InlineKeyboardMarkup(keyboard)


def get_order_keyboard(order_id):
    keyboard = [
        [InlineKeyboardButton("Odeme Yap", callback_data=f"odeme_{order_id}")],
        [InlineKeyboardButton("Siparis Takip", callback_data=f"takip_{order_id}")],
        [InlineKeyboardButton("Geri", callback_data="btn_geri")]
    ]
    return InlineKeyboardMarkup(keyboard)


# ============================================================
# FORMAT FONKSİYONLARI
# ============================================================

def format_product_list(products, title="URUNLERIMIZ"):
    text = f"*{title}*\n\n"
    for p in products:
        price = p['campaign_price'] if p.get('is_campaign') and p.get('campaign_price') else p['price']
        price_text = f"~~{p['price']}TL~~ {price}TL" if p.get('is_campaign') else f"{price}TL"
        text += f"ID: `{p['id']}` | {p['model']}\n"
        if p.get('color'): text += f"Renk: {p['color']} | "
        if p.get('sizes'): text += f"Beden: {p['sizes']}\n"
        text += f"Fiyat: {price_text}\n\n"
    return text


def format_order_list(orders):
    if not orders: return "Henuz siparisiniz bulunmuyor."
    text = "*SIPARISLERINIZ*\n\n"
    for o in orders:
        status_map = {"pending_payment": "Bekliyor", "paid": "Odendi", "shipped": "Kargoda", "delivered": "Teslim", "payment_rejected": "Reddedildi"}
        price = o.get('campaign_price') or o.get('price', 0)
        text += f"#{o['order_id']} | {o['model']}\n"
        text += f"Beden: {o['size']} | Renk: {o.get('color', '-')} | {price}TL\n"
        text += f"Durum: {status_map.get(o['status'], o['status'])}\n"
        if o.get('tracking_code'): text += f"Kargo: {o['tracking_code']}\n"
        text += "\n"
    return text


# ============================================================
# KULLANICI KOMUTLARI
# ============================================================

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    add_user(user.id, username=user.username, first_name=user.first_name, last_name=user.last_name)
    add_stat("start", str(user.id))
    await update.message.reply_text("Hos geldiniz!\n\nBoomer Brand musterI temsilcisiyim.\n\nNasil yardimci olabilirim?", reply_markup=get_main_keyboard())


async def katalog_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    products = get_all_products()
    if not products:
        await update.message.reply_text("Henuz urun bulunmuyor.", reply_markup=get_main_keyboard())
        return
    await update.message.reply_text(format_product_list(products), reply_markup=get_catalog_keyboard())


async def kampanya_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    products = get_campaign_products()
    if not products:
        await update.message.reply_text("Aktif kampanya bulunmuyor.", reply_markup=get_main_keyboard())
        return
    await update.message.reply_text(format_product_list(products, title="KAMPANYALAR"), reply_markup=get_main_keyboard())


async def siparis_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("*SIPARIS VERMEK*\n\nID BEDEN RENK seklinde yazin.\nOrnek: `1 M Mavi`\n\nKatalog icin /katalog yazin.", reply_markup=get_main_keyboard(), parse_mode="Markdown")


async def siparistakip_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    orders = get_user_orders(update.effective_user.id)
    await update.message.reply_text(format_order_list(orders), reply_markup=get_main_keyboard())


async def kargotakip_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    orders = get_user_orders(update.effective_user.id)
    shipped = [o for o in orders if o.get('tracking_code')]
    if not shipped:
        await update.message.reply_text("Kargolanmis siparis yok.", reply_markup=get_main_keyboard())
        return
    text = "*KARGOLANMIS SIPARISLER*\n\n"
    for o in shipped:
        text += f"#{o['order_id']} - {o['model']}\nTakip: `{o['tracking_code']}`\n\n"
    await update.message.reply_text(text, reply_markup=get_main_keyboard(), parse_mode="Markdown")


async def iletisim_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"*ILETISIM*\n\nWhatsApp: {BRAND['whatsapp']}\nInstagram: {BRAND['instagram']}\nTelegram: {BRAND['telegram']}\nGrup: {BRAND['telegram_group']}", reply_markup=get_contact_keyboard(), parse_mode="Markdown")


# ============================================================
# YÖNETİCİ KOMUTLARI
# ============================================================

async def stats_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update.effective_user.id, update.effective_user.username): return
    stats = get_stats()
    text = f"*ISTATISTIKLER*\n\nToplam Kullanici: {stats['total_users']}\nToplam Siparis: {stats['total_orders']}\nBekleyen Odeme: {stats['pending_orders']}\nOdenmis: {stats['paid_orders']}\nKargolanmis: {stats['shipped_orders']}\nYeni Geri Bildirim: {stats['new_feedback']}"
    await update.message.reply_text(text, parse_mode="Markdown")


async def kargo_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update.effective_user.id, update.effective_user.username): return
    await update.message.reply_text("Kullanim: `/kargo SIPARIS_KODU TAKIP_KODU`")


# ============================================================
# MESAJ HANDLER
# ============================================================

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    message = update.message.text
    
    add_user(user.id, username=user.username, first_name=user.first_name, last_name=user.last_name)
    
    # Yönetici kontrolü
    user_is_admin = is_admin(user.id, user.username)
    
    # === YÖNETİCİ İŞLEMLERİ ===
    if user_is_admin:
        if message.startswith("/kargo "):
            parts = message.split()
            if len(parts) >= 3:
                order_id, tracking = parts[1], parts[2]
                set_tracking_code(order_id, tracking)
                order = get_order(order_id)
                if order:
                    try:
                        await context.bot.send_message(order['user_id'], f"Siparisiniz #{order_id} kargoya verildi!\nTakip: `{tracking}`", parse_mode="Markdown")
                    except Exception:
                        pass
                await update.message.reply_text(f"✅ {order_id} kargoya verildi")
            return
        
        if message.startswith("/urun "):
            parts = message[6:].split(maxsplit=4)
            if len(parts) >= 2:
                pid = add_product(parts[0], float(parts[1]), parts[2] if len(parts)>2 else None, parts[3] if len(parts)>3 else None, parts[4] if len(parts)>4 else None)
                await update.message.reply_text(f"Urun eklendi: ID {pid}")
            return
        
        if message.startswith("/onay "):
            order_id = message.split()[1] if len(message.split()) > 1 else None
            if order_id:
                confirm_payment(order_id, "Onaylandi")
                order = get_order(order_id)
                if order:
                    try:
    await context.bot.send_message(order['user_id'], f"Siparisiniz #{order_id} onaylandi!")
except:
    pass
                await update.message.reply_text(f"Siparis {order_id} onaylandi")
            return
        
        if message.startswith("/red "):
            parts = message.split(maxsplit=2)
            if len(parts) >= 2:
                reject_payment(parts[1], parts[2] if len(parts)>2 else "Reddedildi")
                order = get_order(parts[1])
                if order:
                    try: await context.bot.send_message(order['user_id'], f"Siparisiniz #{parts[1]} reddedildi.") except Exception:
    pass
                await update.message.reply_text(f"Siparis {parts[1]} reddedildi")
            return
        
        if message == "/sikayetler":
            feedbacks = get_new_feedback()
            if not feedbacks:
                await update.message.reply_text("Yeni sikayet/oner yok.")
            else:
                for f in feedbacks:
                    text = f"⚠️ *{'SIKAYET' if f['type']=='sikayet' else 'ONERI'}*\n\nKullanici: @{f.get('username', f['user_id'])}\nMesaj: {f['message']}"
                    await update.message.reply_text(text, parse_mode="Markdown")
                    mark_feedback_read(f['id'])
            return
    
    # === ŞİKAYET/ÖNERİ MODU ===
    if hasattr(context, 'feedback_mode') and context.feedback_mode:
        feedback_type = context.feedback_mode
        add_feedback(user.id, feedback_type, message)
        add_stat("feedback", feedback_type)
        
        # Yöneticiye DM
        admin_msg = f"{'🚨 SIKAYET' if feedback_type=='sikayet' else '💡 ONERI'}\n\nKullanici: @{user.username or 'Bilinmiyor'}\nID: `{user.id}`\n\nMesaj: {message}"
        await send_to_admin(context, admin_msg)
        
        context.feedback_mode = None
        await update.message.reply_text("Mesajiniz yoneticimize iletildi. Tesekkur ederiz.", reply_markup=get_main_keyboard())
        return
    
    # === SİPARİŞ ===
    parts = message.split()
    if len(parts) >= 3:
        try:
            product_id = int(parts[0])
            size = parts[1].upper()
            color = parts[2]
            product = get_product(product_id)
            if product:
                order_id = generate_order_id()
                price = product.get('campaign_price') or product.get('price', 0)
                create_order(order_id, user.id, product_id, size, color)
                add_stat("order", order_id)
                
                text = f"*SIPARIS ALINDI*\n\nNo: `{order_id}`\nUrun: {product['model']}\nBeden: {size} | Renk: {color}\nTutar: {price}TL\n\n{PAYMENT_INFO}"
                await update.message.reply_text(text, reply_markup=get_order_keyboard(order_id), parse_mode="Markdown")
                return
        except Exception:
    pass
    
    # === AI YANIT ===
    from llm.inference import generate
    response = generate(message)
    await update.message.reply_text(response, reply_markup=get_main_keyboard())


# ============================================================
# CALLBACK HANDLER
# ============================================================

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data
    
    if data == "btn_geri":
        await query.edit_message_text("Nasil yardimci olabilirim?", reply_markup=get_main_keyboard())
        return
    
    if data == "btn_iletisim":
        await query.edit_message_text(f"*ILETISIM*\n\nWhatsApp: {BRAND['whatsapp']}\nInstagram: {BRAND['instagram']}\nTelegram: {BRAND['telegram']}", reply_markup=get_contact_keyboard(), parse_mode="Markdown")
    
    elif data == "btn_urunler":
        products = get_all_products()
        await query.edit_message_text(format_product_list(products), reply_markup=get_catalog_keyboard())
    
    elif data == "btn_kampanya":
        products = get_campaign_products()
        if not products: await query.edit_message_text("Kampanya yok.", reply_markup=get_main_keyboard())
        else: await query.edit_message_text(format_product_list(products, title="KAMPANYALAR"), reply_markup=get_main_keyboard())
    
    elif data == "btn_katalog":
        products = get_all_products()
        await query.edit_message_text(format_product_list(products), reply_markup=get_catalog_keyboard())
    
    elif data == "btn_siparis":
        await query.edit_message_text("Siparis vermek icin /siparis yazin.", reply_markup=get_main_keyboard())
    
    elif data == "btn_siparistakip":
        orders = get_user_orders(query.from_user.id)
        await query.edit_message_text(format_order_list(orders), reply_markup=get_main_keyboard())
    
    elif data == "btn_feedback":
        await query.edit_message_text("*GERI BILDIRIM*\n\nBir sey soylemek ister misiniz?", reply_markup=get_feedback_keyboard())
    
    elif data == "feedback_sikayet":
        context.feedback_mode = "sikayet"
        await query.edit_message_text("SIKAYETINIZI yazin:\nEn kisa surede cozum sunacagiz.")
    
    elif data == "feedback_oneri":
        context.feedback_mode = "oneri"
        await query.edit_message_text("ONERINIZI yazin:\nDegerlendirelim.")
    
    elif data.startswith("odeme_"):
        order_id = data.replace("odeme_", "")
        await query.edit_message_text(f"*ODEME*\n\nSiparis: `{order_id}`\n\n{PAYMENT_INFO}", reply_markup=get_main_keyboard(), parse_mode="Markdown")


# ============================================================
# MAIN
# ============================================================

def main():
    print("Bot calisiyor...")
    
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    
    # Kullanıcı komutları
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("katalog", katalog_command))
    app.add_handler(CommandHandler("kampanya", kampanya_command))
    app.add_handler(CommandHandler("siparis", siparis_command))
    app.add_handler(CommandHandler("siparistakip", siparistakip_command))
    app.add_handler(CommandHandler("kargotakip", kargotakip_command))
    app.add_handler(CommandHandler("iletisim", iletisim_command))
    
    # Yönetici komutları
    app.add_handler(CommandHandler("stats", stats_command))
    app.add_handler(CommandHandler("kargo", kargo_command))
    
    # Callback
    app.add_handler(CallbackQueryHandler(button_callback))
    
    # Mesajlar
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    app.run_polling(poll_interval=1)


if __name__ == "__main__":
    main()