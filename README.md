# Boomer Brand Telegram AI Müşteri Temsilcisi

## 🚀 Quick Start (Render)

1. **Bu projeyi GitHub'a yükleyin**
2. **Render'da yeni bir Web Service oluşturun**
3. **Build Command**: `pip install -r requirements.txt`
4. **Start Command**: `python bot.py`
5. **Environment Variables** ekleyin:
   - `TELEGRAM_TOKEN` - Telegram Bot Token
   - `HF_API_KEY` - HuggingFace API Key (opsiyonel)
   - `ENCRYPTION_KEY` - Şifreleme anahtarı
   - `ADMIN_USER_IDS` - Admin Telegram ID'leri (virgülle ayrılmış)
   - `WHATSAPP_LINK` - WhatsApp linki

## 📋 Özellikler

- ✅ 7/24 aktif Telegram botu
- ✅ WhatsApp yönlendirme (fiyat, kampanya)
- ✅ Ürün kataloğu (sosyal medyadan gerçek ürünler)
- ✅ Sipariş ve takip sistemi
- ✅ Şikayet/iade yönetimi
- ✅ Şifreli loglama
- ✅ Marka temsili bilinci

## 🛠️ Yerel Çalıştırma

```bash
# 1. Klonla
git clone <repo-url>
cd boomer_brand_bot

# 2. Sanal ortam oluştur
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# 3. Bağımlılıkları yükle
pip install -r requirements.txt

# 4. .env dosyasını düzenle
cp .env.example .env
# .env dosyasını Telegram Token ile doldur

# 5. Çalıştır
python bot.py
```

## 📁 Proje Yapısı

```
boomer_brand_bot/
├── bot.py           # Ana bot dosyası
├── config.py        # Yapılandırma
├── handlers/        # Komut işleyicileri
│   ├── start.py     # /start, /help
│   ├── catalog.py   # /katalog
│   ├── order.py     # /siparis, /durum
│   ├── complaint.py # /sikayet
│   ├── marketing.py# /kampanya
│   └── analytics.py # /stats
├── db/              # Veritabanı
│   ├── models.py    # SQLAlchemy modelleri
│   └── repo.py      # Veritabanı işlemleri
├── llm/             # Yapay Zeka
│   └── inference.py # HuggingFace entegrasyonu
├── crypto/          # Şifreleme
│   └── encrypt.py   # Fernet şifreleme
└── data/            # Veri dosyaları
```

## ⚙️ Komutlar

| Komut | Açıklama |
|-------|----------|
| `/start` | Botu başlat |
| `/help` | Yardım menüsü |
| `/katalog` | Ürünleri göster |
| `/siparis <id>` | Sipariş ver |
| `/durum <no>` | Sipariş durumu |
| `/sikayet` | Şikayet bildir |
| `/kampanya` | Kampanyaları göster (admin) |
| `/stats` | İstatistikler |

## 🔐 Güvenlik

- Şifreleme anahtarı ortam değişkenlerinde tutulmalı
- `.env` dosyası asla repoya eklenmemeli
- Kişisel veriler şifreli olarak saklanır

## 📝 License

Özel proje - Boomer Brand