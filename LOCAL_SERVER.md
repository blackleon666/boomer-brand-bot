# 🏠 Yerel Sunucuda 7/24 Çalıştırma Rehberi

## Seçenek 1: Windows Bilgisayarda (Basit)

### 1. Botu Çalıştırma
```cmd
cd boomer_brand_bot
run.bat
```

Bot `python bot.py` komutuyla çalışır ve sürekli olarak Telegram'dan mesajları çeker (polling).

### 2. Otomatik Başlatma (Windows'ta)
- Başlat menüsü → "Görev Zamanlayıcı" → "Görev Oluştur"
- Program yolu: `C:\Users\SIZIN\yolu\boomer_brand_bot\run.bat`
- "Bilgisayar açılınca otomatik başla" seçeneğini işaretle

---

## Seçenek 2: WiFi Ağından Dışarıya Erişim (ngrok)

Telegram webhooks kullanmak istersen ngrok kullan:

### 1. ngrok indir
https://ngrok.com/download

### 2. Çalıştır
```cmd
ngrok http 10000
```

Bu komut "https://xxxx.ngrok.io" gibi bir URL verir.

### 3. Webhook Ayarla
```cmd
ngrok http 10000
```
Çıkan URL'yi al ve şu komutu çalıştır:
```
https://api.telegram.org/bot<TOKEN>/setWebhook?url=https://xxxx.ngrok.io
```

---

## Seçenek 3: Linux/Raspberry Pi

```bash
chmod +x run.sh
./run.sh &
```

---

## ÖNEMLİ: 7/24 İçin Gerekenler

1. ✅ Bilgisayar sürekli açık kalsın (sleep/hibernate kapalı)
2. ✅ İnternet bağlantısı kesilirse bot otomatik yeniden bağlanır
3. ✅ Elektrik kesilirse bilgisayar otomatik açılsın (BIOS ayarı)
4. ✅ Bot crash olursa otomatik yeniden başlasın (bot.py'de auto-restart var)

---

## Hızlı Başlangıç

```cmd
# 1. GitHub'dan çek
git clone https://github.com/blackleon666/boomer-brand-bot.git
cd boomer-brand-bot

# 2. Ortam oluştur
python -m venv venv
venv\Scripts\activate

# 3. Bağımlılıklar
pip install -r requirements.txt

# 4. .env dosyasını düzenle (TOKEN'ı değiştir)

# 5. Çalıştır
python bot.py
```

Bot çalışmaya başlayacak ve 7/24 mesajları dinleyecek!