# 🧠 SkillTwin - Adaptive AI Personal Mentor

> Next-generation AI learning system engineered for deep personalization, high-fidelity reasoning, multi-modal mastery assessment, and automated instructional content generation.

![SkillTwin](https://img.shields.io/badge/SkillTwin-AI%20Mentor-blue)
![Python](https://img.shields.io/badge/Python-3.11+-green)
![React](https://img.shields.io/badge/React-18.2-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.109-teal)

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Quick Start](#quick-start)
- [Detailed Setup](#detailed-setup)
- [API Documentation](#api-documentation)
- [Module Status](#module-status)
- [Troubleshooting](#troubleshooting)

## 🌟 Overview

SkillTwin is a precision-engineered AI Personal Mentor that models the learner's cognitive profile over time. The system generates individualized explanations, adaptive micro-lessons, speech-based mastery evaluations, and reliable integrity-protected assessments.

Unlike conventional EdTech tools, which rely on static difficulty progression or isolated Q&A systems, SkillTwin maintains an evolving, multi-modal profile of the learner and continuously adjusts instruction to match their conceptual state.

## ✨ Features

### Module 3.1 - Learning Twin Profile (LTP) ✅
- Persistent cognitive state modeling
- Knowledge graph with concept mastery tracking
- SM-2 spaced repetition algorithm
- Misconception identification and remediation
- Learning session analytics

### Module 3.2 - Dual RAG Personalized Reasoning ✅
- Academic content retrieval with ChromaDB
- Student context-aware responses
- Gap analysis and personalized recommendations
- Chat history with context persistence

### Module 3.3 - Micro Lessons 🔶 (Mock)
- Lesson generation endpoints (mock implementation)
- Ready for video/content integration

### Module 3.4 - Speech Assessment ⏳ (Placeholder)
- Placeholder for speech-based mastery evaluation

### Module 3.5 - Integrity Layer ⏳ (Placeholder)
- Placeholder for authentication and verification

## 🏗️ Project Structure

```
Metra/
├── backend/                      # FastAPI Backend
│   ├── app/
│   │   ├── core/                # Configuration & Database
│   │   │   ├── config.py        # Pydantic settings management
│   │   │   └── database.py      # SQLAlchemy async setup
│   │   ├── models/              # SQLAlchemy models
│   │   │   └── user.py          # User model
│   │   ├── modules/             # Feature modules
│   │   │   ├── ltp/             # 3.1 Learning Twin Profile ✅
│   │   │   │   ├── models.py    # LTP database models
│   │   │   │   ├── schemas.py   # Pydantic schemas
│   │   │   │   ├── service.py   # SM-2 spaced repetition
│   │   │   │   └── routes.py    # 20+ API endpoints
│   │   │   ├── dual_rag/        # 3.2 Dual RAG Engine ✅
│   │   │   │   ├── models.py    # RAG database models
│   │   │   │   ├── schemas.py   # Pydantic schemas
│   │   │   │   ├── service.py   # Dual RAG logic
│   │   │   │   ├── vector_store.py # ChromaDB integration
│   │   │   │   └── routes.py    # API endpoints
│   │   │   ├── micro_lessons/   # 3.3 Micro Lessons 🔶 (Mock)
│   │   │   │   ├── models.py
│   │   │   │   ├── schemas.py
│   │   │   │   └── routes.py
│   │   │   ├── speech_assessment/ # 3.4 Speech ⏳ (Placeholder)
│   │   │   │   └── models.py
│   │   │   └── integrity/       # 3.5 Integrity ⏳ (Placeholder)
│   │   │       └── models.py
│   │   └── main.py              # FastAPI app entry
│   ├── requirements.txt         # Python dependencies
│   └── .env.example             # Environment template
│
└── frontend/                    # Vite + React Frontend
    ├── src/
    │   ├── components/          # React components
    │   │   ├── ui/              # Shadcn/UI components
    │   │   ├── DashboardLayout.tsx
    │   │   ├── LearningFeed.tsx
    │   │   └── ...
    │   ├── pages/               # Page components
    │   │   ├── Index.tsx        # Dashboard
    │   │   ├── Chat.tsx         # AI Chat (Dual RAG)
    │   │   ├── Profile.tsx      # Learning Profile (LTP)
    │   │   └── Lessons.tsx      # Micro Lessons
    │   ├── lib/                 # Utilities
    │   │   ├── api.ts           # API client
    │   │   └── utils.ts         # Helper functions
    │   └── hooks/               # React hooks
    ├── package.json             # Node dependencies
    └── .env.example             # Environment template
```

## 📋 Prerequisites

Before starting, ensure you have:

- **Python** 3.11 or higher
- **Node.js** 18.x or higher
- **npm** 9.x or higher
- **OpenAI API Key** (for AI features)

To verify installations:
```powershell
python --version    # Should show Python 3.11+
node --version      # Should show v18.x+
npm --version       # Should show 9.x+
```

## 🚀 Quick Start

### Step 1: Navigate to Project
```powershell
cd c:\Saksham\Work\Hackathons\IITM\Metra
```

### Step 2: Backend Setup
```powershell
# Navigate to backend
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment (Windows PowerShell)
.\venv\Scripts\Activate.ps1

# If you get execution policy error, run this first:
# Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Install dependencies
pip install -r requirements.txt

# Create .env file from template
Copy-Item .env.example .env

# Open .env and add your OpenAI API key
notepad .env
```

### Step 3: Configure Backend Environment

Edit `backend/.env` file:
```env
# Application
APP_NAME=SkillTwin
DEBUG=True
SECRET_KEY=change-this-to-a-random-secret-key

# Database (SQLite for development)
DATABASE_URL=sqlite+aiosqlite:///./skilltwin.db

# OpenAI API - REQUIRED!
OPENAI_API_KEY=sk-your-openai-api-key-here

# ChromaDB Vector Store
CHROMA_PERSIST_DIRECTORY=./chroma_db

# JWT Settings
JWT_SECRET_KEY=change-this-to-another-random-key
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### Step 4: Frontend Setup
```powershell
# Open NEW terminal window
cd c:\Saksham\Work\Hackathons\IITM\Metra\frontend

# Install dependencies
npm install

# Create .env file from template
Copy-Item .env.example .env
```

### Step 5: Configure Frontend Environment

Edit `frontend/.env` file:
```env
VITE_API_URL=http://localhost:8000
```

### Step 6: Run the Application

**Terminal 1 - Backend:**
```powershell
cd c:\Saksham\Work\Hackathons\IITM\Metra\backend
.\venv\Scripts\Activate.ps1
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Terminal 2 - Frontend:**
```powershell
cd c:\Saksham\Work\Hackathons\IITM\Metra\frontend
npm run dev
```

### Step 7: Access the Application

| Service | URL |
|---------|-----|
| **Frontend** | http://localhost:8080 |
| **Backend API** | http://localhost:8000 |
| **API Docs (Swagger)** | http://localhost:8000/docs |
| **API Docs (ReDoc)** | http://localhost:8000/redoc |

## 📡 API Documentation

Once the backend is running, access interactive docs at http://localhost:8000/docs

### Key Endpoints

#### LTP (Learning Twin Profile) - `/api/v1/ltp`
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/profiles` | Create new learner profile |
| GET | `/profiles/{id}` | Get profile details |
| POST | `/concepts` | Add a concept |
| PUT | `/mastery/{id}` | Update concept mastery |
| GET | `/profiles/{id}/learning-path` | Get personalized learning path |
| POST | `/profiles/{id}/spaced-review` | Get spaced repetition items |
| GET | `/profiles/{id}/stats` | Get learning statistics |

#### Dual RAG - `/api/v1/rag`
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/query` | Query with personalized context |
| POST | `/contexts` | Create student context |
| POST | `/documents` | Add academic document |
| GET | `/gap-analysis/{profile_id}` | Analyze learning gaps |
| GET | `/chat-history/{profile_id}` | Get chat history |

#### Micro Lessons - `/api/v1/lessons`
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/generate` | Generate a micro lesson (mock) |
| GET | `/` | List all lessons |
| GET | `/{id}` | Get lesson details |

## 🔧 Module Status

| Module | Status | Implementation |
|--------|--------|----------------|
| 3.1 LTP | ✅ Complete | Full SM-2 algorithm, 20+ endpoints |
| 3.2 Dual RAG | ✅ Complete | ChromaDB + OpenAI integration |
| 3.3 Micro Lessons | 🔶 Mock | Endpoints with mock responses |
| 3.4 Speech | ⏳ Placeholder | Ready for implementation |
| 3.5 Integrity | ⏳ Placeholder | Ready for implementation |

## 🛠️ Troubleshooting

### Common Issues

#### 1. PowerShell Execution Policy Error
```powershell
# Run this command to allow script execution
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

#### 2. Port Already in Use
```powershell
# Find process using port 8000
netstat -ano | findstr :8000

# Kill the process (replace <PID> with actual PID)
taskkill /PID <PID> /F
```

#### 3. Module Not Found Errors
```powershell
# Ensure virtual environment is activated
.\venv\Scripts\Activate.ps1

# Reinstall dependencies
pip install -r requirements.txt
```

#### 4. OpenAI API Errors
- Verify your API key is correct in `.env` file
- Ensure the API key has sufficient credits
- Check you're using the correct key format: `sk-...`

#### 5. ChromaDB Errors
```powershell
# Delete the chroma_db folder and restart
Remove-Item -Recurse -Force .\chroma_db
```

#### 6. Frontend Build Errors
```powershell
# Clear npm cache and reinstall
npm cache clean --force
Remove-Item -Recurse -Force node_modules
npm install
```

## 👥 Team Distribution

| Module | Owner |
|--------|-------|
| 3.1 LTP | Your Implementation |
| 3.2 Dual RAG | Your Implementation |
| 3.3 Micro Lessons | Mock (Ready for extension) |
| 3.4 Speech Assessment | Friend's Implementation |
| 3.5 Integrity | Friend's Implementation |

## 📝 Development Notes

### Running in Development Mode

Both backend and frontend support hot-reload:
- Backend: `--reload` flag with uvicorn
- Frontend: Vite's built-in HMR

### Database

- Using SQLite for development (file: `skilltwin.db`)
- Tables are auto-created on first run
- For production, consider PostgreSQL

### Vector Store

- ChromaDB persists to `./chroma_db`
- Embeddings generated via sentence-transformers

## 📄 License

MIT License - See LICENSE file for details

---

**Built for IITM Hackathon** 🚀
