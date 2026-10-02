
import json
import os
from pathlib import Path

import chromadb
from dotenv import load_dotenv
from openai import OpenAI


PROJECT_ROOT = Path(__file__).resolve().parents[2]
PROCESSED_DIR = PROJECT_ROOT / "knowledge-base" / "processed"
VECTOR_DIR = PROJECT_ROOT / "knowledge-base" / "vector_store"

EMBEDDING_MODEL = "text-embedding-3-small"
COLLECTION_NAME = "aged_care_knowledge"
BATCH_SIZE = 64


def load_chunks():
    """Load chunk records from all processed JSONL files."""
    records = []

    for path in sorted(PROCESSED_DIR.glob("*.jsonl")):
        with path.open(encoding="utf-8") as file:
            for line in file:
                if line.strip():
                    records.append(json.loads(line))

    return records


def main():
    load_dotenv(PROJECT_ROOT / "backend" / ".env")

    if not os.getenv("OPENROUTER_API_KEY"):
        raise RuntimeError(
            "OPENROUTER_API_KEY is missing from backend/.env"
        )

    chunks = load_chunks()

    if not chunks:
        raise RuntimeError(
            f"No JSONL chunks found in {PROCESSED_DIR}"
        )

    client = OpenAI(
        api_key=os.getenv("OPENROUTER_API_KEY"),
        base_url="https://openrouter.ai/api/v1",
    )

    VECTOR_DIR.mkdir(parents=True, exist_ok=True)

    db = chromadb.PersistentClient(path=str(VECTOR_DIR))

    collection = db.get_or_create_collection(
        name=COLLECTION_NAME,
        metadata={"hnsw:space": "cosine"},
    )

    print(f"Loaded {len(chunks)} chunks.")

    for start in range(0, len(chunks), BATCH_SIZE):
        batch = chunks[start:start + BATCH_SIZE]

        texts = [record["text"] for record in batch]
        ids = [record["chunk_id"] for record in batch]

        metadatas = [
            record["metadata"] for record in batch
        ]

        response = client.embeddings.create(
            model=EMBEDDING_MODEL,
            input=texts,
        )

        embeddings = [
            item.embedding for item in response.data
        ]

        collection.upsert(
            ids=ids,
            documents=texts,
            metadatas=metadatas,
            embeddings=embeddings,
        )

        print(
            f"Indexed {min(start + len(batch), len(chunks))}"
            f" / {len(chunks)} chunks"
        )

    print(f"Total indexed records: {collection.count()}")
    print(f"Vector database saved to: {VECTOR_DIR}")


if __name__ == "__main__":
    main()