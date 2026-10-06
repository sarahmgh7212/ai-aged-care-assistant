import json
from pathlib import Path

from app.rag import generate_answer, retrieve_context
from app.evaluator import evaluate_answer


PROJECT_ROOT = Path(__file__).resolve().parents[1]

QUESTIONS_FILE = (
    PROJECT_ROOT
    / "knowledge-base"
    / "evaluation"
    / "questions.json"
)

RESULTS_FILE = (
    PROJECT_ROOT
    / "knowledge-base"
    / "evaluation"
    / "results.json"
)


with open(QUESTIONS_FILE, "r", encoding="utf-8") as file:
    questions = json.load(file)


total_questions = len(questions)

answerable_questions = [
    question
    for question in questions
    if question["answerable"]
]

out_of_scope_questions = [
    question
    for question in questions
    if not question["answerable"]
]


retrieval_successes = 0
out_of_scope_rejections = 0

grounded_successes = 0
relevant_successes = 0
complete_successes = 0
citation_successes = 0

no_hallucination_successes = 0


# Store detailed results for each question
question_results = []


print()
print("=" * 60)
print("AI AGED CARE ASSISTANT EVALUATION")
print("=" * 60)
print()


for item in questions:

    question_id = item["id"]
    question = item["question"]
    answerable = item["answerable"]

    print("-" * 60)
    print(f"{question_id}: {question}")
    print("-" * 60)

    sources = retrieve_context(question)
    has_sources = len(sources) > 0

    print(f"Retrieved sources: {len(sources)}")

    # ---------------------------------------------------------
    # Retrieval evaluation
    # ---------------------------------------------------------

    retrieval_success = False
    out_of_scope_rejection_success = False

    if answerable and has_sources:
        retrieval_successes += 1
        retrieval_success = True

    if not answerable and not has_sources:
        out_of_scope_rejections += 1
        out_of_scope_rejection_success = True

    # ---------------------------------------------------------
    # Generate answer
    # ---------------------------------------------------------

    result = generate_answer(question)

    answer = result["answer"]
    answer_sources = result["sources"]

    print()
    print("Answer:")
    print(answer)

    # ---------------------------------------------------------
    # Answer evaluation
    # ---------------------------------------------------------

    evaluation = evaluate_answer(
        question=question,
        answer=answer,
        sources=answer_sources,
        answerable=answerable,
    )

    print()
    print("LLM Evaluation:")

    question_result = {
        "id": question_id,
        "question": question,
        "answerable": answerable,
        "retrieved_source_count": len(sources),
        "retrieval_success": retrieval_success,
        "out_of_scope_rejection_success": (
            out_of_scope_rejection_success
            if not answerable
            else None
        ),
        "answer": answer,
    }

    if answerable:

        grounded = evaluation.get(
            "grounded",
            False,
        )

        relevant = evaluation.get(
            "relevant",
            False,
        )

        complete = evaluation.get(
            "complete",
            False,
        )

        citations_correct = evaluation.get(
            "citations_correct",
            False,
        )

        print(f"Grounded:          {grounded}")
        print(f"Relevant:          {relevant}")
        print(f"Complete:          {complete}")
        print(f"Citations correct: {citations_correct}")

        if grounded:
            grounded_successes += 1

        if relevant:
            relevant_successes += 1

        if complete:
            complete_successes += 1

        if citations_correct:
            citation_successes += 1

        question_result["evaluation"] = {
            "grounded": grounded,
            "relevant": relevant,
            "complete": complete,
            "citations_correct": citations_correct,
            "reason": evaluation.get("reason", ""),
        }

    else:

        no_hallucination = evaluation.get(
            "no_hallucination",
            False,
        )

        print(f"No hallucination:  {no_hallucination}")

        if no_hallucination:
            no_hallucination_successes += 1

        question_result["evaluation"] = {
            "no_hallucination": no_hallucination,
            "reason": evaluation.get("reason", ""),
        }

    print(
        f"Reason:            "
        f"{evaluation.get('reason', '')}"
    )

    question_results.append(question_result)

    print()


def percentage(successes, total):

    if total == 0:
        return 0

    return round(
        (successes / total) * 100,
        1,
    )


# Calculate metrics
# ---------------------------------------------------------

retrieval_accuracy = percentage(
    retrieval_successes,
    len(answerable_questions),
)

out_of_scope_rejection = percentage(
    out_of_scope_rejections,
    len(out_of_scope_questions),
)

grounded_accuracy = percentage(
    grounded_successes,
    len(answerable_questions),
)

relevant_accuracy = percentage(
    relevant_successes,
    len(answerable_questions),
)

complete_accuracy = percentage(
    complete_successes,
    len(answerable_questions),
)

citation_accuracy = percentage(
    citation_successes,
    len(answerable_questions),
)

no_hallucination_accuracy = percentage(
    no_hallucination_successes,
    len(out_of_scope_questions),
)


# Build structured results
# ---------------------------------------------------------

results = {
    "total_questions": total_questions,
    "answerable_questions": len(answerable_questions),
    "out_of_scope_questions": len(out_of_scope_questions),
    "metrics": {
        "retrieval_accuracy": retrieval_accuracy,
        "out_of_scope_rejection": out_of_scope_rejection,
        "grounded_answers": grounded_accuracy,
        "relevant_answers": relevant_accuracy,
        "complete_answers": complete_accuracy,
        "citation_accuracy": citation_accuracy,
        "no_hallucination": no_hallucination_accuracy,
    },
    "questions": question_results,
}


# Save results
# ---------------------------------------------------------

with open(
    RESULTS_FILE,
    "w",
    encoding="utf-8",
) as file:

    json.dump(
        results,
        file,
        indent=2,
        ensure_ascii=False,
    )


# Print summary
# ---------------------------------------------------------

print("=" * 60)
print("EVALUATION SUMMARY")
print("=" * 60)

print(f"Total questions:          {total_questions}")
print(
    f"Answerable questions:     "
    f"{len(answerable_questions)}"
)
print(
    f"Out-of-scope questions:   "
    f"{len(out_of_scope_questions)}"
)

print()

print(
    f"Retrieval accuracy:       "
    f"{retrieval_accuracy}%"
)

print(
    f"Out-of-scope rejection:   "
    f"{out_of_scope_rejection}%"
)

print()

print(
    f"Grounded answers:         "
    f"{grounded_accuracy}%"
)

print(
    f"Relevant answers:         "
    f"{relevant_accuracy}%"
)

print(
    f"Complete answers:         "
    f"{complete_accuracy}%"
)

print(
    f"Citation accuracy:        "
    f"{citation_accuracy}%"
)

print()

print(
    f"No hallucination:         "
    f"{no_hallucination_accuracy}%"
)

print()

print(f"Results saved to: {RESULTS_FILE}")

print("=" * 60)
print()

