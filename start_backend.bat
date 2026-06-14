@echo off
title PC Yordamchi - Django Backend
color 0A
echo.
echo  ██████╗  ██████╗    ██╗   ██╗ ██████╗ ██████╗ ██████╗  █████╗ ███╗   ███╗ ██████╗██╗  ██╗██╗
echo  ██╔══██╗██╔════╝    ╚██╗ ██╔╝██╔═══██╗██╔══██╗██╔══██╗██╔══██╗████╗ ████║██╔════╝██║  ██║██║
echo  ██████╔╝██║          ╚████╔╝ ██║   ██║██████╔╝██║  ██║███████║██╔████╔██║██║     ███████║██║
echo  ██╔═══╝ ██║           ╚██╔╝  ██║   ██║██╔══██╗██║  ██║██╔══██║██║╚██╔╝██║██║     ██╔══██║██║
echo  ██║     ╚██████╗       ██║   ╚██████╔╝██║  ██║██████╔╝██║  ██║██║ ╚═╝ ██║╚██████╗██║  ██║██║
echo  ╚═╝      ╚═════╝       ╚═╝    ╚═════╝ ╚═╝  ╚═╝╚═════╝ ╚═╝  ╚═╝╚═╝     ╚═╝ ╚═════╝╚═╝  ╚═╝╚═╝
echo.
echo  O'zbek tilida ovozli PC boshqaruv tizimi
echo  ==========================================
echo.

cd /d "%~dp0backend"

echo [1/3] Kerakli paketlar tekshirilmoqda...
pip install django djangorestframework django-cors-headers psutil --quiet 2>nul
echo       OK

echo [2/3] Ma'lumotlar bazasi tayyorlanmoqda...
python manage.py migrate --run-syncdb 2>nul
echo       OK

echo [3/3] Server ishga tushirilmoqda...
echo.
echo  Server manzili: http://localhost:8000
echo  API manzili:    http://localhost:8000/api/
echo.
echo  Electron ilova uchun start_app.bat ni ishga tushiring
echo  Yopish uchun: Ctrl+C
echo.

python manage.py runserver 8000
pause
