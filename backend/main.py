from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import projects, items, questions, generation

app = FastAPI(title="ReqScribe API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register API routers
app.include_router(projects.router)
app.include_router(items.router)
app.include_router(questions.router)
app.include_router(generation.router)

@app.get("/")
def root():
    return {"message": "ReqScribe API"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}
