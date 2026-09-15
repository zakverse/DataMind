from fastapi import APIRouter, HTTPException, Query, status
from backend.app.core.config import settings
from backend.app.models.ai import AskRequest, AskResponse
from backend.app.services.ai_service import AIService, ai_service

router = APIRouter()


@router.post("/ask", response_model=AskResponse, summary="Ask AI via POST")
def ask_ai_post(request: AskRequest) -> AskResponse:
    """Submit a question to the AI service using a JSON request body."""
    try:
        service = AIService(model_name=request.model) if request.model else ai_service
        answer = service.ask(request.question)
        return AskResponse(
            question=request.question,
            answer=answer,
            model_used=service.model_name,
            status="success",
        )
    except ValueError as ve:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(ve),
        ) from ve
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"AI service error: {exc}",
        ) from exc


@router.get("/ask", response_model=AskResponse, summary="Ask AI via GET")
def ask_ai_get(
    question: str = Query(..., min_length=1, description="Question for the AI"),
    model: str | None = Query(None, description="Optional custom Gemini model"),
) -> AskResponse:
    """Submit a question to the AI service using query parameters (convenient for browser testing)."""
    return ask_ai_post(AskRequest(question=question, model=model))
