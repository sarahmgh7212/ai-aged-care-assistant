import json
from pathlib import Path

from app.rag import retrieve_context


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATASET_PATH = (
    PROJECT_ROOT / "knowledge-base" / "evaluation" / "questions.json"
)


def main():
    with open(DATASET_PATH, "r", encoding="utf-8") as file:
        questions = json.load(file)

    total = len(questions)
    answerable_count = 0
    answerable_retrieved = 0
    out_of_scope_count = 0
    out_of_scope_rejected = 0

    for item in questions:
        results = retrieve_context(item["question"])
        retrieved = len(results) > 0

        print(f"\n{item['id']}: {item['question']}")
        print(f"Expected answerable: {item['answerable']}")
        print(f"Retrieved relevant chunks: {retrieved}")

        if item["answerable"]:
            answerable_count += 1

            if retrieved:
                answerable_retrieved += 1

        else:
            out_of_scope_count += 1

            if not retrieved:
                out_of_scope_rejected += 1

        for source in results:
            print(
                f"  - {source['source']}, "
                f"page {source['page']}, "
                f"distance {source['distance']:.3f}"
            )

    print("\n--- Evaluation summary ---")

    if answerable_count:
        recall = answerable_retrieved / answerable_count
        print(f"Answerable questions retrieved: {recall:.1%}")

    if out_of_scope_count:
        rejection_rate = out_of_scope_rejected / out_of_scope_count
        print(f"Out-of-scope questions rejected: {rejection_rate:.1%}")

    print(f"Total questions tested: {total}")


if __name__ == "__main__":
    main()