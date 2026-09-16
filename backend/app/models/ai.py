from typing import List, Optional
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


class DatasetAskRequest(BaseModel):
    """Request model for asking questions about a specific dataset."""

    question: str = Field(..., min_length=1, description="Question about the dataset")
    model: Optional[str] = Field(None, description="Optional custom Gemini model override")


class DatasetAskResponse(BaseModel):
    """Response model for dataset-aware AI questions."""

    dataset_id: str = Field(..., description="Unique dataset identifier")
    question: str = Field(..., description="The original question asked")
    answer: str = Field(..., description="AI generated answer grounded in dataset context/tools")
    tools_used: List[str] = Field(
        default_factory=list,
        description="List of LangChain tools invoked by the agent to answer the question",
    )
    model_used: str = Field(..., description="Gemini model used for this request")
    status: str = Field(default="success", description="Status of the request execution")
