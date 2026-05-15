import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# ============================================================================
# BOOMER BRAND YAPAY ZEKA - TAM EĞİTİM (EMOJI YOK)
# ============================================================================

WHATSAPP_LINK = "https://wa.me/boomermerter"
INSTAGRAM_LINK = "https://www.instagram.com/boomermerter/"
TELEGRAM_LINK = "@Boomerbrandd"
INSTAGRAM_KURUCU = "https://www.instagram.com/1suayipsolmaz"
KONUM = "Istanbul/Merter"

def generate(prompt, user_id=None):
    """Ana generate fonksiyonu - Marka bilinciyle"""
    print(f"[AI] Processing: {prompt}")
    return generate_brand_response(prompt)

def generate_brand_response(prompt):
    """Marka bilinçli yanıt üretici"""
    
    p = prompt.lower()
    
    # KURUCU/SORGU/CİDDİYET SORULARI
    if any(w in p for w in ["kimin", "sahibi", "patron", "yetkili", "kim kurdu", "kim yonetiyor", "boss", "owner", "yönetmen"]):
        return f"""Boomer Brand'in kurucusu ve sahibi *Suayip Solmaz* Bey'dir.

Suayip Solmaz, Merter giyim piyasasinda cekirdekten yetismis, Turkiye genelinde yuzlerce esnaf, marka ve sirketle baglantilar kurmus basarili bir girisimci, esnaf ve is adamidir.

Daima guvenilir ticaretler ile adini sektorde altin harflerle yazdirmistir.

Instagram: {INSTAGRAM_KURUCU}

Size nasil yardimci olabilirim?"""
    
    # KONUM/ADRES
    if any(w in p for w in ["yeriniz", "magaza", "adres", "nerede", "konum", "location", "shop", "magaza nerede", "nereden alabilirim"]):
        return f"""Magazamiz *Istanbul/Merter*'dedir!

Merter, Istanbul'un en onemli giyim merkezlerinden biridir. 

Urunlerimizi gormek icin: /katalog

Detayli adres ve yol tarifi icin WhatsApp uzerinden iletisime gecabilirsiniz:
{WHATSAPP_LINK}

Sizleri magazamizda misafir etmekten mutluluk duyariz!"""
    
    # KALİTE
    if any(w in p for w in ["kalite", "kaliteli mi", "guvenilir", "nasil", "eger", "kalitelimi", "malzeme", "urun kalitesi", "dayanikli mi"]):
        return f"""Hic supheeniz olmasin!

Boomer Brand olarak sizlere daima en kaliteli urunleri, en ideal fiyata sunmak icin tum emegimizi sarf ediyoruz.

Urunlerimizi Telegram grubumuzdan veya magazamizda inceleyebilirsiniz. 
Telegram: {TELEGRAM_LINK}

Bize WhatsApp uzerinden 7/24 ulasabilirsiniz:
{WHATSAPP_LINK}

Memnuniyetiniz bizim icin en onemli onceliktir!"""
    
    # SELAMLAMA
    if any(w in p for w in ["merhaba", "selam", "hi", "naber", "nasilsin", "hello", "hey"]):
        return f"""Merhaba! Boomer Brand musteri temsilcisiyim!

Size nasil yardimci olabilirim?

- Urunlerimizi gormek icin: /katalog
- Siparis vermek icin: WhatsApp uzerinden
- Sikayetinizi bildirmek icin: /sikayet

Bize ulasmak icin: {WHATSAPP_LINK}

Hos geldiniz!"""
    
    # FİYAT
    if any(w in p for w in ["fiyat", "kac", "ucret", "ne kadar", "para", "tl", "lira", "fiyati", "fiyatlar", "ne var", "kac lira"]):
        return f"""Merhaba!

Guncel fiyatlarimiz ve ozel tekliflerimiz icin WhatsApp hatimizi ziyaret edebilirsiniz:

{WHATSAPP_LINK}

Size ozel indirimler ve kampanyalarimiz olabilir!

Ayrıca urunlerimizi Telegram grubumuzda da inceleyebilirsiniz:
{TELEGRAM_LINK}

Saygilarmyla."""
    
    # KAMPANYA
    if any(w in p for w in ["kampanya", "indirim", "yuzde", "promo", "offer", "discount", "ozel", "firsat"]):
        return f"""Merhaba!

Aktif kampanyalarimiz ve ozel indirimlerimiz icin WhatsApp hatimizi ziyaret edin:

{WHATSAPP_LINK}

Instagram ve Telegram hesaplarimizi da takip etmeyi unutmayin:
- Instagram: {INSTAGRAM_LINK}
- Telegram: {TELEGRAM_LINK}

Sizlere ozel fırsatlar kacirmayin!"""
    
    # SİPARİŞ
    if any(w in p for w in ["siparis", "satin", "almak", "vermek", "order", "alacagim", "istiyorum", "nasil alirim"]):
        return f"""Merhaba!

Siparisinizi hemen almak icin WhatsApp hatimiz uzerinden size yardimci olabiliriz:

{WHATSAPP_LINK}

Urunlerimizi incelemek icin /katalog komutunu kullanabilirsiniz.

Telegram grubumuzda da urunleri gorebilirsiniz:
{TELEGRAM_LINK}

Saygilarmyla."""
    
    # ŞİKAYET
    if any(w in p for w in ["sikayet", "iade", "sorun", "problem", "sikayetim", "bozuk", "kotu", "ayipli"]):
        return f"""Merhaba!

Yasadiginiz sorunu duyduguma uzgunum. Size yardimci olmak icin buradayim!

Sikayetinizi /sikayet komutuyla bildirebilir veya direkt WhatsApp uzerinden destek ekibimizle iletisime gecabilirsiniz:

{WHATSAPP_LINK}

En kisa surede cozum saglayacagiz. Musteri memnuniyeti bizim icin cok onemli!

Saygilarmyla."""
    
    # ÜRÜN
    if any(w in p for w in ["urun", "urunler", "katalog", "ne var", "neler var", "giyim", "elbise", "pantolon", "tisort", "ceket", "mont"]):
        return f"""Merhaba!

Urun katalogumuzu gormek icin /katalog komutunu kullanabilirsiniz!

Urunlerimiz Telegram grubumuzda da duzenli olarak paylasilmaktadir:
{TELEGRAM_LINK}

Detayli bilgi, fiyat ve stok durumu icin WhatsApp hatimiz:
{WHATSAPP_LINK}

Merter'in en kaliteli urunleri sizleri bekliyor!

Saygilarmyla."""
    
    # İLETİŞİM
    if any(w in p for w in ["iletisim", "contact", "ulas", "whatsapp", "telefon", "adres", "mail", "eposta"]):
        return f"""Boomer Brand Iletisim Bilgileri:

WhatsApp: {WHATSAPP_LINK}
Instagram: {INSTAGRAM_LINK}
Telegram: {TELEGRAM_LINK}
Magaza: Istanbul/Merter

7/24 size yardimci olmaya haziriz!

Saygilarmyla."""
    
    # TEŞEKKÜR
    if any(w in p for w in ["tesekkur", "tesekkurler", "tsk", "tsk", "sagol", "sagol", "thank"]):
        return """Merhaba!

Rica ederim! Yardimci olmaktan cok mutluluk duyarim.

Herhangi bir sorunuz olursa cekinmeden sorun!

Saygilarmyla,
Boomer Brand"""
    
    # YARDIM
    if any(w in p for w in ["yardim", "help", "ne yaparsin", "neler yaparsin", "ne yapabilirsin", "neler var", "komutlar"]):
        return f"""Boomer Brand Asistani - Size yardimci olabilecekler:

/katalog - Urunlerimizi goruntule
/siparis <urun_id> - Siparis ver
/sikayet - Sikayet veya iade bildir
/stats - Istatistikleri goruntule
/kampanya - Kampanyalari goruntule (sadece yonetici)

Dilerseniz direkt sorunuzu yazin, yanitlayayim!

Iletisim: {WHATSAPP_LINK}

Saygilarmyla."""
    
    # HAKKINDA
    if any(w in p for w in ["hakkinda", "hakkinda", "nedir", "neyin", "ne marka", "ne marka", "brand", "kimsiniz", "neyi satiyorsunuz"]):
        return f"""Boomer Brand Hakkinda:

Boomer Brand, Istanbul/Merter'de faaliyet gosteren guvenilir bir giyim markasidir.

Kurucumuz *Suayip Solmaz* Bey, sektorde yillarin deneyimine sahip basarili bir is insanidir.

Politikamiz:
- En kaliteli urunler
- En ideal fiyatlar  
- Guvenilir ticaret
- Musteri memnuniyeti

Urunlerimiz: Pantolon, tisort, ceket, mont, gomlek ve daha fazlasi!

Bize ulasin:
{WHATSAPP_LINK}

Saygilarmyla."""
    
    # VARSayıLAN
    return f"""Merhaba! Boomer Brand musteri temsilcisiyim!

Size yardimci olmak icin buradayim:

/katalog - Urunlerimizi goruntule
/siparis - Siparis vermek icin WhatsApp
/sikayet - Sikayet veya iade bildir
/stats - Istatistikleri goruntule

Ya da direkt sorunuzu yazin, yanitlayayim!

Iletisim: {WHATSAPP_LINK}

Saygilarmyla."""