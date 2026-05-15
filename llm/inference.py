import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# ============================================================================
# BOOMER BRAND YAPAY ZEKA - TAM EĞİTİLMİŞ, SAMİMİ, PAZARLAMA UZMANI
# ============================================================================

WHATSAPP = "https://wa.me/boomermerter"
INSTAGRAM = "https://www.instagram.com/boomermerter/"
TELEGRAM = "@Boomerbrandd"
INSTAGRAM_KURUCU = "https://www.instagram.com/1suayipsolmaz"

def generate(prompt, user_id=None):
    return smart_response(prompt)

def smart_response(prompt):
    p = prompt.lower()
    
    # KURUCU
    if any(w in p for w in ["kimin", "sahibi", "patron", "yetkili", "kim kurdu", "boss", "owner", "yönetmen", "kimin", "kursahibi", "yöneticiniz", "sorumlu"]):
        return "Merhaba! \n\nBoomer Brand'in kurucusu ve sahibi **Suayip Solmaz** Bey'dir.\n\nKendisi yıllardır Merter'te tekstil sektöründe çalışan, sektörü çok iyi tanıyan, güvenilir ve başarılı bir iş insanıdır. Türkiye genelinde yüzlerce esnaf ve markayla iş bağlantıları kurmuş, adını sektörde duyurmuş bir girişimcidir.\n\nMisyonumuz: Musterilerimize en kaliteli urunleri en uygun fiyatla sunmek ve guvenilir hizmet vermektir.\n\nSize yardimci olmamı ister misiniz?"
    
    # KONUM
    if any(w in p for w in ["yeriniz", "mağaza", "adres", "nerede", "konum", "location", "shop", "neredesiniz", "adresiniz", "nerden", "gelmek", "ziyaret"]):
        return "Merhaba!\n\nMagazamiz Istanbul Merter'tedir. Merter, Istanbul'un en büyük tekstil ve giyim merkezlerinden biridir.\n\nMagazamiza gelip urunleri yakından inceleyebilir, deneyebilir ve begendiginiz urunleri aninda satin alabilirsiniz.\n\nYol tarifi veya magaza hakkinda detayli bilgi ister misiniz? WhatsApp uzerinden yardimci olabilirim: " + WHATSAPP + "\n\nGorüşmek uzere!"
    
    # KALİTE
    if any(w in p for w in ["kalite", "kaliteli mi", "güvenilir", "nasil", "kalitelimi", "malzeme", "dayanikli mi", "kaliteli", "kalite", "malzeme kalitesi", "kumas"]):
        return "Merak etmeyin, kalite konusunda sizi asla yaniltmayiz!\n\nBoomer Brand olarak:\n- En kaliteli kumaslari kullaniyoruz\n- Isçilik ve dikis kalitesine dikkat ediyoruz\n- Türkiye'nin en iyi ureticileriyle çalışıyoruz\n- Her urunu bizzat kontrol ediyoruz\n\nUrunlerimizi magazamizda veya Telegram grubumuzda gorebilirsiniz. " + TELEGRAM + "\n\nTatmin olmazsaniz kosulsuz iade garantisi sunuyoruz!\n\nYardimci olabilecek bir konu var mi?"
    
    # SELAMLAMA
    if any(w in p for w in ["merhaba", "selam", "hi", "naber", "nasilsin", "hello", "hey", "gunaydin", "iyi gunler", "slm", "sg"]):
        return "Merhaba!\n\nBoomer Brand'dan selamlar! \n\nBen size yardimci olmak için buradayim. Bugun ne ariyordunuz? Urunlerimiz mi, fiyatlar mi, yoksa baska bir konu mu?\n\nMerak etmeyin, soru sormaktan cekinmeyin - ne bilirsem hemen yardimci olurum!\n\nOrnek:\n- Hangi urunleri var?\n- Fiyatlar ne?\n- Nasil siparis verilir?\n\nNe isterseniz sorun, yanitlayayim!"
    
    # FİYAT
    if any(w in p for w in ["fiyat", "kac", "ücret", "ne kadar", "para", "tl", "lira", "fiyati", "fiyatlar", "ne var", "kac lira", "pazarlik", "indirim", "iskonto", "kampanya"]):
        return "Merhaba!\n\nFiyatlarimiz hakkinda detayli bilgi almak istemeniz çok normal. Sizlere en uygun fiyatlari sunmak istiyoruz!\n\nWhatsApp uzerinden bize ulasin, size ozel fiyat teklifi yapalim:\n" + WHATSAPP + "\n\nAyrica:\n- Dostlarinizi getirdiginizde ekstra indirim\n- Sezon sonu indirimleri\n- Toplu alimlarda ozel fiyatlar\n\nMesgul oldugunuz bir is mi var? Tamam, WhatsApp'tan yazin, hemen donelim!\n\nSaygilarmyla."
    
    # ÜRÜN
    if any(w in p for w in ["urun", "urunler", "katalog", "ne var", "neler var", "giyim", "elbise", "pantolon", "tisort", "ceket", "mont", "elbise", "ne satiyorsunuz"]):
        return "Merhaba!\n\nUrun yelpazemiz oldukça genis! Pantolon, tisort, gomlek, ceket, mont, sweatshirt ve daha fazlasi...\n\nHer mevsime uygun, hem gunluk hem sik tasarimlarimiz var.\n\nKatalog göruntulemek için /katalog yazabilirsiniz.\n\nYa da hangi tarz urun ariyorsunuz? Ornegin:\n- Spor giyim mi?\n- Office tarzi mi?\n- Gunluk kiyasif mi?\n\nSize ozel öneri yapabilirim!\n\nDetaylar icin WhatsApp: " + WHATSAPP
    
    # SİPARİŞ
    if any(w in p for w in ["siparis", "satin", "almak", "vermek", "order", "alacagim", "istiyorum", "nasil alirim", "siparis vermek", "nasil siparis"]):
        return "Merhaba!\n\nSiparis vermek çok kolay!\n\nWhatsApp uzerinden yazin, size siparis sürecini adim adim anlatayim:\n" + WHATSAPP + "\n\nSiparis sonrasi:\n- Kargo takibi yapilir\n- Olcu uyumsuzlugunda ucretsiz degisim\n- Memnuniyetsizlik durumunda iade\n\nYaninizdayim! Hangi urunu almak istediginizi soylerseniz hemen yardimci olayim!"
    
    # ŞİKAYET
    if any(w in p for w in ["sikayet", "iade", "sorun", "problem", "sikayetim", "bozuk", "kotu", "ayipli", "begmedim", "pazardim"]):
        return "Merhaba!\n\nYasadiginiz sorun hakkinda bilgi almam çok uzgun...\n\nHemen çözelim! Size ozel yardimci olmak istiyorum.\n\nSikayetinizi veya yasadiginiz problemi detayli yazin - en kisa surede çözelim!\n\nAyrica dilerseniz /sikayet komutuyla form doldurabilirsiniz.\n\nWhatsApp uzerinden de ulasabilirsiniz:\n" + WHATSAPP + "\n\nMusteri memnuniyeti bizim için en önemli konu!\n\nMerak etmeyin, çözüme kavusturacagiz!"
    
    # İLETİŞİM
    if any(w in p for w in ["iletisim", "contact", "ulas", "whatsapp", "telefon", "adres", "mail", "eposta", "nasil ulasirim", "numaraniz", "telefon"]):
        return "Merhaba!\n\nBize ulasmak çok kolay! Hangisini tercih edersiniz?\n\n- WhatsApp: " + WHATSAPP + "\n- Instagram: " + INSTAGRAM + "\n- Telegram: " + TELEGRAM + "\n- Magaza: Istanbul/Merter\n\nHangi konuda yardimci olmami isterseniz söyleyin!\n\n7/24 yaninizdayim!"
    
    # TEŞEKKÜR
    if any(w in p for w in ["tesekkur", "tesekkurler", "tsk", "sagol", "sagolun", "thank", "tesekkur ederim", "tesekkurler", "eywallah"]:
        return "Rica ederim!\n\nYardimci olabildiysem ne mutlu!\n\nBir baska konuda yardimci olmami ister misiniz?\n\nOrnegin:\n- Urunler hakkinda sorulariniz var mi?\n- Fiyat bilgisi ister misiniz?\n- Kampanyalardan haberdar olmak ister misiniz?\n\nBuradayim!"
    
    # YARDIM
    if any(w in p for w in ["yardim", "help", "ne yaparsin", "neler yaparsin", "ne yapabilirsin", "neler var", "komutlar", "neleri yapabilirsin", "neleri", "yapay zeka", "nasil çalişirsin", "ne yaparsin"]:
        return "Merhaba! Size yardimci olabilecek komutlar:\n\n- /katalog - Urunlerimizi görüntüle\n- /siparis - Siparis vermek için\n- /sikayet - Sikayet veya iade bildirmek için\n- /stats - Istatistikleri görmek için\n- /kampanya - Aktif kampanyalar için (sadece yönetici)\n\nAyrıca bana direkt yazabilirsiniz - ornegin:\n- Hangi tisortlariniz var?\n- Pantolon fiyatlari ne?\n- En yakin kampanya ne?\n\nHer soruniza yanit vereyim!\n\nWhatsApp: " + WHATSAPP + "\nInstagram: " + INSTAGRAM
    
    # HAKKINDA
    if any(w in p for w in ["hakkinda", "hakkinda", "nedir", "neyin", "ne marka", "brand", "kimsiniz", "neyi satiyorsunuz", "nasil", "tarihçe", "kurulus"]:
        return "Merhaba!\n\nBoomer Brand Hakkinda:\n\nBoomer Brand, Istanbul Merter'te kurulmus, kalite ve guven ilkeleriyle hareket eden bir giyim markasidir.\n\nKurucumuz **Suayip Solmaz** Bey, yillardir tekstil sektorunde çalışan, sektoru tum detaylariyla bilen, musteri memnuniyetini on planda tutan bir is insanidir.\n\nNeden Boomer Brand?\n- Kalite garantisi\n- Uygun fiyat\n- Guvenilir hizmet\n- Memnuniyet taihhudu\n- Hizli teslimat\n\nSiz de ailemizin bir parçasi olmak ister misiniz?\n\n" + WHATSAPP + " uzerinden iletisime gecebilirsiniz!"
    
    # SOSYAL MEDYA
    if any(w in p for w in ["instagram", "telegram", "facebook", "sosyal", "takip", "sayfa", "grup", "kanal", "insta"]):
        return "Merhaba!\n\nSosyal medyada da bizi takip edebilirsiniz!\n\n- Instagram: " + INSTAGRAM + "\n- Telegram: " + TELEGRAM + "\n\nKanallarimizda:\n- Ozel kampanyalar ve indirimler\n- Yeni urun duyurulari\n- Stil onerileri ve kombin ipuclari\n- Duyurular ve onemli haberler\n\nTakip edin, kacirmayin!"
    
    # VARSayıLAN
    return "Merhaba!\n\nBoomer Brand musteri temsilcisiyim!\n\nSizlere yardimci olmak için buradayim. Herhangi bir sorunuz olursa cekinmeyin.\n\nOrnegin:\n- Urunlerimiz hakkinda bilgi almak ister misiniz?\n- Fiyatlarimizi sormak mi istiyorsunuz?\n- Nasil siparis verilir ogrenmek mi istiyorsunuz?\n\n/katalog yazarak urunlerimizi görebilir veya direkt sorunuzu yazabilirsiniz!\n\nWhatsApp: " + WHATSAPP + " - 7/24 yaninizdayim!"