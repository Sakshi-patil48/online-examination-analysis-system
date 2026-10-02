# SMARTEXAMS - AI-Powered Online Examination & Performance Analysis Platform

SMARTEXAMS is a full-stack, AI-driven online examination system featuring role-based dashboards (Student, Examiner, Admin), AI short-answer semantic evaluation, server-synced proctored exam engine, autosave, and performance analytics.

---

## 🚀 Key Features

- **Role-Based Access Control (RBAC)**: Enforced both on Frontend (React Router) and Backend API (Django DRF).
  - 🎓 **Student**: Analytics Dashboard, Performance & Insights, My Exams, Question Bank, Public Exams, Exam Engine, Results Review.
  - 👩‍🏫 **Examiner**: Exam Creation, Question Bank Management (CRUD & Bulk Import), Student Analytics, Proctoring Audit.
  - 🛡️ **Admin**: System Overview, User Management, Audit Logs, Platform Stats.
- **SmartExams UI System**: Clean SaaS dashboard matching custom visual design language (Royal Blue `#2A3B8F` sidebar, white rounded cards, status badge pills).
- **AI Evaluation Engine**: Gemini AI integration for short-answer grading with automatic deterministic keyword/token overlap fallback.
- **Proctored Exam Engine**: Server-synced countdown timer, question palette, answer autosave, refresh recovery, and submission verification.

---

## 🛠️ Technology Stack

- **Frontend**: React 18, Vite, React Router v6, Redux Toolkit, Axios, Lucide Icons, Custom CSS.
- **Backend**: Python 3.14 / 3.13, Django 5, Django REST Framework, SimpleJWT, CORS Headers, SQLite.
- **AI/ML**: Gemini API (`google-genai`) with fallback keyword matcher.

---

## 🔑 Demo Login Credentials

| Role | Email / Username | Password |
| :--- | :--- | :--- |
| 🎓 **Student** | `student@smartexams.com` | `student123` |
| 👩‍🏫 **Examiner** | `teacher@smartexams.com` | `teacher123` |
| 🛡️ **Admin** | `admin@smartexams.com` | `admin123` |

---

## 💻 Quick Start & Setup

### 1. Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create & activate virtual environment (if not created)
python -m venv venv
# Windows:
..\venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
pip install Pillow

# Run database migrations
python manage.py makemigrations core
python manage.py migrate

# Seed demo users & sample exams
python manage.py seed_data

# Start Django backend server (Port 8000)
python manage.py runserver 127.0.0.1:8000
```

### 2. Frontend Setup

```bash
# Navigate to frontend directory
cd frontend

# Install node dependencies
npm install

# Start Vite React development server (Port 5173)
npm run dev -- --port 5173
```

---

## 🔗 Local Access Links

- **Frontend Application**: [http://localhost:5173/](http://localhost:5173/)
- **Backend REST API**: [http://127.0.0.1:8000/api/](http://127.0.0.1:8000/api/)
- **Django Admin Panel**: [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)
