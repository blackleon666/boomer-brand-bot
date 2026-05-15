@echo off
REM ========================================
REM   BOOMER BRAND BOT - CALISTIRICI
REM   7/24 Aktif Tutmak Icin
REM ========================================

echo.
echo ========================================
echo   Boomer Brand Bot Baslatiliyor...
echo ========================================
echo.

REM Ortam degiskenlerini kontrol et
if not exist .env (
    echo HATA: .env dosyasi bulunamadi!
    echo Lütfen .env dosyasini olusturun ve TELEGRAM_TOKEN ayarlayin.
    pause
    exit /b 1
)

REM Python sanal ortam kontrol
if not exist venv (
    echo Sanal ortam olusturuluyor...
    python -m venv venv
)

REM Sanal ortami aktif et
echo Sanal ortam aktif ediliyor...
call venv\Scripts\activate.bat

REM Bagimliliklari kontrol et
pip install -r requirements.txt

REM Botu calistir
echo.
echo ========================================
echo   Bot calisiyor! Ctrl+C ile durdurabilirsiniz.
echo ========================================
echo.

python bot.py

pause