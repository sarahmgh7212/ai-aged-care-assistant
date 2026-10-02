
import os
from pathlib import Path

import chromadb
from dotenv import load_dotenv
from openai import OpenAI


PROJECT_ROOT = Path(__file__).resolve().parents[2]
VECTOR_DIR = PROJECT_ROOT / "knowledge-base" / "vector_store"

COLLECTION_NAME = "aged_care_knowledge"
EMBEDDING_MODEL = "text-embedding-3-small"


def main():
    load_dotenv(PROJECT_ROOT / "backend" / ".env")

    if not os.getenv("OPENROUTER_API_KEY"):
        raise RuntimeError(
            "OPENROUTER_API_KEY is missing from backend/.env"
        )

    openai_client = OpenAI(
        api_key=os.getenv("OPENROUTER_API_KEY"),
        base_url="https://openrouter.ai/api/v1",
    )

    db = chromadb.PersistentClient(path=str(VECTOR_DIR))

    collection = db.get_collection(
        name=COLLECTION_NAME
    )

    question = input("Ask an aged care question: ").strip()

    if not question:
        print("Please enter a question.")
        return

    response = openai_client.embeddings.create(
        model=EMBEDDING_MODEL,
        input=[question],
    )

    query_embedding = response.data[0].embedding

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=min(5, collection.count()),
        include=["documents", "metadatas", "distances"],
    )

    documents = results["documents"][0]
    metadatas = results["metadatas"][0]
    distances = results["distances"][0]

    print("\nRelevant passages:\n")

    for index, (text, metadata, distance) in enumerate(
        zip(documents, metadatas, distances),
        start=1,
    ):
        print(f"--- Result {index} ---")
        print(f"Source: {metadata.get('source')}")
        print(f"Page: {metadata.get('page')}")
        print(f"Distance: {distance:.4f}")
        print(f"Text:\n{text}\n")


if __name__ == "__main__":
    main()