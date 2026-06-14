# 🤖 PC Yordamchi — O'zbek tilida ovozli PC boshqaruv

**Django REST API + Electron Desktop App**

---

## 🚀 Ishga tushirish

### Birinchi marta (o'rnatish):

```
START_HERE.bat — ikki marta bosing
```

Yoki alohida:
1. `start_backend.bat` — Django serverni ishga tushirish
2. `start_app.bat` — Electron ilovani ochish

---

## 📋 Talablar

- Python 3.10+
- Node.js 18+
- npm

---

## 🎤 Ovoz buyruqlari (O'zbek tilida)

### Ilovalar
| Buyruq | Natija |
|--------|--------|
| "brauzer och" | Chrome/Firefox ochiladi |
| "vscode och" | VS Code ochiladi |
| "terminal och" | CMD ochiladi |
| "kalkulyator" | Kalkulyator ochiladi |
| "fayl menejeri" | Explorer ochiladi |

### Internet
| Buyruq | Natija |
|--------|--------|
| "youtube" | YouTube ochiladi |
| "google" | Google ochiladi |
| "github" | GitHub ochiladi |
| "qidirish [narsa]" | Google qidirish |
| "och [sayt.com]" | Sayt ochiladi |

### Tizim
| Buyruq | Natija |
|--------|--------|
| "ovozni oshir" | Volume +10% |
| "ovozni kamayt" | Volume -10% |
| "jim" | Mute |
| "tizim holati" | CPU/RAM/Disk ko'rsatish |
| "skrinshot" | Ekran surati |
| "qulflash" | Ekranni qulflash |
| "uxlatish" | Sleep mode |

### Fayllar
| Buyruq | Natija |
|--------|--------|
| "downloads" | Downloads papkasi |
| "ish stoli" | Desktop ochish |
| "hujjatlar" | Documents ochish |
| "papka yarat [nom]" | Yangi papka |

---

## ⌨️ Tez tugmalar

| Tugma | Vazifa |
|-------|--------|
| `Ctrl+Shift+V` | Ovozni yoqish/o'chirish |

---

## 🔑 Whisper AI (ixtiyoriy)

Aniqroq ovoz tanish uchun:

```
set OPENAI_API_KEY=sk-...
start_backend.bat
```

---

## 📁 Loyiha tuzilishi

```
pc-assistant/
├── backend/              ← Django REST API
│   ├── api/
│   │   ├── uzbek_processor.py   ← O'zbek NLP
│   │   ├── system_controller.py ← PC boshqaruv
│   │   ├── views.py             ← API endpointlar
│   │   └── urls.py
│   └── pc_assistant/
│       ├── settings.py
│       └── urls.py
├── electron-app/         ← Desktop UI
│   ├── main.js           ← Electron asosiy
│   ├── preload.js
│   └── renderer/
│       └── index.html    ← Chiroyli UI
├── START_HERE.bat        ← Bitta bosish bilan ishga tushirish
├── start_backend.bat
└── start_app.bat
```

---

## 🌐 API Endpointlar

| URL | Metod | Vazifa |
|-----|-------|--------|
| `/api/command/` | POST | Buyruq yuborish |
| `/api/status/` | GET | Tizim holati |
| `/api/code/run/` | POST | Kod bajarish |
| `/api/speech/transcribe/` | POST | Audio → Matn |

