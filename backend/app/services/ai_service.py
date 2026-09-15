import os

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY belum ditemukan di .env")

llm = ChatGoogleGenerativeAI(
    model="gemini-3.6-flash",
    google_api_key=api_key,
    temperature=0,
)


def ask_gemini(question: str) -> str:
    response = llm.invoke(question)

    if isinstance(response.content, str):
        return response.content

    return "".join(
        block["text"]
        for block in response.content
        if isinstance(block, dict) and block.get("type") == "text"
    )