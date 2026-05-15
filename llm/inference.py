import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import requests
import time
from config import HF_API_KEY, WHATSAPP_LINK, INSTAGRAM_LINK, TELEGRAM_GROUP_ID

# ============================================
# BOOMER BRAND AI SISTEMI - TAM TURKCE
# ============================================

BOOMER_PERSONA = """Sen "Boomer Brand" markasının resmi yapay zeka müşteri temsilcisisin.

KİMLİĞİN (ÇOK ÖNEMLİ):
- Adın "Boomer" ve marka temsilcisisin
- Her yanıtta kendini tanıt: "Boomer Brand müşteri temsilcisiyim" veya "Boomer olarak yardımcı oluyorum"
- Müşteri temsilcisi, satış ve pazarlama uzmanısın
- Profesyonel, sıcak, güven verici ve yardımsever birisin
- Markayı en iyi şekilde temsil edersin

DAVRANIŞ KURALLARI:
- Kısa, net ve Türkçe yanıtlar ver
- Sorunları çözmek için elinden geleni yap
- Müşteriyi yönlendirirken nazik ol
- Olumlu ve iyimmer bir dil kullan

YÖNLENDİRME KURALLARI (MUTLAK):
- Fiyat, fiyatliste, kaç para, ne kadar, para soruları → "Size en güncel fiyatları sunabilmem için WhatsApp hattımı ziyaret edebilirsiniz: https://wa.me/boomermerter"
- Kampanya, indirim, yüzde, promo soruları → "Aktif kampanyalarımız ve özel indirimlerimiz için WhatsApp hattımızda size özel tekliflerimiz var: https://wa.me/boomermerter"
- Sipariş vermek isteyen → "Siparişinizi hemen almak için WhatsApp üzerinden size yardımcı olabilirim: https://wa.me/boomermerter"
- Stok durumu soruları → "Stok durumunu öğrenmek için WhatsApp hattımızdan bilgi alabilirsiniz: https://wa.me/boomermerter"
- İade/şikayet → "Yaşadığınız sorunu çözmek için buradayım. Detayları WhatsApp'tan alabiliriz: https://wa.me/boomermerter"

İLETİŞİM BİLGİLERİ:
- WhatsApp: https://wa.me/boomermerter
- Instagram: https://www.instagram.com/boomermerter/
- Telegram: @Boomerbrandd

Şimdi kullanıcının sorusuna yanıt ver:"""

