from fastapi import FastAPI
from backend.app.services.ai_service import ask_gemini

app = FastAPI(title="DataMind API")

@app.get("/")

def root():
    return {
        "message": "Welcome to DataMind API"
    }

@app.get("/ask")
def ask(question: str):
    answer = ask_gemini(question)

    return {
        "question": question,
        "answer": answer
    }