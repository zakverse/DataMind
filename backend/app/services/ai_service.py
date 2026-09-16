import logging
from typing import Any, List, Optional, Tuple
from langchain_google_genai import ChatGoogleGenerativeAI
from backend.app.agents.analyst_agent import DatasetAnalystAgent, dataset_analyst_agent
from backend.app.core.config import settings

logger = logging.getLogger(__name__)


class AIService:
    """Service for interacting with Google Gemini models via LangChain for general and dataset Q&A."""

    def __init__(self, model_name: Optional[str] = None):
        self.api_key = settings.GEMINI_API_KEY
        if not self.api_key:
            raise ValueError(
                "GEMINI_API_KEY belum dikonfigurasi di environment atau file .env"
            )

        self.model_name = model_name or settings.GEMINI_MODEL
        self._llm: Optional[ChatGoogleGenerativeAI] = None

    @property
    def llm(self) -> ChatGoogleGenerativeAI:
        """Lazy initialization of the LangChain ChatGoogleGenerativeAI instance."""
        if self._llm is None:
            self._llm = ChatGoogleGenerativeAI(
                model=self.model_name,
                google_api_key=self.api_key,
            )
        return self._llm

    def _extract_text_content(self, content: Any) -> str:
        """Helper to reliably extract string text from LangChain message content."""
        if isinstance(content, str):
            return content

        if isinstance(content, list):
            extracted_parts = []
            for block in content:
                if isinstance(block, str):
                    extracted_parts.append(block)
                elif isinstance(block, dict) and block.get("type") == "text":
                    extracted_parts.append(block.get("text", ""))
                elif hasattr(block, "text"):
                    extracted_parts.append(block.text)
            return "".join(extracted_parts)

        return str(content)

    def ask(self, question: str) -> str:
        """Sends a natural language question to Gemini and returns the extracted text response."""
        if not question or not question.strip():
            raise ValueError("Pertanyaan tidak boleh kosong.")

        try:
            response = self.llm.invoke(question)
            return self._extract_text_content(response.content)
        except Exception as exc:
            logger.error(f"Error invoking Gemini model ({self.model_name}): {exc}")
            raise RuntimeError(f"Gagal memproses pertanyaan dengan AI: {exc}") from exc

    def ask_dataset(
        self, dataset_id: str, question: str
    ) -> Tuple[str, List[str], str]:
        """Answers user question about a specific dataset using the Dataset Analyst Agent and LangChain tool calling.

        Returns (answer_text, tools_used, model_name).
        """
        agent = (
            DatasetAnalystAgent(model_name=self.model_name)
            if self.model_name != settings.GEMINI_MODEL
            else dataset_analyst_agent
        )
        return agent.run(dataset_id=dataset_id, question=question)


# Global service instance for default usage
ai_service = AIService()


def ask_gemini(question: str) -> str:
    """Convenience wrapper for backward compatibility."""
    return ai_service.ask(question)


def ask_gemini_dataset(dataset_id: str, question: str) -> str:
    """Convenience wrapper for dataset-aware AI questions."""
    answer, _, _ = ai_service.ask_dataset(dataset_id, question)
    return answer