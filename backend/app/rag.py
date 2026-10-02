from pathlib import Path
import os

import chromadb
from dotenv import load_dotenv
from openai import OpenAI


PROJECT_ROOT = Path(__file__).resolve().parents[2]
VECTOR_DIR = PROJECT_ROOT / "knowledge-base" / "vector_store"

load_dotenv(PROJECT_ROOT / "backend" / ".env")

client = OpenAI(
        api_key=os.getenv("OPENROUTER_API_KEY"),
        base_url="https://openrouter.ai/api/v1",
    )


chroma_client = chromadb.PersistentClient(
    path=str(VECTOR_DIR)
)

collection = chroma_client.get_collection(
    name="aged_care_knowledge"
)


EMBEDDING_MODEL = "text-embedding-3-small"
CHAT_MODEL = "gpt-5-mini"


def retrieve_context(
    question: str,
    top_k: int = 5,
    max_distance: float = 0.6,
):
    """
    Retrieve the most relevant knowledge-base chunks
    for a user's question.
    """

    question_embedding = client.embeddings.create(
        model=EMBEDDING_MODEL,
        input=question
    ).data[0].embedding

    results = collection.query(
        query_embeddings=[question_embedding],
        n_results=min(top_k, collection.count()),
        include=[
            "documents",
            "metadatas",
            "distances",
        ],
    )

    documents = results["documents"][0]
    metadatas = results["metadatas"][0]
    distances = results["distances"][0]
    filtered_sources = []

    for index, document in enumerate(documents):
        distance = distances[index]

        if distance <= max_distance:
            metadata = metadatas[index]

            filtered_sources.append({
                "id": f"S{len(filtered_sources) + 1}",
                "text": document,
                "source": metadata["source"],
                "page": metadata["page"],
                "distance": distance,
            })

    return filtered_sources

   
def generate_answer(question: str):
    """
    Retrieve relevant information and generate
    an answer grounded in the retrieved sources.
    """

    sources = retrieve_context(question)

    if not sources:
        return {
            "answer": (
                "I couldn't find relevant information in the "
                "available aged care knowledge base."
            ),
            "sources": [],
        }

    evidence = []

    for source in sources:
        evidence.append(
            f"""
[{source['id']}]
Source: {source['source']}
Page: {source['page']}

{source['text']}
"""
        )

    evidence_text = "\n".join(evidence)

    system_prompt = """
You are an aged care information assistant.

Your job is to answer questions using ONLY the information
provided in the knowledge-base sources.

Rules:

1. Do not invent facts.
2. Do not use information that is not contained in the sources.
3. If the sources do not contain enough information to answer
   the question, clearly say that there is not enough information
   in the available knowledge base.
4. Cite the sources you use using [S1], [S2], etc.
5. Do not create citations that were not provided.
6. Use clear, respectful and easy-to-understand language.
7. Do not present yourself as the official Aged Care Quality
   and Safety Commission.
8. Do not provide personalised medical or legal advice.
9. When appropriate, explain what the person can do next based
   on the information in the sources.

The answer should be concise but useful.
"""

    user_prompt = f"""
Question:

{question}

Knowledge-base sources:

{evidence_text}
"""

    response = client.responses.create(
        model=CHAT_MODEL,
        instructions=system_prompt,
        input=user_prompt,
    )

    return {
        "answer": response.output_text,
        "sources": [
            {
                "id": source["id"],
                "text": source["text"],
                "source": source["source"],
                "page": source["page"],
            }
            for source in sources
        ],
    }