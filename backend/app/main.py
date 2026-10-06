import os
from pathlib import Path
import json
from fastapi import FastAPI, HTTPException
from dotenv import load_dotenv
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

class ChatMessage(BaseModel):
    role: str
    content: str


class ChatRequest(BaseModel):
    question: str
    messages: list[ChatMessage] = []


@app.post("/api/chat")
def chat(request: ChatRequest):
    result = generate_answer(
        request.question,
        request.messages,
    )

    return result

@app.get("/api/evaluation")
def get_evaluation():
    project_root = Path(__file__).resolve().parents[2]
    results_file = (
        project_root
        / "knowledge-base"
        / "evaluation"
        / "results.json"
    )

    if not results_file.exists():
        raise HTTPException(
            status_code=404,
            detail="Evaluation results file not found."
        )

    try:
        with open(results_file, "r", encoding="utf-8") as file:
            results = json.load(file)

        return results

    except json.JSONDecodeError:
        raise HTTPException(
            status_code=500,
            detail="Evaluation results file contains invalid JSON."
        )
    
@app.get("/ai-test")
def ai_test():
    response = client.responses.create(
        model="openai/gpt-4o-mini",
        input="Explain what aged care means in one short sentence.",
    )

    return {
        "response": response.output_text
    }