import json
from openai import OpenAI
import os
from dotenv import load_dotenv



EVALUATION_MODEL = "gpt-5-mini"


def evaluate_answer(
    question: str,
    answer: str,
    sources: list,
):
    client = OpenAI(
           api_key=os.getenv("OPENROUTER_API_KEY"),
           base_url="https://openrouter.ai/api/v1",
       )

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
You are evaluating an AI-generated answer for an aged care
information assistant.

Evaluate the answer ONLY against the supplied evidence.

Do not use your own outside knowledge.

Evaluate four things:

1. grounded
   Is the answer supported by the supplied evidence?

2. relevant
   Does the answer directly address the user's question?

3. complete
   Does the answer include the important information needed
   to answer the question based on the available evidence?

4. citations_correct
   Does the answer use citations such as [S1] correctly,
   where the cited source actually supports the statement?

Return ONLY valid JSON in this format:

{
  "grounded": true,
  "relevant": true,
  "complete": true,
  "citations_correct": true,
  "reason": "Short explanation"
}

Use boolean values for the four evaluation fields.
"""

    user_prompt = f"""
Question:

{question}

Generated answer:

{answer}

Available evidence:

{evidence_text}
"""

    response = client.responses.create(
        model=EVALUATION_MODEL,
        instructions=system_prompt,
        input=user_prompt,
    )

    try:
        return json.loads(response.output_text)
    except json.JSONDecodeError:
        return {
            "grounded": False,
            "relevant": False,
            "complete": False,
            "citations_correct": False,
            "reason": "Evaluator returned invalid JSON.",
        }