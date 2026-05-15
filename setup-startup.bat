@echo off
REM ========================================
REM   BOOMER BRAND BOT - WINDOWS STARTUP KURULUM
REM   Bilgisayar acildiginda otomatik baslatir
REM ========================================

echo.
echo ========================================
echo   7/24 Otomatik Baslatma Kurulumu
echo ========================================
echo.

REM Startup klasorune kisayol ekle
set STARTUP=%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup
set SCRIPT_PATH=%~dp0run-247.bat

echo Startup klasorune kisayol ekleniyor...
powershell -Command "$WshShell = New-Object -ComObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%STARTUP%\BoomerBot.lnk'); $Shortcut.TargetPath = '%SCRIPT_PATH%'; $Shortcut.WorkingDirectory = '%~dp0'; $Shortcut.WindowStyle = 7; $Shortcut.Save()"

echo.
echo ========================================
echo   KURULUM TAMAMLANDI!
echo ========================================
echo.
echo Her bilgisayar acildiginda bot otomatik baslayacak.
echo.
echo NOT: UptimeRobot icin asagidaki adimlari manuel yapin:
echo 1. uptimerobot.com'a kaydol
echo 2. New Monitor ^> HTTP(s)
echo 3. URL: http://DIS_IP_ADRESINIZ:10000/
echo 4. Interval: 5 minutes
echo.
echo DIS IP adresinizi ogrenmek icin: whatismyip.com
echo.
pause
