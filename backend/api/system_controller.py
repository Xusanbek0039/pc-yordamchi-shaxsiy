# -*- coding: utf-8 -*-
"""
Windows tizim buyruqlarini bajaruvchi modul.
PC ni boshqarish: ovoz, ilovalar, fayllar, tizim.
"""

import subprocess
import os
import sys
import platform
import datetime
import psutil
import json

IS_WINDOWS = platform.system() == 'Windows'


def _run(cmd, shell=True):
    """Shell buyruqni bajaradi."""
    try:
        result = subprocess.run(cmd, shell=shell, capture_output=True, text=True, timeout=10)
        return {'success': True, 'output': result.stdout, 'error': result.stderr}
    except Exception as e:
        return {'success': False, 'output': '', 'error': str(e)}


# ==================== TIZIM ====================

def system_shutdown():
    if IS_WINDOWS:
        return _run('shutdown /s /t 10')
    return _run('shutdown -h +1')


def system_restart():
    if IS_WINDOWS:
        return _run('shutdown /r /t 10')
    return _run('shutdown -r +1')


def system_sleep():
    if IS_WINDOWS:
        return _run('rundll32.exe powrprof.dll,SetSuspendState 0,1,0')
    return _run('systemctl suspend')


def system_lock():
    if IS_WINDOWS:
        return _run('rundll32.exe user32.dll,LockWorkStation')
    return _run('loginctl lock-session')


def cancel_shutdown():
    if IS_WINDOWS:
        return _run('shutdown /a')
    return _run('shutdown -c')


# ==================== OVOZ ====================

def volume_up(amount=10):
    """Ovozni oshirish."""
    if IS_WINDOWS:
        try:
            from ctypes import cast, POINTER
            from comtypes import CLSCTX_ALL
            from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
            devices = AudioUtilities.GetSpeakers()
            interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
            volume = cast(interface, POINTER(IAudioEndpointVolume))
            current = volume.GetMasterVolumeLevelScalar()
            new_vol = min(1.0, current + amount / 100)
            volume.SetMasterVolumeLevelScalar(new_vol, None)
            return {'success': True, 'volume': int(new_vol * 100)}
        except ImportError:
            # pycaw yo'q bo'lsa, PowerShell orqali
            script = f'$obj = New-Object -com wscript.shell; for($i=0;$i<{amount//2};$i++){{$obj.SendKeys([char]175)}}'
            result = _run(f'powershell -Command "{script}"')
            return result
    return {'success': False, 'error': 'Not Windows'}


def volume_down(amount=10):
    """Ovozni pasaytirish."""
    if IS_WINDOWS:
        try:
            from ctypes import cast, POINTER
            from comtypes import CLSCTX_ALL
            from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
            devices = AudioUtilities.GetSpeakers()
            interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
            volume = cast(interface, POINTER(IAudioEndpointVolume))
            current = volume.GetMasterVolumeLevelScalar()
            new_vol = max(0.0, current - amount / 100)
            volume.SetMasterVolumeLevelScalar(new_vol, None)
            return {'success': True, 'volume': int(new_vol * 100)}
        except ImportError:
            script = f'$obj = New-Object -com wscript.shell; for($i=0;$i<{amount//2};$i++){{$obj.SendKeys([char]174)}}'
            result = _run(f'powershell -Command "{script}"')
            return result
    return {'success': False, 'error': 'Not Windows'}


def volume_mute():
    """Ovozni o'chirish."""
    if IS_WINDOWS:
        script = '$obj = New-Object -com wscript.shell; $obj.SendKeys([char]173)'
        return _run(f'powershell -Command "{script}"')
    return {'success': False}


def volume_unmute():
    """Ovozni yoqish."""
    return volume_mute()  # Toggle


def get_volume():
    """Hozirgi ovoz darajasini qaytaradi."""
    if IS_WINDOWS:
        try:
            from ctypes import cast, POINTER
            from comtypes import CLSCTX_ALL
            from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
            devices = AudioUtilities.GetSpeakers()
            interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
            volume = cast(interface, POINTER(IAudioEndpointVolume))
            current = volume.GetMasterVolumeLevelScalar()
            return {'success': True, 'volume': int(current * 100)}
        except:
            return {'success': True, 'volume': 50}
    return {'success': True, 'volume': 50}


# ==================== ILOVALAR OCHISH ====================

