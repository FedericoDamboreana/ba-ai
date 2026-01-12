# ba-ai

AI-powered requirements documentation platform for Business Analysts.

## Tech Stack

- **Frontend**: React 18 + Tailwind CSS + React Query
- **Backend**: Python FastAPI + SQLAlchemy
- **Database**: SQLite (file: `data/ba-ai.db`)
- **AI**: OpenAI GPT-5 with structured outputs

## Project Structure

```
ba-ai/
├── frontend/          # React app
│   └── src/
│       ├── components/
│       ├── pages/
│       ├── hooks/
│       └── services/
├── backend/           # FastAPI app
│   └── app/
│       ├── api/
│       ├── models/
│       ├── services/
│       └── prompts/
├── data/              # SQLite database
└── docs/              # Documentation
```

## Commands

```bash
# Frontend
cd frontend && npm install
cd frontend && npm run dev        # Dev server on :5173

# Backend
cd backend && pip install -r requirements.txt
cd backend && uvicorn main:app --reload  # API on :8000

# Database
cd backend && alembic upgrade head  # Run migrations
```

## Key Conventions

- All code and UI text in English
- AI tone: formal, professional (German business clients)
- Use structured outputs (JSON schema) for all AI calls
- Dark theme with purple accents (#7C3AED)
- API prefix: `/api/`

## Testing Requirements

- Write tests for every new function/component
- Backend: pytest with pytest-asyncio
- Frontend: Vitest + React Testing Library
- Run tests after completing each task before moving on
- Never mark a phase complete if tests fail

## Commands
```bash
# ... existing commands ...

# Tests
cd backend && pytest                    # Run backend tests
cd frontend && npm test                 # Run frontend tests
cd frontend && npm run test:coverage    # With coverage
```

## Hooks (run automatically)

After completing any implementation:
1. Run relevant tests
2. Fix any failures before proceeding
3. Only then update PLAN.md

After editing files, run: `.claude/hooks/post-edit.sh`

## Important Files

- @docs/PRD.md - Full product requirements
- @docs/PLAN.md - Implementation checklist

## Don't

- Don't use class components (functional + hooks only)
- Don't hardcode API keys (use .env)
- Don't skip error handling on AI calls
- Don't use chat interface for questions (use list UI)