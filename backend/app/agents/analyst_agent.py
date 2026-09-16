import logging
from typing import Any, List, Optional, Tuple
from langchain.agents import create_agent
from langchain_core.language_models import BaseChatModel
from langchain_google_genai import ChatGoogleGenerativeAI

from backend.app.core.config import settings
from backend.app.services.dataset_service import dataset_service
from backend.app.tools.dataset_tools import ALL_DATASET_TOOLS

logger = logging.getLogger(__name__)

DATASET_ANALYST_AGENT_SYSTEM_PROMPT = """You are DataMind, an expert AI Data Analyst Agent.
You are tasked with analyzing and answering questions about a specific dataset with ID: `{dataset_id}`.

CRITICAL INSTRUCTIONS & CONSTRAINTS:
1. TOOL CALLING REQUIRED: Whenever answering questions about the dataset, ALWAYS invoke the relevant tool(s) passing `dataset_id="{dataset_id}"`.
   - `dataset_profile_tool`: For overall dataset structure, filename, rows, columns, and column types.
   - `missing_values_tool`: For missing/null values, missing percentages, and affected columns.
   - `numeric_statistics_tool`: For statistical summaries (mean, std, min, median, max, percentiles) of numeric columns.
   - `categorical_summary_tool`: For categorical distributions, unique values, and top frequencies.
   - `correlation_tool`: For Pearson correlation matrices between numeric features.
2. ZERO NUMERIC HALLUCINATION: NEVER make up, assume, or estimate numbers, column names, or statistics that were not explicitly returned by the tools.
3. GROUNDED ANSWERS: Formulate your answer based strictly on the structured tool outputs.
4. MISSING INFORMATION: If a requested column or piece of data is not found in the dataset, clearly state that it is not available.
5. PRESENTATION: Present your findings in a structured, professional manner with markdown formatting (bullet points, bold key values).
6. LANGUAGE: Always respond in the same language as the user's question (e.g., Indonesian or English).
"""


def extract_content_text(content: Any) -> str:
    """Extracts plain text string from various LangChain message content formats."""
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        parts = []
        for block in content:
            if isinstance(block, str):
                parts.append(block)
            elif isinstance(block, dict) and block.get("type") == "text":
                parts.append(block.get("text", ""))
            elif hasattr(block, "text"):
                parts.append(block.text)
        return "".join(parts)
    return str(content)


class DatasetAnalystAgent:
    """Agent orchestrator for dataset analysis and tool-calling reasoning."""

    def __init__(self, model_name: Optional[str] = None):
        self.api_key = settings.GEMINI_API_KEY
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY belum dikonfigurasi di environment atau file .env")

        self.model_name = model_name or settings.GEMINI_MODEL
        self._llm: Optional[ChatGoogleGenerativeAI] = None

    @property
    def llm(self) -> ChatGoogleGenerativeAI:
        """Lazy initialization of the Gemini chat model."""
        if self._llm is None:
            self._llm = ChatGoogleGenerativeAI(
                model=self.model_name,
                google_api_key=self.api_key,
            )
        return self._llm

    def run(self, dataset_id: str, question: str) -> Tuple[str, List[str], str]:
        """Runs the Dataset Analyst Agent on a dataset question using tool calling.

        Returns (answer_text, tools_used, model_name).
        """
        if not question or not question.strip():
            raise ValueError("Pertanyaan tidak boleh kosong.")

        if not dataset_id or not dataset_id.strip():
            raise ValueError("Dataset ID tidak boleh kosong.")

        # Ensure dataset exists before running agent
        dataset_service.get_dataset_profile(dataset_id)

        # Prepare system prompt for this specific dataset
        system_prompt = DATASET_ANALYST_AGENT_SYSTEM_PROMPT.format(dataset_id=dataset_id)

        # Create modern LangChain agent graph
        agent = create_agent(
            model=self.llm,
            tools=ALL_DATASET_TOOLS,
            system_prompt=system_prompt,
        )

        user_message = f"User Question regarding dataset '{dataset_id}': {question.strip()}"

        try:
            result = agent.invoke({"messages": [{"role": "user", "content": user_message}]})
        except Exception as exc:
            logger.error(f"Error executing DatasetAnalystAgent for dataset {dataset_id}: {exc}")
            raise RuntimeError(f"Gagal mengeksekusi agent analisis data: {exc}") from exc

        # Extract tools called during reasoning
        tools_used: List[str] = []
        messages = result.get("messages", [])
        for msg in messages:
            # Check tool calls on AIMessage
            if hasattr(msg, "tool_calls") and msg.tool_calls:
                for tc in msg.tool_calls:
                    name = tc.get("name") if isinstance(tc, dict) else getattr(tc, "name", None)
                    if name and name not in tools_used:
                        tools_used.append(name)
            # Check ToolMessage name
            elif getattr(msg, "name", None) and msg.name not in tools_used:
                tools_used.append(msg.name)

        # Extract final answer
        if messages:
            last_message = messages[-1]
            answer_text = extract_content_text(last_message.content)
        else:
            answer_text = "Tidak ada jawaban yang dihasilkan oleh agent."

        return answer_text, tools_used, self.model_name


# Global agent instance
dataset_analyst_agent = DatasetAnalystAgent()


def run_dataset_analyst_agent(dataset_id: str, question: str) -> Tuple[str, List[str], str]:
    """Convenience function to run the global Dataset Analyst Agent."""
    return dataset_analyst_agent.run(dataset_id, question)
