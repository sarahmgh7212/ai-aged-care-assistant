import os

from dotenv import load_dotenv
from fastapi import FastAPI
from openai import OpenAI
from pydantic import BaseModel
from app.rag import generate_answer
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()

app = FastAPI(
    title="AI Aged Care Information Assistant",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

client = OpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1",
)


@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "service": "AI Aged Care Information Assistant",
    }

class ChatRequest(BaseModel):
    question: str


@app.post("/api/chat")
def chat(request: ChatRequest):
    if not request.question.strip():
        return {
            "answer": "Please enter a question.",
            "sources": [],
        }

    return generate_answer(request.question)


@app.get("/ai-test")
def ai_test():
    response = client.responses.create(
        model="openai/gpt-4o-mini",
        input="Explain what aged care means in one short sentence.",
    )

    return {
        "response": response.output_text
    }