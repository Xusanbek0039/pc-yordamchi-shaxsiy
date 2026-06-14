# -*- coding: utf-8 -*-
"""
O'zbek tilida ovozli buyruqlarni tahlil qiluvchi modul.
Har bir buyruq uchun intent va parametrlar aniqlanadi.
"""

import re

# ==================== BUYRUQLAR LUG'ATI ====================

INTENTS = {
    # TIZIM
    'shutdown': {
        'keywords': ['o\'chir', 'kompyuterni o\'chir', 'o\'chirish', 'shutdown', 'yop'],
        'action': 'system_shutdown',
        'response': '💤 Kompyuter o\'chirilmoqda...'
    },
    'restart': {
        'keywords': ['qayta yuklash', 'restart', 'qayta ishga tushir', 'reboot'],
        'action': 'system_restart',
        'response': '🔄 Kompyuter qayta yuklanmoqda...'
    },
    'sleep': {
        'keywords': ['uxlat', 'sleep', 'kutish rejimi', 'uxlatish'],
        'action': 'system_sleep',
        'response': '😴 Kutish rejimiga o\'tilmoqda...'
    },
    'lock': {
        'keywords': ['qulf', 'lock', 'qulflash', 'ekranni qulflash'],
        'action': 'system_lock',
        'response': '🔒 Ekran qulflanmoqda...'
    },

    # OVOZ
    'volume_up': {
        'keywords': ['ovozni oshir', 'ovoz ko\'tar', 'balandroq', 'ovoz baland', 'volume up'],
        'action': 'volume_up',
        'response': '🔊 Ovoz balandlashtirildi'
    },
    'volume_down': {
        'keywords': ['ovozni kamayt', 'ovoz past', 'pastroq', 'volume down'],
        'action': 'volume_down',
        'response': '🔉 Ovoz pasaytirildi'
    },
    'mute': {
        'keywords': ['jim', 'ovozni o\'chir', 'mute', 'soqov'],
        'action': 'volume_mute',
        'response': '🔇 Ovoz o\'chirildi'
    },
    'unmute': {
        'keywords': ['ovozni yoq', 'unmute', 'ovoz yoq'],
        'action': 'volume_unmute',
        'response': '🔊 Ovoz yoqildi'
    },

    # ILOVALAR
    'open_browser': {
        'keywords': ['brauzer och', 'internet och', 'chrome och', 'firefox och', 'brauzerni och'],
        'action': 'open_app',
        'params': {'app': 'browser'},
        'response': '🌐 Brauzer ochilmoqda...'
    },
    'open_notepad': {
        'keywords': ['notepad och', 'matn muharrir', 'daftar och', 'yozuv och'],
        'action': 'open_app',
        'params': {'app': 'notepad'},
        'response': '📝 Notepad ochilmoqda...'
    },
    'open_calculator': {
        'keywords': ['kalkulyator', 'hisob kitob', 'calculator', 'hisoblash'],
        'action': 'open_app',
        'params': {'app': 'calculator'},
        'response': '🧮 Kalkulyator ochilmoqda...'
    },
    'open_explorer': {
        'keywords': ['fayl menejeri', 'papka', 'explorer', 'fayllarni ko\'rsat'],
        'action': 'open_app',
        'params': {'app': 'explorer'},
        'response': '📁 Fayl menejeri ochilmoqda...'
    },
    'open_vscode': {
        'keywords': ['vscode', 'vs code', 'visual studio', 'kod muharrir', 'coding'],
        'action': 'open_app',
        'params': {'app': 'vscode'},
        'response': '💻 VS Code ochilmoqda...'
    },
    'open_terminal': {
        'keywords': ['terminal', 'cmd', 'command prompt', 'powershell', 'konsol'],
        'action': 'open_app',
        'params': {'app': 'terminal'},
        'response': '⌨️ Terminal ochilmoqda...'
    },
    'open_task_manager': {
        'keywords': ['task manager', 'vazifalar', 'jarayonlar', 'taskmgr'],
        'action': 'open_app',
        'params': {'app': 'taskmgr'},
        'response': '📊 Task Manager ochilmoqda...'
    },

    # BRAUZER
    'open_youtube': {
        'keywords': ['youtube', 'video ko\'r', 'you tube'],
        'action': 'open_url',
        'params': {'url': 'https://youtube.com'},
        'response': '▶️ YouTube ochilmoqda...'
    },
    'open_google': {
        'keywords': ['google', 'qidirish', 'internet qidirish'],
        'action': 'open_url',
        'params': {'url': 'https://google.com'},
        'response': '🔍 Google ochilmoqda...'
    },
    'open_github': {
        'keywords': ['github', 'git hub', 'kod repozitoriya'],
        'action': 'open_url',
        'params': {'url': 'https://github.com'},
        'response': '🐙 GitHub ochilmoqda...'
    },
    'open_chatgpt': {
        'keywords': ['chatgpt', 'gpt', 'sun\'iy intellekt', 'ai'],
        'action': 'open_url',
        'params': {'url': 'https://chat.openai.com'},
        'response': '🤖 ChatGPT ochilmoqda...'
    },

    # FAYL BOSHQARUVI
    'create_folder': {
        'keywords': ['papka yarat', 'yangi papka', 'folder yarat', 'katalog yarat'],
        'action': 'file_create_folder',
        'response': '📁 Yangi papka yaratilmoqda...'
    },
    'list_files': {
        'keywords': ['fayllarni ko\'rsat', 'papkani ko\'rsat', 'nima bor', 'fayllar'],
        'action': 'file_list',
        'response': '📋 Fayllar ro\'yxati...'
    },
    'open_downloads': {
        'keywords': ['yuklanganlar', 'downloads', 'yuklamalar'],
        'action': 'open_folder',
        'params': {'folder': 'downloads'},
        'response': '⬇️ Downloads papkasi ochilmoqda...'
    },
    'open_desktop': {
        'keywords': ['ish stoli', 'desktop', 'rабочий стол'],
        'action': 'open_folder',
        'params': {'folder': 'desktop'},
        'response': '🖥️ Desktop ochilmoqda...'
    },
    'open_documents': {
        'keywords': ['hujjatlar', 'documents', 'documents papkasi'],
        'action': 'open_folder',
        'params': {'folder': 'documents'},
        'response': '📄 Documents papkasi ochilmoqda...'
    },

    # KOD BAJARISH
    'run_python': {
        'keywords': ['python ishga tushir', 'python run', 'py fayl', 'python skript'],
        'action': 'run_code',
        'params': {'lang': 'python'},
        'response': '🐍 Python kod bajarilmoqda...'
    },
    'run_node': {
        'keywords': ['node ishga tushir', 'nodejs run', 'node skript', 'javascript run'],
        'action': 'run_code',
        'params': {'lang': 'node'},
        'response': '📗 Node.js kod bajarilmoqda...'
    },

    # TIZIM MA'LUMOTI
    'system_info': {
        'keywords': ['tizim holati', 'kompyuter holati', 'ram', 'cpu', 'disk', 'protsessor', 'xotira'],
        'action': 'get_system_info',
        'response': '📊 Tizim ma\'lumotlari...'
    },
    'battery': {
        'keywords': ['batareya', 'battery', 'quvvat', 'zaryadka'],
        'action': 'get_battery',
        'response': '🔋 Batareya holati...'
    },
    'time': {
        'keywords': ['vaqt', 'soat', 'sana', 'bugun', 'time', 'date'],
        'action': 'get_time',
        'response': '🕐 Vaqt va sana...'
    },

    # SCREENSHOT
    'screenshot': {
        'keywords': ['skrinshot', 'screenshot', 'ekranni olish', 'ekran surati'],
        'action': 'take_screenshot',
        'response': '📸 Skrinshot olinmoqda...'
    },

    # SALOMLASHISH
    'greeting': {
        'keywords': ['salom', 'assalomu alaykum', 'hey', 'hi', 'hello'],
        'action': 'greeting',
        'response': '👋 Salom! Men PC Yordamchiman. Sizga qanday yordam bera olaman?'
    },
    'thanks': {
        'keywords': ['rahmat', 'tashakkur', 'thanks', 'thank you', 'rahmat senga'],
        'action': 'thanks',
        'response': '😊 Xush kelibsiz! Yana yordam kerak bo\'lsa, aytavering.'
    },

    # YOPISH
    'close_window': {
        'keywords': ['yopish', 'oynani yop', 'close', 'yop', 'chiqish'],
        'action': 'close_window',
        'response': '❌ Oyna yopilmoqda...'
    },
}

