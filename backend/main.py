from fastapi import FastAPI

app = FastAPI(
    title="AI Aged Care Information Assistant",
    version="0.1.0",
)


@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "service": "AI Aged Care Information Assistant",
    }
