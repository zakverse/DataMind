import os
from pathlib import Path
from dotenv import load_dotenv
from pydantic import BaseModel, Field

# Root directory of the DataMind project
BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent
ENV_PATH = BASE_DIR / ".env"

# Load environment variables from .env
load_dotenv(dotenv_path=ENV_PATH)


class Settings(BaseModel):
    """Application settings and environment configurations."""

    PROJECT_NAME: str = "DataMind API"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    DEBUG: bool = False

    # Gemini LLM Settings
    GEMINI_API_KEY: str = Field(default_factory=lambda: os.getenv("GEMINI_API_KEY", ""))
    GEMINI_MODEL: str = Field(default_factory=lambda: os.getenv("GEMINI_MODEL", "gemini-3.6-flash"))

    # Upload & Data Settings
    MAX_FILE_SIZE_MB: int = 50
    DATA_DIR: Path = BASE_DIR / "data"
    UPLOAD_DIR: Path = BASE_DIR / "data" / "uploads"
    PROCESSED_DIR: Path = BASE_DIR / "data" / "processed"


settings = Settings()

# Ensure data directories exist
settings.DATA_DIR.mkdir(parents=True, exist_ok=True)
settings.UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
settings.PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
