from pydantic import BaseModel, Field


class HealthResponse(BaseModel):
    """Response model for system health check."""

    status: str = Field(default="ok", description="Overall health status")
    app_name: str = Field(..., description="Name of the application")
    version: str = Field(..., description="Current application version")
    llm_configured: bool = Field(..., description="Whether Gemini API key is configured")
