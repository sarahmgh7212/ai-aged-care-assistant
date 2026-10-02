import json
from pathlib import Path

from app.rag import generate_answer
from app.evaluator import evaluate_answer


PROJECT_ROOT = Path(__file__).resolve().parents[1]

DATASET_PATH = (
    PROJECT_ROOT
    / "knowledge-base"
    / "evaluation"
    / "questions.json"
)


def main():
    with open(DATASET_PATH, "r", encoding="utf-8") as file:
        questions = json.load(file)

    total = len(questions)
    answerable_questions = 0
    answers_with_sources = 0
    keyword_matches = 0
    unsupported_questions_rejected = 0

    for item in questions:
        question = item["question"]

        print("\n" + "=" * 70)
        print(f"{item['id']}: {question}")

        result = generate_answer(question)
        evaluation = evaluate_answer(
        question=question,
        answer=result["answer"],
        sources=result["sources"],
      )

        answer = result["answer"]
        sources = result["sources"]

        print("\nAnswer:")
        print(answer)
        print("\nLLM Evaluation:")

        print(
            f"Grounded: "
            f"{evaluation['grounded']}"
        )

        print(
            f"Relevant: "
            f"{evaluation['relevant']}"
        )

        print(
            f"Complete: "
            f"{evaluation['complete']}"
        )

        print(
            f"Citations correct: "
            f"{evaluation['citations_correct']}"
        )

        print(
            f"Reason: "
            f"{evaluation['reason']}"
        )

        print("\nSources:")

        for source in sources:
            print(
                f"- [{source['id']}] "
                f"{source['source']} "
                f"(page {source['page']})"
            )

        if item["answerable"]:
            answerable_questions += 1

            if sources:
                answers_with_sources += 1

            answer_lower = answer.lower()

            matched_keywords = [
                keyword
                for keyword in item["expected_keywords"]
                if keyword.lower() in answer_lower
            ]

            print(
                f"\nKeyword matches: "
                f"{matched_keywords}"
            )

            if matched_keywords:
                keyword_matches += 1

        else:
            if not sources:
                unsupported_questions_rejected += 1

    print("\n" + "=" * 70)
    print("EVALUATION SUMMARY")
    print("=" * 70)

    if answerable_questions:
        retrieval_rate = (
            answers_with_sources / answerable_questions
        )

        keyword_rate = (
            keyword_matches / answerable_questions
        )

        print(
            f"Answerable questions with sources: "
            f"{retrieval_rate:.1%}"
        )

        print(
            f"Answerable questions with keyword matches: "
            f"{keyword_rate:.1%}"
        )

    unsupported_rate = (
        unsupported_questions_rejected
        / (total - answerable_questions)
    )

    print(
        f"Unsupported questions rejected: "
        f"{unsupported_rate:.1%}"
    )


if __name__ == "__main__":
    main()