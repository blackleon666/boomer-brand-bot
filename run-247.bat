@echo off
REM ========================================
REM   BOOMER BRAND BOT - 7/24 CALISTIRICI
REM ========================================

REM Dizini sabitle
cd /d "%~dp0"

REM Sanal ortam yolu (OneDrive disina tasinmis)
set VENV_PATH=C:\Users\izumi\venv_boomer

echo ========================================
echo   Boomer Brand Bot Baslatiliyor...
echo ========================================
echo.
echo Calisma Dizini: %CD%
echo Sanal Ortam: %VENV_PATH%
echo.

REM Log klasoru
if not exist logs mkdir logs

REM Sanal ortam kontrol
if not exist "%VENV_PATH%\Scripts\python.exe" (
    echo HATA: Sanal ortam bulunamadi!
    echo.
    echo Lutfen asagidaki komutu PowerShell'de calistirin:
    echo python -m venv C:\Users\izumi\venv_boomer
    echo.
    pause
    exit /b 1
)

REM .env kontrol
if not exist .env (
    echo HATA: .env dosyasi bulunamadi!
    echo Konum: %CD%\.env
    pause
    exit /b 1
)

REM Sanal ortami aktif et
echo Sanal ortam aktif ediliyor...
call "%VENV_PATH%\Scripts\activate.bat"

REM Bagimliliklari yukle
echo Bagimliliklar kontrol ediliyor...
"%VENV_PATH%\Scripts\pip.exe" install -r requirements.txt -q

echo.
echo ========================================
echo   Bot calisiyor!
echo   Kapatmak icin bu pencereyi kapatin.
echo ========================================
echo.

REM Botu calistir
"%VENV_PATH%\Scripts\python.exe" bot.py

REM Bot kapandi
echo.
echo ========================================
echo   Bot kapandi!
echo   10 saniye sonra yeniden baslatiliyor...
echo ========================================
timeout /t 10 /nobreak
goto loop