# ==================== WEB QIDIRISH ====================
SEARCH_PATTERNS = [
    r'(?:qidirish|search|qidirsin|izla)\s+(.+)',
    r'(.+)\s+(?:haqida qidir|haqida search|haqida izla)',
    r'(?:google|youtube|internet)da\s+(.+)\s+(?:qidir|izla|search)',
]

# ==================== URL OCHISH ====================
URL_PATTERNS = [
    r'(?:och|open|kir)\s+(.+\.(?:com|uz|ru|net|org|io|dev)(?:[^\s]*))',
    r'(?:saytga|saytini|sayt)\s+(.+\.(?:com|uz|ru|net|org))',
]

# ==================== FAYL YARATISH ====================
FILE_CREATE_PATTERNS = [
    r'(?:yarat|create|yangi)\s+(.+)\s+(?:nomli|deb atalgan)?\s*(?:papka|fayl|file|folder)',
    r'(?:papka|fayl)\s+(.+)\s+(?:yarat|create)',
]


def process_command(text: str) -> dict:
    """
    O'zbek tilidagi matnni tahlil qilib, buyruq va parametrlarni qaytaradi.
    """
    text_lower = text.lower().strip()

    # URL ochish
    for pattern in URL_PATTERNS:
        match = re.search(pattern, text_lower)
        if match:
            url = match.group(1)
            if not url.startswith('http'):
                url = 'https://' + url
            return {
                'intent': 'open_url',
                'action': 'open_url',
                'params': {'url': url},
                'response': f'🌐 {url} ochilmoqda...',
                'confidence': 0.9
            }

    # Qidirish
    for pattern in SEARCH_PATTERNS:
        match = re.search(pattern, text_lower)
        if match:
            query = match.group(1).strip()
            search_url = f'https://www.google.com/search?q={query.replace(" ", "+")}'
            return {
                'intent': 'search',
                'action': 'open_url',
                'params': {'url': search_url},
                'response': f'🔍 "{query}" qidirilmoqda...',
                'confidence': 0.9
            }

    # Fayl/papka yaratish
    for pattern in FILE_CREATE_PATTERNS:
        match = re.search(pattern, text_lower)
        if match:
            name = match.group(1).strip()
            return {
                'intent': 'create_folder',
                'action': 'file_create_folder',
                'params': {'name': name},
                'response': f'📁 "{name}" papkasi yaratilmoqda...',
                'confidence': 0.85
            }

    # Asosiy intentlarni tekshirish
    best_match = None
    best_score = 0

    for intent_name, intent_data in INTENTS.items():
        for keyword in intent_data['keywords']:
            if keyword in text_lower:
                score = len(keyword) / len(text_lower) + 0.5
                if score > best_score:
                    best_score = score
                    best_match = intent_name

    if best_match:
        intent_data = INTENTS[best_match]
        return {
            'intent': best_match,
            'action': intent_data['action'],
            'params': intent_data.get('params', {}),
            'response': intent_data['response'],
            'confidence': min(best_score, 1.0)
        }

    # Tushunilmadi
    return {
        'intent': 'unknown',
        'action': 'unknown',
        'params': {},
        'response': f'🤔 Kechirasiz, "{text}" buyrug\'ini tushunmadim. Iltimos boshqacha ayting.',
        'confidence': 0.0
    }


def get_suggestions(text: str) -> list:
    """Qisman mos keluvchi takliflar qaytaradi."""
    text_lower = text.lower().strip()
    suggestions = []

    for intent_name, intent_data in INTENTS.items():
        for keyword in intent_data['keywords']:
            if text_lower in keyword or keyword[:3] in text_lower:
                suggestions.append({
                    'text': keyword,
                    'intent': intent_name,
                    'icon': intent_data['response'].split()[0]
                })
                break

    return suggestions[:5]
