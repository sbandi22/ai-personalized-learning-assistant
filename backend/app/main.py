"""FastAPI application entrypoint.

Run with:  uvicorn backend.app.main:app --reload
Docs:      http://localhost:8000/docs
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .config import settings
from .database import init_db
from .routers import students, courses, recommendations, analytics, auth

app = FastAPI(
    title=settings.app_name,
    version=settings.api_version,
    description="Adaptive, personalized learning-path recommendation API.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup():
    init_db()


@app.get("/", tags=["health"])
def root():
    return {"status": "ok", "service": settings.app_name,
            "version": settings.api_version}


@app.get("/health", tags=["health"])
def health():
    return {"status": "healthy"}


app.include_router(auth.router)
app.include_router(students.router)
app.include_router(courses.router)
app.include_router(recommendations.router)
app.include_router(analytics.router)
