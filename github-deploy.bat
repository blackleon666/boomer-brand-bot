@echo off
REM ==== BOOMER BRAND BOT - GITHUB YUKLEME SCRIPTI ====

echo.
echo ========================================
echo   BOOMER BRAND BOT - GitHub Yukleme
echo ========================================
echo.

REM GitHub'da yeni bir repo oluşturun:
REM 1. https://github.com/new adresine gidin
REM 2. "boomer-brand-bot" adında bir repository oluşturun
REM 3. "Create repository" butonuna tıklayın
REM 4. Aşağıdaki komutu orada gördüğünüz URL ile değiştirin

echo.
echo [1/3] GitHub URL'nizi girin (ornek: https://github.com/kullanici/boomer-brand-bot.git):
set /p GH_URL=

echo.
echo [2/3] Remote ekleniyor...
git remote add origin %GH_URL%

echo.
echo [3/3] GitHub'a yukleniyor...
git push -u origin master

echo.
echo ========================================
echo   Basariyla yuklendi!
echo ========================================
echo.
echo Render deployment icin:
echo 1. https://dashboard.render.com adresine gidin
echo 2. "New" > "Web Service" secin
echo 3. GitHub repository'nizi secin
echo 4. Build command: pip install -r requirements.txt
echo 5. Start command: python bot.py
echo 6. Environment variables ekleyin:
echo    - TELEGRAM_TOKEN
echo    - HF_API_KEY
echo    - ENCRYPTION_KEY
echo    - ADMIN_USER_IDS
echo    - WHATSAPP_LINK
echo.
pause