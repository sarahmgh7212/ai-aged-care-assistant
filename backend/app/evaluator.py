import json
import os

from openai import OpenAI


EVALUATION_MODEL = "gpt-5-mini"


def evaluate_answer(
    question: str,
    answer: str,
    sources: list,
    answerable: bool = True,
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

    if answerable:

        system_prompt = """
You are evaluating an AI-generated answer for an aged care
information assistant.

The question IS expected to be answerable using the supplied
knowledge-base evidence.

Evaluate the answer ONLY against the supplied evidence.

Do not use your own outside knowledge.

Evaluate four things:

1. grounded
- Are the factual claims supported by the supplied evidence?

2. relevant
- Does the answer directly address the user's question?

3. complete
- Does the answer provide a sufficiently complete response
  based on the available evidence?

4. citations_correct
- Are the citations used correctly?
- Does each citation actually support the claim it is attached to?

Return ONLY valid JSON:

{
  "grounded": true,
  "relevant": true,
  "complete": true,
  "citations_correct": true,
  "reason": "Short explanation"
}
"""

    else:

        system_prompt = """
You are evaluating an AI-generated answer for an aged care
information assistant.

The question is NOT expected to be answerable using the supplied
aged-care knowledge base.

The assistant should therefore avoid hallucinating an answer
or presenting unsupported information as fact.

Evaluate one thing:

1. no_hallucination
- Did the assistant correctly avoid inventing an answer from
  information that is not supported by the supplied evidence?

A response such as:

"I couldn't find relevant information in the available
knowledge base."

is acceptable.

It is also acceptable for the assistant to explain that the
available knowledge base does not contain enough information.

Do NOT mark an answer as incorrect merely because it does not
directly answer the user's original question.

For example, if the user asks about car maintenance, weather,
political voting or medication and the aged-care knowledge base
does not contain that information, refusing to answer from the
knowledge base is correct behavior.

Return ONLY valid JSON:

{
  "no_hallucination": true,
  "reason": "Short explanation"
}
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

        if answerable:

            return {
                "grounded": False,
                "relevant": False,
                "complete": False,
                "citations_correct": False,
                "reason": "Evaluator returned invalid JSON.",
            }

        return {
            "no_hallucination": False,
            "reason": "Evaluator returned invalid JSON.",
        }

