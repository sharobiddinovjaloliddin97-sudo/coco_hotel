# Coco Hotel — Boutique Hotel Web Application

Official web platform repository for Coco Hotel (Tashkent, Uzbekistan).

- **Existing website:** https://coco-hotel.uz/
- **Google / Yandex Location:** 156 Bogibuston Street, Tashkent

---

## Technology Stack

### Frontend
- **Framework:** React 19
- **Build Tool:** Vite
- **Styling:** Tailwind CSS (v4)
- **Routing:** react-router-dom
- **Icons & UI:** Custom SVG luxury icon suite, responsive mobile drawer
- **i18n:** Multi-language support (Uzbek, Russian, English)

### Backend
- **Language:** Python
- **Framework:** Django 5.2
- **API Toolkit:** Django REST Framework
- **Storage:** Supabase S3-compatible media storage (django-storages)
- **Database:** PostgreSQL (Neon / Supabase)

### Deployment & Infrastructure
- **Backend Hosting:** Railway
- **Storage Hosting:** Supabase
- **Database Hosting:** Supabase / Neon
- **Frontend Hosting:** Railway / Vercel

---

## Getting Started

### Backend Setup
```bash
cd backend
python -m venv .venv
# Windows:
.venv\Scripts\activate
# Linux/macOS:
source .venv/bin/activate

pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

### Frontend Setup
```bash
cd frontend
npm install
npm run dev
```
