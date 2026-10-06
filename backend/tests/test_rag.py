import app.rag as rag


def test_retrieve_context_filters_by_distance(monkeypatch):
    class MockCollection:
        def query(self, **kwargs):
            return {
                "documents": [[
                    "Relevant aged care information.",
                    "Another relevant passage.",
                    "Irrelevant information.",
                ]],
                "metadatas": [[
                    {
                        "source": "aged-care-quality-standards.pdf",
                        "page": 10,
                    },
                    {
                        "source": "aged-care-quality-standards.pdf",
                        "page": 18,
                    },
                    {
                        "source": "aged-care-quality-standards.pdf",
                        "page": 50,
                    },
                ]],
                "distances": [[
                    0.30,
                    0.50,
                    0.80,
                ]],
            }

    monkeypatch.setattr(rag, "collection", MockCollection())

    class MockEmbedding:
      embedding = [0.1, 0.2, 0.3]


    class MockEmbeddingResponse:
      data = [MockEmbedding()]

    def mock_embeddings_create(**kwargs):
        return MockEmbeddingResponse()

    monkeypatch.setattr(
        rag.client.embeddings,
        "create",
        mock_embeddings_create,
    )

    results = rag.retrieve_context(
        "What rights do older people have?",
        top_k=5,
        max_distance=0.6,
    )

    assert len(results) == 2

    assert results[0]["text"] == "Relevant aged care information."
    assert results[1]["text"] == "Another relevant passage."

    assert results[0]["page"] == 10
    assert results[1]["page"] == 18

def test_check_answerability_returns_true(monkeypatch):
    class MockResponse:
        output_text = '{"answerable": true}'

    def mock_responses_create(**kwargs):
        return MockResponse()

    monkeypatch.setattr(
        rag.client.responses,
        "create",
        mock_responses_create,
    )

    sources = [
        {
            "id": "S1",
            "source": "aged-care-quality-standards.pdf",
            "page": 10,
            "text": "Older people have rights and choices.",
        }
    ]

    result = rag.check_answerability(
        "What rights do older people have?",
        sources,
    )

    assert result is True

def test_check_answerability_returns_false(monkeypatch):
    class MockResponse:
        output_text = '{"answerable": false}'

    def mock_responses_create(**kwargs):
        return MockResponse()

    monkeypatch.setattr(
        rag.client.responses,
        "create",
        mock_responses_create,
    )

    sources = [
        {
            "id": "S1",
            "source": "aged-care-quality-standards.pdf",
            "page": 18,
            "text": "Complaints and feedback should be managed appropriately.",
        }
    ]

    result = rag.check_answerability(
        "What legal action can I take against my provider?",
        sources,
    )

    assert result is False