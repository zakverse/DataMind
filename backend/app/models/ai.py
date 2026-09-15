from typing import Optional
from pydantic import BaseModel, Field


class AskRequest(BaseModel):
    """Request model for asking questions to Gemini."""

    question: str = Field(..., min_length=1, description="Question or prompt for the AI")
    model: Optional[str] = Field(None, description="Optional custom Gemini model override")


class AskResponse(BaseModel):
    """Response model for AI questions."""

    question: str = Field(..., description="The original question asked")
    answer: str = Field(..., description="AI generated answer")
    model_used: str = Field(..., description="Gemini model used for this request")
    status: str = Field(default="success", description="Status of the request execution")