def call_huggingface(prompt, model="mistralai/Mistral-7B-Instruct-v0.2"):
    """HuggingFace API çağrısı"""
    if not HF_API_KEY or HF_API_KEY in ["", "YOUR_HUGGINGFACE_API_KEY_HERE", "hf_your_huggingface_token_here"]:
        return None
    
    try:
        API_URL = f"https://api-inference.huggingface.co/models/{model}"
        headers = {"Authorization": f"Bearer {HF_API_KEY}"}
        
        payload = {
            "inputs": prompt,
            "parameters": {
                "max_new_tokens": 256,
                "temperature": 0.7,
                "top_p": 0.95,
                "do_sample": True,
                "return_full_text": False
            }
        }
        
        response = requests.post(API_URL, headers=headers, json=payload, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            if isinstance(result, list) and len(result) > 0:
                return result[0].get("generated_text", "").strip()
        elif response.status_code == 503:
            print(f"Model busy, trying alternate...")
        else:
            print(f"HF Error: {response.status_code}")
            
    except Exception as e:
        print(f"HF Exception: {e}")
    
    return None

def generate(prompt, user_id=None):
    """Ana generate fonksiyonu"""
    print(f"[AI] Processing: {prompt[:50]}...")
    
    # Kullanıcı bağlamını al
    user_context = ""
    if user_id:
        try:
            from db.repo import get_user_context
            user_context = get_user_context(user_id)
        except:
            pass
    
    # Full prompt oluştur
    full_prompt = BOOMER_PERSONA
    if user_context:
        full_prompt += f"\n\nKullanıcının önceki mesajları: {user_context}"
    full_prompt += f"\n\nKullanıcı: {prompt}\n\nBoomer:"
    
    # Model 1: Mistral
    result = call_huggingface(full_prompt, "mistralai/Mistral-7B-Instruct-v0.2")
    if result:
        return clean_ai_response(result)
    
    # Model 2: Llama (alternatif)
    result = call_huggingface(full_prompt, "meta-llama/Llama-3-8b-instruct")
    if result:
        return clean_ai_response(result)
    
    # Yedek yanıtlar (fallback)
    print("[AI] Using fallback responses")
    return get_fallback_response(prompt)

def clean_ai_response(text):
    """AI yanıtını temizle"""
    if not text:
        return None
    
    # "Boomer:" veya "Asistan:" sonrasını al
    if "Boomer:" in text:
        text = text.split("Boomer:")[-1].strip()
    elif "Asistan:" in text:
        text = text.split("Asistan:")[-1].strip()
    elif "Assistant:" in text:
        text = text.split("Assistant:")[-1].strip()
    
    # Temizle
    text = text.strip()
    if len(text) > 600:
        text = text[:597] + "..."
    
    return text if text else None

def get_fallback_response(prompt):
    """Yedek yanıtlar - AI çalışmazsa"""
    p = prompt.lower()
    
    # Selamlama
    if any(w in p for w in ["merhaba", "selam", "hi", "hello", "hey", "naber", "nasılsın"]):
        return """👋 Merhaba! 😊

Boomer Brand müşteri temsilcisiyim!

Size nasıl yardımcı olabilirim?

🛍️ Ürünlerimizi görmek için /katalog
🛒 Sipariş vermek için WhatsApp: https://wa.me/boomermerter
📝 Şikayetinizi bildirmek için /sikayet

Her türlü sorunuz için buradayım!"""

    # Fiyat sorusu
    if any(w in p for w in ["fiyat", "kaç", "ücret", "ne kadar", "lira", "tl", "para", "price"]):
        return """💰 Merhaba!

Güncel fiyatlarımız ve özel tekliflerimiz için WhatsApp hattımızı ziyaret edebilirsiniz:

📱 https://wa.me/boomermerter

Size özel indirimler ve kampanyalarımız var!"""

    # Kampanya/indirim
    if any(w in p for w in ["kampanya", "indirim", "yüzde", "promo", "discount", "offer"]):
        return """🎉 Merhaba!

Aktif kampanyalarımız ve özel indirimlerimiz için WhatsApp hattımızı ziyaret edin:

📱 https://wa.me/boomermerter

Instagram ve Telegram hesaplarımızı da takip etmeyi unutmayın!"""

    # Sipariş
    if any(w in p for w in ["sipariş", "satın", "almak", "order", "vermek", "alacağım"]):
        return """🛒 Merhaba!

Siparişinizi hemen almak için WhatsApp hattımızdan size yardımcı olabiliriz:

📱 https://wa.me/boomermerter

Ürünlerimizi incelemek için /katalog komutunu da kullanabilirsiniz!"""

    # Şikayet/iade
    if any(w in p for w in ["şikayet", "iade", "sorun", "problem", "şikayetim", "kötü"]):
        return """📝 Merhaba!

Yaşadığınız sorunu duyduğuma üzgünüm. Size yardımcı olmak için buradayım!

Şikayetinizi /sikayet komutuyla bildirebilir veya direkt WhatsApp üzerinden destek ekibimizle iletişime geçebilirsiniz:

📱 https://wa.me/boomermerter"""

    # Ürün sorusu
    if any(w in p for w in ["ürün", "ürünler", "katalog", "ne var", "neler var", "giyim", "elbise", "pantolon", "tişört"]):
        return """🛍️ Merhaba!

Ürün kataloğumuzu görmek için /katalog komutunu kullanabilirsiniz!

Detaylı bilgi, fiyat ve stok durumu için WhatsApp hattımız:

📱 https://wa.me/boomermerter"""

    # Teşekkür
    if any(w in p for w in ["teşekkür", "tşk", "sağol", "teşekkürler", "thank"]):
        return """😊 Merhaba!

Rica ederim! Her zaman yardımcı olmaktan mutluluk duyarım!

Başka bir sorunuz olursa çekinmeyin!"""

    # Yardım
    if any(w in p for w in ["yardım", "help", "ne yapabilirsin", "neler yaparsın"]):
        return """🤖 Merhaba! Boomer olarak size şu konularda yardımcı olabilirim:

🛍️ Ürün ve fiyat bilgisi
🛒 Sipariş vermek
📝 Şikayet ve iade işlemleri
🎁 Kampanya ve indirimler
❓ Genel sorular

Nasıl yardımcı olabilirim?"""

    # Varsayılan
    return """🤖 Merhaba! Boomer Brand müşteri temsilcisiyim!

Size yardımcı olmak için buradayım:

🛍️ /katalog - Ürünlerimizi görüntüle
🛒 /siparis - Sipariş ver
📝 /sikayet - Şikayet bildir
📊 /stats - İstatistikleri görüntüle

Ya da direkt sorunuzu yazın, yanıtlayacağım! 😊"""