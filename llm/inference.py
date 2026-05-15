"""
BOOMER BRAND YAPAY ZEKA ASISTANI - V4
====================================
En iyi müşteri temsilcisi deneyimi

Ozellikler:
- Akıllı intent esleme
- Kisa ve net yanıtlar
- Soru sorma
- Dogal Turkce
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# ============================================================
# MARKA BİLGİLERİ
# ============================================================

BRAND = {
    "name": "Boomer Brand",
    "founder": "Şuayip Solmaz",
    "location": "İstanbul Merter",
    "whatsapp": "https://wa.me/boomermerter",
    "instagram": "https://www.instagram.com/boomermerter/",
    "telegram": "@Boomerbrandd"
}

# ============================================================
# INTENT MAP
# ============================================================

INTENTS = {
    "greeting": ["merhaba", "selam", "hi", "hey", "slm", "sg", "naber", "nasilsin", "gunaydin", "hos geldin", "merhabalar"],
    "thanks": ["tesekkur", "tesekkurler", "ty", "tsk", "sagol", "sagolun", "eyvallah", "rica", "cok tesekkurler"],
    "founder": ["kimin", "sahibi", "patron", "boss", "kim kurdu", "kurucu", "kurucusu", "yetkili", "sorumlu", "yonetici", "siz kimsiniz", "kimsiniz", "mudur", "patronunuz", "yonetici kim", "lider"],
    "location": ["nerede", "adres", "konum", "yer", "magaza", "dukkan", "neredesiniz", "adresiniz", "gelmek", "ziyaret", "nerden", "nasil gelinir", "yol tarifi", "merter", "istanbul", "nereli", "adres"],
    "brand": ["marka", "brand", "boomer brand", "hakkinda", "nedir", "neyin", "neyi", "firma", "sirket", "kurulus", "tarihce", "vizyon", "misyon", "ne is yapiyorsunuz", "neyi satiyorsunuz"],
    "quality": ["kalite", "kaliteli", "malzeme", "kumas", "guvenilir", "nasil", "iyi mi", "dayanikli", "kalitelimi"],
    "price": ["fiyat", "fiyati", "fiyatlar", "kac", "ucret", "para", "tl", "lira", "ne kadar", "ucuz mu", "pahali mi", "indirim", "iskonto", "fiyat ne", "kac para", "fiyati ne", "ucreti ne"],
    "product": ["urun", "urunler", "ne var", "neler var", "pantolon", "tishort", "gomlek", "ceket", "mont", "sweatshirt", "sort", "katalog", "giyim", "kiyafet", "moda", "store", "shop", "stok", "satiyorsunuz", "gormek", "bakmak", "incelemek", "hangi urun", "ne satiyorsunuz", "modeller", "urunleriniz", "koleksiyon", "neler satiyorsunuz"],
    "order": ["siparis", "siparis vermek", "order", "almak", "satın almak", "alacagim", "istiyorum", "almak istiyorum", "nasil alirim", "alisveris", "vermek istiyorum", "urun almak", "bir sey almak"],
    "complaint": ["sikayet", "sikayetim", "iade", "sorun", "problem", "bozuk", "kotu", "ayipli", "begenedim", "pazardim", "degistirme", "iade etmek", "bozdu", "calismadi", "uzgunum", "hayal kirikligi"],
    "contact": ["iletisim", "contact", "whatsapp", "telefon", "ulasmak", "numara", "mail", "eposta", "ulas", "baglanmak", "telefon numaraniz", "numaraniz", "irttibat", "irtibat", "bilgi"],
    "social": ["instagram", "insta", "ig", "telegram", "facebook", "sosyal", "sayfa", "kanal", "profil", "reels", "video", "story", "insta hesabiniz", "insta adresiniz"],
    "help": ["yardim", "yardim", "help", "yardimci", "komut", "komutlar", "ne yaparsin", "neler yaparsin", "ne yapabilirsin", "nelerin var", "ne var", "ne yapalim", "neleriniz var", "bana yardim"],
    "tracking": ["kargo", "kargom", "kargo takip", "kargo takibi", "kargom nerede", "kargom ne zaman", "kargo durumu", "kargoya verdiniz mi", "siparisim nerede", "teslimat", "kargo numarasi"],
    "order_tracking": ["siparis takip", "siparis durumu", "siparisim", "siparislerim", "gecmis siparisler", "siparis durum", "siparisi kontrol", "siparislerim nerede"],
}

# ============================================================
# YANITLAR
# ============================================================

RESPONSES = {
    "greeting": "Merhaba! Size nasil yardimci olabilirim?",
    "thanks": "Rica ederim. Baska bir konuda yardimci olabilir miyim?",
    "founder": "Kurucusu Şuayip Solmaz'dir.",
    "location": "Merter'deyiz. Istanbul'un onemli tekstil carsilarindan birinin merkezindeyiz.",
    "brand": "Boomer Brand, Istanbul Merter'de tekstil sektorunde faaliyet gosteren bir markadir.",
    "quality": "Kalite standartlarimiz yuksektir.",
    "price": "Fiyat bilgisi icin WhatsApp'tan yazabilirsiniz:\nhttps://wa.me/boomermerter",
    "product": "Urunlerimizi Instagram'dan inceleyebilirsiniz:\nhttps://www.instagram.com/boomermerter/",
    "order": "Siparis vermek icin WhatsApp'tan yazabilirsiniz:\nhttps://wa.me/boomermerter",
    "complaint": "Yasadiginiz sorun icin uzgunum. Cozmak icin WhatsApp'tan ulasabilirsiniz:\nhttps://wa.me/boomermerter",
    "contact": "Iletisim:\nWhatsApp: https://wa.me/boomermerter\nInstagram: https://www.instagram.com/boomermerter/\nTelegram: @Boomerbrandd",
    "social": "Instagram: https://www.instagram.com/boomermerter/\nTelegram: @Boomerbrandd",
    "help": "Komutlar:\n/katalog - Urunler\n/kampanya - Kampanyalar\n/siparis - Siparis\n/siparistakip - Siparis takip\n/kargotakip - Kargo takip\n/iletisim - Iletisim",
    "tracking": "Kargo takip icin /kargotakip yazabilirsiniz.",
    "order_tracking": "Siparis takip icin /siparistakip yazabilirsiniz.",
    "fallback": "Size yardimci olabilecegim konular: urunler, fiyat, siparis, sikayet, iletisim. Hangisini tercih edersiniz?"
}

# ============================================================
# ENGINE
# ============================================================

def find_best_intent(text: str) -> str:
    if not text or not text.strip():
        return "fallback"
    
    text = text.strip().lower()
    
    if len(text) <= 2:
        return "greeting"
    
    best_intent = None
    best_match_len = 0
    
    for intent_name, keywords in INTENTS.items():
        for keyword in keywords:
            if text == keyword or f" {keyword} " in f" {text} ":
                if len(keyword) > best_match_len:
                    best_intent = intent_name
                    best_match_len = len(keyword)
            elif keyword in text and len(keyword) >= 3:
                if len(keyword) > best_match_len:
                    best_intent = intent_name
                    best_match_len = len(keyword)
    
    return best_intent if best_intent else "fallback"


def generate(prompt: str, user_id: str = None) -> str:
    if not prompt or not prompt.strip():
        return "Size nasil yardimci olabilirim?"
    
    prompt = prompt.strip()
    
    if prompt.startswith("/"):
        return RESPONSES["fallback"]
    
    intent = find_best_intent(prompt)
    return RESPONSES.get(intent, RESPONSES["fallback"])


if __name__ == "__main__":
    tests = [
        ("merhaba", "greeting"),
        ("kimin", "founder"),
        ("nerede", "location"),
        ("fiyat", "price"),
        ("urun", "product"),
        ("siparis", "order"),
        ("sikayet", "complaint"),
        ("iletisim", "contact"),
        ("instagram", "social"),
        ("yardim", "help"),
        ("kargo takip", "tracking"),
        ("siparis takip", "order_tracking"),
    ]
    print("TEST:")
    for t, expected in tests:
        result = find_best_intent(t)
        status = "OK" if result == expected else "HATA"
        print(f"{status}: {t} -> {result}")