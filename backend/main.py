"""Main FastAPI application for DSA Mentor."""
import os
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from database import init_db
from routes import users, roadmap, problems, daily_plan, chat, stats, skill_tree, review, videos, patterns, faang_prep, settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize database on startup."""
    await init_db()
    yield


app = FastAPI(
    title="DSA Mentor - AI Interview Prep",
    description="Agentic AI application for personalized DSA interview preparation",
    version="1.0.0",
    lifespan=lifespan,
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API Routes
app.include_router(users.router, prefix="/api/users", tags=["Users"])
app.include_router(roadmap.router, prefix="/api/roadmap", tags=["Roadmap"])
app.include_router(problems.router, prefix="/api/problems", tags=["Problems"])
app.include_router(daily_plan.router, prefix="/api/daily-plan", tags=["Daily Plan"])
app.include_router(chat.router, prefix="/api/chat", tags=["Chat"])
app.include_router(stats.router, prefix="/api/stats", tags=["Stats"])
app.include_router(skill_tree.router, prefix="/api", tags=["Skill Tree"])
app.include_router(review.router, prefix="/api", tags=["Review"])
app.include_router(videos.router, prefix="/api", tags=["Videos"])
app.include_router(patterns.router, prefix="/api", tags=["Patterns"])
app.include_router(faang_prep.router, prefix="/api", tags=["FAANG Prep"])
app.include_router(settings.router, prefix="/api/settings", tags=["Settings"])

# Serve frontend static files
frontend_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "frontend", "dist")
if os.path.exists(frontend_dir):
    app.mount("/assets", StaticFiles(directory=os.path.join(frontend_dir, "assets")), name="assets")

    @app.get("/{full_path:path}")
    async def serve_frontend(full_path: str):
        """Serve the frontend SPA."""
        file_path = os.path.join(frontend_dir, full_path)
        if os.path.isfile(file_path):
            return FileResponse(file_path)
        return FileResponse(os.path.join(frontend_dir, "index.html"))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
