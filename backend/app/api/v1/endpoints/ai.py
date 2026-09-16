from fastapi import APIRouter, HTTPException, Query, status
from backend.app.models.ai import (
    AskRequest,
    AskResponse,
    DatasetAskRequest,
    DatasetAskResponse,
)
from backend.app.services.ai_service import AIService, ai_service

router = APIRouter()


@router.post("/ask", response_model=AskResponse, summary="Ask AI (General Q&A) via POST")
def ask_ai_post(request: AskRequest) -> AskResponse:
    """Submit a general question to the AI service using a JSON request body."""
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


@router.get("/ask", response_model=AskResponse, summary="Ask AI (General Q&A) via GET")
def ask_ai_get(
    question: str = Query(..., min_length=1, description="Question for the AI"),
    model: str | None = Query(None, description="Optional custom Gemini model"),
) -> AskResponse:
    """Submit a general question to the AI service using query parameters."""
    return ask_ai_post(AskRequest(question=question, model=model))


@router.post(
    "/datasets/{dataset_id}/ask",
    response_model=DatasetAskResponse,
    summary="Ask AI about a specific dataset (Agent with Tool Calling)",
)
def ask_dataset_post(
    dataset_id: str,
    request: DatasetAskRequest,
) -> DatasetAskResponse:
    """Submit a natural language question about an uploaded dataset.

    The Dataset Analyst Agent determines and invokes the necessary LangChain tools (statistics, missing values, profiling, correlation) to provide grounded answers.
    """
    try:
        service = AIService(model_name=request.model) if request.model else ai_service
        answer, tools_used, model_used = service.ask_dataset(
            dataset_id=dataset_id, question=request.question
        )
        return DatasetAskResponse(
            dataset_id=dataset_id,
            question=request.question,
            answer=answer,
            tools_used=tools_used,
            model_used=model_used,
            status="success",
        )
    except FileNotFoundError as fnf:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(fnf),
        ) from fnf
    except ValueError as ve:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(ve),
        ) from ve
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Gagal memproses pertanyaan dataset: {exc}",
        ) from exc
