#!/bin/bash
# ========================================
#   BOOMER BRAND BOT - Linux/Mac Runner
#   7/24 Aktif Tutmak İçin
# ========================================

echo "========================================"
echo "  Boomer Brand Bot Başlatılıyor..."
echo "========================================"

# Sanal ortam oluştur (yoksa)
if [ ! -d "venv" ]; then
    echo "Sanal ortam oluşturuluyor..."
    python3 -m venv venv
fi

# Sanal ortamı aktif et
source venv/bin/activate

# Bağımlılıkları yükle
pip install -r requirements.txt

# Botu çalıştır (hata olursa yeniden başlat)
while true; do
    echo "Bot çalışıyor... (Ctrl+C ile durdur)"
    python bot.py
    echo "Bot durdu! 5 saniye içinde yeniden başlatılacak..."
    sleep 5
done