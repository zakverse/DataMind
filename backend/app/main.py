from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from backend.app.api.router import api_router
from backend.app.core.config import settings
from backend.app.services.ai_service import ask_gemini

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="DataMind - AI-Powered Data Analytics Platform API",
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include modular API routers under /api/v1
app.include_router(api_router)


@app.get("/", summary="Root Index")
def root():
    """Welcome endpoint for DataMind API."""
    return {
        "app_name": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "message": "Welcome to DataMind API",
        "docs_url": "/docs",
        "health_check": f"{settings.API_V1_STR}/health",
    }


@app.get("/ask", summary="Quick Ask (Compatibility Route)")
def ask(question: str = Query(..., description="Pertanyaan untuk AI Gemini")):
    """Direct route for backward compatibility and quick testing."""
    answer = ask_gemini(question)
    return {
        "question": question,
        "answer": answer,
    }