APP_PATHS = {
    'browser': [
        r'C:\Program Files\Google\Chrome\Application\chrome.exe',
        r'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe',
        r'C:\Program Files\Mozilla Firefox\firefox.exe',
        r'C:\Program Files\Microsoft\Edge\Application\msedge.exe',
    ],
    'notepad': ['notepad.exe'],
    'calculator': ['calc.exe'],
    'explorer': ['explorer.exe'],
    'vscode': [
        r'C:\Users\{username}\AppData\Local\Programs\Microsoft VS Code\Code.exe',
        r'C:\Program Files\Microsoft VS Code\Code.exe',
        'code',
    ],
    'terminal': ['cmd.exe', 'powershell.exe'],
    'taskmgr': ['taskmgr.exe'],
    'paint': ['mspaint.exe'],
    'wordpad': ['wordpad.exe'],
    'snipping': ['SnippingTool.exe'],
}


def open_app(app: str):
    """Ilovani ishga tushirish."""
    if not IS_WINDOWS:
        return {'success': False, 'error': 'Only Windows supported'}

    username = os.environ.get('USERNAME', 'User')

    if app == 'browser':
        for path in APP_PATHS['browser']:
            path = path.replace('{username}', username)
            if os.path.exists(path):
                subprocess.Popen([path])
                return {'success': True, 'app': app}
        # default brauzer
        result = _run('start "" "http://www.google.com"')
        return {'success': True, 'app': 'browser'}

    if app in APP_PATHS:
        for exe in APP_PATHS[app]:
            exe = exe.replace('{username}', username)
            try:
                if os.path.exists(exe):
                    subprocess.Popen([exe])
                    return {'success': True, 'app': app}
                else:
                    subprocess.Popen(exe, shell=True)
                    return {'success': True, 'app': app}
            except:
                continue

    # Umumiy try
    try:
        subprocess.Popen(app, shell=True)
        return {'success': True, 'app': app}
    except Exception as e:
        return {'success': False, 'error': str(e)}


def open_url(url: str):
    """Brauzarda URL ochish."""
    if IS_WINDOWS:
        result = _run(f'start "" "{url}"')
        return {'success': True, 'url': url}
    else:
        result = _run(f'xdg-open "{url}"')
        return {'success': True, 'url': url}


def close_window():
    """Faol oynani yopish."""
    if IS_WINDOWS:
        script = 'Add-Type -AssemblyName Microsoft.VisualBasic; [Microsoft.VisualBasic.Interaction]::AppActivate((Get-Process | Where-Object {$_.MainWindowHandle -ne 0} | Select-Object -First 1).Id)'
        _run(f'powershell -Command "{script}"')
        import pyautogui
        pyautogui.hotkey('alt', 'f4')
        return {'success': True}
    return {'success': False}


# ==================== FAYL BOSHQARUVI ====================

def file_create_folder(name: str, path: str = None):
    """Yangi papka yaratish."""
    if path is None:
        path = os.path.join(os.path.expanduser('~'), 'Desktop')
    full_path = os.path.join(path, name)
    try:
        os.makedirs(full_path, exist_ok=True)
        return {'success': True, 'path': full_path}
    except Exception as e:
        return {'success': False, 'error': str(e)}


def file_list(path: str = None):
    """Papkadagi fayllarni ro'yxati."""
    if path is None:
        path = os.path.join(os.path.expanduser('~'), 'Desktop')
    try:
        items = []
        for item in os.listdir(path):
            full = os.path.join(path, item)
            items.append({
                'name': item,
                'type': 'folder' if os.path.isdir(full) else 'file',
                'size': os.path.getsize(full) if os.path.isfile(full) else 0,
            })
        return {'success': True, 'items': items[:20], 'path': path}
    except Exception as e:
        return {'success': False, 'error': str(e)}


def open_folder(folder: str):
    """Maxsus papkani ochish."""
    home = os.path.expanduser('~')
    folders = {
        'desktop': os.path.join(home, 'Desktop'),
        'downloads': os.path.join(home, 'Downloads'),
        'documents': os.path.join(home, 'Documents'),
        'pictures': os.path.join(home, 'Pictures'),
        'music': os.path.join(home, 'Music'),
        'videos': os.path.join(home, 'Videos'),
    }
    path = folders.get(folder, home)
    if IS_WINDOWS:
        subprocess.Popen(['explorer', path])
    else:
        subprocess.Popen(['xdg-open', path])
    return {'success': True, 'path': path}


# ==================== TIZIM MA'LUMOTI ====================

