# ba-ai - Implementation Plan

Use this as a checklist. Mark items `[x]` when complete.

---

## Phase 1: Project Setup (~30 min) ✓

### Backend Setup
- [x] Create `backend/` directory structure
- [x] Create `requirements.txt` with dependencies:
  - fastapi
  - uvicorn
  - sqlalchemy
  - python-dotx
  - openai
  - python-dotenv
  - alembic
- [x] Create `main.py` with FastAPI app
- [x] Create `.env.example` with `OPENAI_API_KEY=`
- [x] Add `.env` to `.gitignore`

### Frontend Setup
- [x] Create React app with Vite: `npm create vite@latest frontend -- --template react`
- [x] Install dependencies:
  - tailwindcss, postcss, autoprefixer
  - @tanstack/react-query
  - react-router-dom
  - lucide-react (icons)
  - axios
- [x] Configure Tailwind with dark theme colors
- [x] Set up React Query provider
- [x] Set up React Router

### Database Setup
- [x] Create SQLAlchemy models (Project, DocumentationItem, Question)
- [x] Configure SQLite connection
- [x] Create `data/` directory for database
- [x] Set up Alembic for migrations
- [x] Create initial migration

### Testing Setup
- [x] Backend: Add pytest, pytest-asyncio, httpx to requirements.txt
- [x] Backend: Create `tests/` directory with `conftest.py`
- [x] Frontend: Install vitest, @testing-library/react, @testing-library/jest-dom
- [x] Frontend: Configure vitest.config.js
- [x] Verify both test runners work with a dummy test

---

## Phase 2: Core Backend (~1.5 hours) ✓

### Models
- [x] `models/project.py` - Project model with all fields
- [x] `models/documentation_item.py` - DocItem model
- [x] `models/question.py` - Question model with conditionals
- [x] `models/enums.py` - Status enums

### API Routes
- [x] `api/projects.py`
  - [x] GET /api/projects (list with status filter)
  - [x] POST /api/projects (create)
  - [x] GET /api/projects/{id}
  - [x] PUT /api/projects/{id}
  - [x] DELETE /api/projects/{id}
  - [x] PATCH /api/projects/{id}/archive
- [x] `api/items.py`
  - [x] GET /api/projects/{id}/items
  - [x] POST /api/projects/{id}/items
  - [x] GET /api/items/{id}
  - [x] PUT /api/items/{id}
  - [x] DELETE /api/items/{id}
- [x] `api/questions.py`
  - [x] GET /api/items/{id}/questions
  - [x] PUT /api/questions/{id}
  - [x] POST /api/items/{id}/validate
- [x] `api/generation.py`
  - [x] POST /api/items/{id}/generate (placeholder)
  - [x] POST /api/items/{id}/regenerate (placeholder)
  - [x] GET /api/items/{id}/export (placeholder)

### Services
- [x] `services/project_service.py` - CRUD operations
- [x] `services/item_service.py` - CRUD + status management
- [x] `services/question_service.py` - Answer handling

### Tests
- [x] Write tests for all new endpoints/functions
- [x] Run full test suite
- [x] All tests passing (25 tests, 0 warnings)

---

## Phase 3: AI Integration (~1.5 hours) ✓

### OpenAI Client
- [x] `services/ai_service.py`
  - [x] Configure OpenAI client
  - [x] Implement structured output parsing
  - [x] Handle API errors gracefully

### Prompts
- [ ] `prompts/question_generation.py`
  - [ ] System prompt template
  - [ ] Response schema definition
  - [ ] Context assembly function
- [ ] `prompts/doc_generation.py`
  - [ ] System prompt per doc type
  - [ ] User Story response schema
  - [ ] PRD response schema
  - [ ] Epic response schema
  - [ ] FRS response schema
- [ ] `prompts/knowledge_base.py`
  - [ ] Update prompt template
  - [ ] Merge function for KB updates

### AI Functions
- [ ] `generate_questions(item, project)` → Question[]
- [ ] `validate_completeness(item)` → {complete: bool, missing: string[]}
- [ ] `generate_documentation(item, feedback?)` → GeneratedDoc
- [ ] `update_knowledge_base(project, item, doc)` → string

### Tests
- [ ] Write tests for all new endpoints/functions
- [ ] Run full test suite
- [ ] All tests passing

---

## Phase 4: Frontend Core (~2 hours)

### Layout & Navigation
- [ ] `components/Layout.jsx` - Dark theme wrapper
- [ ] `components/Header.jsx` - Logo, nav
- [ ] `components/Sidebar.jsx` - If needed
- [ ] Configure routes in `App.jsx`

### Project Pages
- [ ] `pages/ProjectsList.jsx`
  - [ ] Filter tabs (All/Active/Archived)
  - [ ] Project cards grid
  - [ ] Empty state
  - [ ] New Project button → modal
- [ ] `pages/ProjectDetail.jsx`
  - [ ] Breadcrumb
  - [ ] Project info header
  - [ ] Documentation items list
  - [ ] New Documentation dropdown
- [ ] `components/ProjectForm.jsx` - Create/Edit modal
- [ ] `components/ProjectCard.jsx` - Card component

### Documentation Item Pages
- [ ] `pages/DocumentationItem.jsx`
  - [ ] Header with title, type, progress
  - [ ] Questions list
  - [ ] Generate button (fixed footer)
