@echo off
title PC Yordamchi - To'liq ishga tushirish
color 0A

echo.
echo  ====================================================
echo   🤖 PC YORDAMCHI - O'zbek tilida ovozli boshqaruv
echo  ====================================================
echo.
echo  Django backend va Electron app bir vaqtda ishga tushadi
echo.

:: Backend alohida oynada
start "PC Yordamchi - Backend" cmd /k "cd /d "%~dp0backend" && echo Backend ishga tushmoqda... && pip install django djangorestframework django-cors-headers psutil -q && python manage.py migrate --run-syncdb 2>nul && echo. && echo Server: http://localhost:8000 && python manage.py runserver 8000"

:: 3 soniya kutish
timeout /t 3 /nobreak >nul

:: Electron app
cd /d "%~dp0electron-app"
if not exist node_modules (
    echo npm install bajarilmoqda...
    npm install
)

echo Electron app ishga tushmoqda...
npx electron .
