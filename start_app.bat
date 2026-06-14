@echo off
title PC Yordamchi - Electron App
color 0B
echo.
echo  PC YORDAMCHI - Electron App ishga tushirilmoqda...
echo  ===================================================
echo.

cd /d "%~dp0electron-app"

echo [1/2] Node.js paketlari tekshirilmoqda...
if not exist node_modules (
    echo       npm install bajarilmoqda, biroz kuting...
    npm install
    echo       OK
) else (
    echo       OK - allaqachon o'rnatilgan
)

echo [2/2] Electron ilovasi ishga tushirilmoqda...
echo.
echo  ESLATMA: Avval start_backend.bat ni ishga tushiring!
echo.

npx electron .
pause
