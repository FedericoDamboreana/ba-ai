import os
from pathlib import Path
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from app.api import projects, items, questions, generation
from app.config import settings

app = FastAPI(title="ba-ai API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["Content-Disposition"],
)

# Register API routers
app.include_router(projects.router)
app.include_router(items.router)
app.include_router(questions.router)
app.include_router(generation.router)

# Serve static frontend files in production
# The frontend build output is copied to /app/static in Docker
STATIC_DIR = Path(__file__).parent / "static"
if STATIC_DIR.exists():
    # Serve static assets (JS, CSS, images)
    app.mount("/assets", StaticFiles(directory=STATIC_DIR / "assets"), name="assets")

    # Serve index.html for all non-API routes (SPA routing)
    @app.get("/{full_path:path}")
    async def serve_spa(full_path: str):
        # Don't serve SPA for API routes or health check
        if full_path.startswith("api/") or full_path == "health":
            return {"detail": "Not Found"}
        # Serve index.html for SPA routing
        index_path = STATIC_DIR / "index.html"
        if index_path.exists():
            return FileResponse(index_path)
        return {"detail": "Frontend not built"}

@app.get("/")
def root():
    # In production, serve the SPA
    if STATIC_DIR.exists():
        index_path = STATIC_DIR / "index.html"
        if index_path.exists():
            return FileResponse(index_path)
    return {"message": "ba-ai API"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}
