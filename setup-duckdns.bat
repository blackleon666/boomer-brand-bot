@echo off
REM ========================================
REM   DUCKDNS - OTOMATIK KURULUM
REM ========================================

echo.
echo ========================================
echo   DuckDNS Kurulum Sihirbazi
echo ========================================
echo.
echo 1. https://www.duckdns.org adresine gidin
echo 2. Google/Hesabinizla giris yapin
echo 3. Bir domain olusturun (orn: boomerbot.duckdns.org)
echo 4. Token degerini kopyalayin
echo.
pause

set /p DOMAIN="DuckDNS Domain (sonu .duckdns.org olmadan): "
set /p TOKEN="DuckDNS Token: "

REM Script olustur
echo Oluşturuluyor: %DOMAIN%.duckdns.org >> install.log

(
echo @echo off
echo :loop
echo curl -s "https://www.duckdns.org/update?domains=%DOMAIN%^&token=%TOKEN%^&ip=" ^>nul
echo timeout /t 300 /nobreak ^>nul
echo goto loop
) > duckdns-updater.bat

REM Startup'a ekle
set STARTUP=%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup
powershell -Command "$WshShell = New-Object -ComObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%STARTUP%\DuckDNS.lnk'); $Shortcut.TargetPath = '%~dp0duckdns-updater.bat'; $Shortcut.WorkingDirectory = '%~dp0'; $Shortcut.WindowStyle = 7; $Shortcut.Save()"

echo.
echo ========================================
echo   KURULUM TAMAMLANDI!
echo ========================================
echo.
echo Adresiniz: %DOMAIN%.duckdns.org
echo.
echo Simdi UptimeRobot'ta bu adresi kullanin:
echo https://%DOMAIN%.duckdns.org:10000/
echo.
pause