- [ ] `pages/DocumentationPreview.jsx`
  - [ ] Generated content display
  - [ ] Copy buttons per field
  - [ ] Edit mode
  - [ ] Action buttons

### Components
- [ ] `components/QuestionList.jsx` - Questions container
- [ ] `components/QuestionRow.jsx` - Expandable row
- [ ] `components/QuestionInput.jsx` - Text/MC/Checkbox inputs
- [ ] `components/DocumentationOutput.jsx` - Formatted output
- [ ] `components/BDDScenario.jsx` - Gherkin display
- [ ] `components/StatusBadge.jsx` - Status indicators
- [ ] `components/DeadlineWarning.jsx` - Warning alert

### Hooks
- [ ] `hooks/useProjects.js` - Projects CRUD
- [ ] `hooks/useDocumentationItem.js` - Item + questions
- [ ] `hooks/useQuestions.js` - Answer management
- [ ] `hooks/useGeneration.js` - Generate/regenerate

### Services
- [ ] `services/api.js` - Axios instance with base URL
- [ ] `services/projectsApi.js` - Project endpoints
- [ ] `services/itemsApi.js` - Item endpoints
- [ ] `services/questionsApi.js` - Question endpoints
- [ ] `services/generationApi.js` - Generation endpoints

### Tests
- [ ] Write tests for all new endpoints/functions
- [ ] Run full test suite
- [ ] All tests passing

---

## Phase 5: Document Export (~30 min)

### Word Export
- [ ] `services/export_service.py`
  - [ ] Create docx from generated content
  - [ ] Format User Story properly
  - [ ] Format BDD scenarios
  - [ ] Add styling (fonts, spacing)
- [ ] Return file as download response

### Tests
- [ ] Write tests for all new endpoints/functions
- [ ] Run full test suite
- [ ] All tests passing

---

## Phase 6: Polish (~1 hour)

### Error Handling
- [ ] API error responses (proper status codes)
- [ ] Frontend error boundaries
- [ ] Toast notifications for actions
- [ ] Loading states/skeletons

### UX Improvements
- [ ] Confirm dialogs for delete
- [ ] Auto-save indicators
- [ ] Progress persistence verification
- [ ] Mobile responsive tweaks

### Final Testing
- [ ] Create project flow
- [ ] Create documentation item flow
- [ ] Answer questions flow
- [ ] Generate documentation flow
- [ ] Edit and export flow
- [ ] Regenerate with feedback flow

### Tests
- [ ] Write tests for all new endpoints/functions
- [ ] Run full test suite
- [ ] All tests passing

---

## File Checklist

```
ba-ai/
├── CLAUDE.md ✓
├── .gitignore
├── README.md
├── docs/
│   ├── PRD.md ✓
│   └── PLAN.md ✓
├── frontend/
│   ├── package.json
│   ├── vite.config.js
│   ├── tailwind.config.js
│   ├── postcss.config.js
│   ├── index.html
│   └── src/
│       ├── main.jsx
│       ├── App.jsx
│       ├── index.css
│       ├── components/
│       │   ├── Layout.jsx
│       │   ├── Header.jsx
│       │   ├── ProjectCard.jsx
│       │   ├── ProjectForm.jsx
│       │   ├── QuestionList.jsx
│       │   ├── QuestionRow.jsx
│       │   ├── QuestionInput.jsx
│       │   ├── DocumentationOutput.jsx
│       │   ├── BDDScenario.jsx
│       │   ├── StatusBadge.jsx
│       │   └── DeadlineWarning.jsx
│       ├── pages/
│       │   ├── ProjectsList.jsx
│       │   ├── ProjectDetail.jsx
│       │   ├── DocumentationItem.jsx
│       │   └── DocumentationPreview.jsx
│       ├── hooks/
│       │   ├── useProjects.js
│       │   ├── useDocumentationItem.js
│       │   ├── useQuestions.js
│       │   └── useGeneration.js
│       └── services/
│           ├── api.js
│           ├── projectsApi.js
│           ├── itemsApi.js
│           ├── questionsApi.js
│           └── generationApi.js
├── backend/
│   ├── main.py
│   ├── requirements.txt
│   ├── .env.example
│   ├── alembic.ini
│   ├── alembic/
│   └── app/
│       ├── __init__.py
│       ├── config.py
│       ├── database.py
│       ├── models/
│       │   ├── __init__.py
│       │   ├── project.py
│       │   ├── documentation_item.py
│       │   ├── question.py
│       │   └── enums.py
│       ├── api/
│       │   ├── __init__.py
│       │   ├── projects.py
│       │   ├── items.py
│       │   ├── questions.py
│       │   └── generation.py
│       ├── services/
│       │   ├── __init__.py
│       │   ├── project_service.py
│       │   ├── item_service.py
│       │   ├── question_service.py
│       │   ├── ai_service.py
│       │   └── export_service.py
│       └── prompts/
│           ├── __init__.py
│           ├── question_generation.py
│           ├── doc_generation.py
│           └── knowledge_base.py
└── data/
    └── ba-ai.db
```

---

## Quick Commands Reference

```bash
# Start backend
cd backend && uvicorn main:app --reload

# Start frontend
cd frontend && npm run dev

# Run migrations
cd backend && alembic upgrade head

# Create new migration
cd backend && alembic revision --autogenerate -m "description"
```