def get_system_info():
    """CPU, RAM, disk ma'lumotlari."""
    try:
        cpu_percent = psutil.cpu_percent(interval=0.5)
        ram = psutil.virtual_memory()
        disk = psutil.disk_usage('/')

        return {
            'success': True,
            'cpu': {
                'percent': cpu_percent,
                'cores': psutil.cpu_count(),
                'freq': psutil.cpu_freq().current if psutil.cpu_freq() else 0,
            },
            'ram': {
                'total': round(ram.total / (1024**3), 1),
                'used': round(ram.used / (1024**3), 1),
                'percent': ram.percent,
            },
            'disk': {
                'total': round(disk.total / (1024**3), 1),
                'used': round(disk.used / (1024**3), 1),
                'percent': disk.percent,
            },
            'platform': platform.system(),
            'hostname': platform.node(),
        }
    except Exception as e:
        return {'success': False, 'error': str(e)}


def get_battery():
    """Batareya holati."""
    try:
        battery = psutil.sensors_battery()
        if battery:
            return {
                'success': True,
                'percent': battery.percent,
                'plugged': battery.power_plugged,
                'time_left': battery.secsleft if battery.secsleft != psutil.POWER_TIME_UNLIMITED else -1,
            }
        return {'success': True, 'percent': 100, 'plugged': True, 'time_left': -1}
    except:
        return {'success': True, 'percent': 100, 'plugged': True, 'time_left': -1}


def get_time():
    """Hozirgi vaqt va sana."""
    now = datetime.datetime.now()
    days = ['Dushanba', 'Seshanba', 'Chorshanba', 'Payshanba', 'Juma', 'Shanba', 'Yakshanba']
    months = ['Yanvar', 'Fevral', 'Mart', 'Aprel', 'May', 'Iyun',
              'Iyul', 'Avgust', 'Sentabr', 'Oktabr', 'Noyabr', 'Dekabr']
    return {
        'success': True,
        'time': now.strftime('%H:%M:%S'),
        'date': f"{now.day} {months[now.month-1]} {now.year}",
        'day': days[now.weekday()],
        'full': now.strftime('%Y-%m-%d %H:%M:%S'),
    }


# ==================== KOD BAJARISH ====================

def run_code(lang: str, code: str):
    """Kodni bajarish."""
    import tempfile

    if lang == 'python':
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False, encoding='utf-8') as f:
            f.write(code)
            tmp_file = f.name
        try:
            result = subprocess.run(
                [sys.executable, tmp_file],
                capture_output=True, text=True, timeout=30
            )
            return {
                'success': result.returncode == 0,
                'output': result.stdout,
                'error': result.stderr,
                'returncode': result.returncode
            }
        finally:
            os.unlink(tmp_file)

    elif lang == 'node':
        with tempfile.NamedTemporaryFile(mode='w', suffix='.js', delete=False, encoding='utf-8') as f:
            f.write(code)
            tmp_file = f.name
        try:
            result = subprocess.run(
                ['node', tmp_file],
                capture_output=True, text=True, timeout=30
            )
            return {
                'success': result.returncode == 0,
                'output': result.stdout,
                'error': result.stderr,
                'returncode': result.returncode
            }
        finally:
            os.unlink(tmp_file)

    return {'success': False, 'error': f'Noto\'liq til: {lang}'}


# ==================== SCREENSHOT ====================

def take_screenshot():
    """Ekran suratini olish."""
    try:
        import pyautogui
        screenshot_dir = os.path.join(os.path.expanduser('~'), 'Pictures', 'Screenshots')
        os.makedirs(screenshot_dir, exist_ok=True)
        filename = f"screenshot_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        filepath = os.path.join(screenshot_dir, filename)
        screenshot = pyautogui.screenshot()
        screenshot.save(filepath)
        return {'success': True, 'path': filepath, 'filename': filename}
    except ImportError:
        if IS_WINDOWS:
            # PowerShell bilan
            screenshot_dir = os.path.join(os.path.expanduser('~'), 'Pictures', 'Screenshots')
            os.makedirs(screenshot_dir, exist_ok=True)
            filename = f"screenshot_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            filepath = os.path.join(screenshot_dir, filename)
            script = f'Add-Type -AssemblyName System.Windows.Forms; [System.Windows.Forms.Screen]::PrimaryScreen | Out-Null; $bitmap = [System.Drawing.Bitmap]::new([System.Windows.Forms.SystemInformation]::VirtualScreen.Width, [System.Windows.Forms.SystemInformation]::VirtualScreen.Height); $graphics = [System.Drawing.Graphics]::FromImage($bitmap); $graphics.CopyFromScreen([System.Windows.Forms.SystemInformation]::VirtualScreen.Location, [System.Drawing.Point]::Empty, [System.Windows.Forms.SystemInformation]::VirtualScreen.Size); $bitmap.Save("{filepath}")'
            _run(f'powershell -Command "{script}"')
            return {'success': True, 'path': filepath, 'filename': filename}
    except Exception as e:
        return {'success': False, 'error': str(e)}
