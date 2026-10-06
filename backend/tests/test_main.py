from fastapi.testclient import TestClient

import app.main as main


client = TestClient(main.app)


def test_health_endpoint():
    response = client.get("/health")

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "ok"
    assert data["service"] == "AI Aged Care Information Assistant"


def test_chat_endpoint(monkeypatch):
    def mock_generate_answer(question, messages):
        return {
            "answer": "Older people have rights when receiving aged care.",
            "sources": [
                {
                    "id": "S1",
                    "source": "aged-care-quality-standards.pdf",
                    "page": 10,
                    "text": "Older people have rights when receiving aged care.",
                }
            ],
        }

    monkeypatch.setattr(
        main,
        "generate_answer",
        mock_generate_answer,
    )

    response = client.post(
        "/api/chat",
        json={
            "question": "What rights do older people have?",
            "messages": [],
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert "answer" in data
    assert "sources" in data

    assert data["answer"] == (
        "Older people have rights when receiving aged care."
    )

    assert len(data["sources"]) == 1
    assert data["sources"][0]["id"] == "S1"


def test_chat_endpoint_accepts_conversation_history(monkeypatch):
    def mock_generate_answer(question, messages):
        assert question == "What about their choices?"
        assert len(messages) == 2
        assert messages[0].role == "user"
        assert messages[1].role == "assistant"

        return {
            "answer": "Older people should have choices about their care.",
            "sources": [],
        }

    monkeypatch.setattr(
        main,
        "generate_answer",
        mock_generate_answer,
    )

    response = client.post(
        "/api/chat",
        json={
            "question": "What about their choices?",
            "messages": [
                {
                    "role": "user",
                    "content": "What rights do older people have?",
                },
                {
                    "role": "assistant",
                    "content": "Older people have rights when receiving care.",
                },
            ],
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["answer"] == (
        "Older people should have choices about their care."
    )