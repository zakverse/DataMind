from fastapi import APIRouter
from backend.app.core.config import settings
from backend.app.models.health import HealthResponse

router = APIRouter()


@router.get("/health", response_model=HealthResponse, summary="System Health Check")
def health_check() -> HealthResponse:
    """Returns the operational status of the DataMind backend system."""
    return HealthResponse(
        status="ok",
        app_name=settings.PROJECT_NAME,
        version=settings.VERSION,
        llm_configured=bool(settings.GEMINI_API_KEY),
    )
