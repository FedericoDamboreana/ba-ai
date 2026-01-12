# ReqScribe

AI-powered requirements documentation platform for Business Analysts.

## Tech Stack

- **Frontend**: React 18 + Vite + Tailwind CSS + React Query
- **Backend**: Python FastAPI + SQLAlchemy + Alembic
- **Database**: SQLite
- **AI**: OpenAI GPT-5 with structured outputs
- **Testing**: Pytest (backend) + Vitest (frontend)

## Project Structure

```
ba-ai/
├── backend/
│   ├── app/
│   │   ├── api/          # API endpoints
│   │   ├── models/       # SQLAlchemy models
│   │   ├── services/     # Business logic
│   │   ├── prompts/      # AI prompt templates
│   │   ├── config.py
│   │   └── database.py
│   ├── tests/            # Backend tests
│   ├── alembic/          # Database migrations
│   ├── data/             # SQLite database
│   ├── main.py           # FastAPI application
│   └── requirements.txt
├── frontend/
│   └── src/
│       ├── components/   # React components
│       ├── pages/        # Page components
│       ├── hooks/        # Custom hooks
│       └── services/     # API clients
└── docs/
    ├── PRD.md           # Product Requirements
    └── PLAN.md          # Implementation Plan
```

## Setup

### Backend Setup

```bash
cd backend
pip install -r requirements.txt
```

Create a `.env` file:
```
OPENAI_API_KEY=your_api_key_here
```

Run migrations:
```bash
alembic upgrade head
```

Start the server:
```bash
uvicorn main:app --reload
```

API will be available at http://localhost:8000

### Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

Frontend will be available at http://localhost:5173

## Testing

### Backend Tests

```bash
cd backend
pytest
```

### Frontend Tests

```bash
cd frontend
npm test
```

## Phase 1 Completed ✓

- [x] Backend directory structure
- [x] FastAPI app with CORS
- [x] SQLAlchemy models (Project, DocumentationItem, Question)
- [x] Alembic migrations setup
- [x] Pytest testing infrastructure
- [x] React + Vite frontend
- [x] Tailwind CSS with dark theme
- [x] React Query setup
- [x] React Router setup
- [x] Vitest testing infrastructure
- [x] All verification tests passing

## Next Steps

See [docs/PLAN.md](docs/PLAN.md) for the full implementation roadmap. Ready to proceed with Phase 2: Core Backend.
