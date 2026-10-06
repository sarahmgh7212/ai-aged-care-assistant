from app.rag import retrieve_context, check_answerability


questions = [
    "What can I do if I am unhappy with the care I receive?",
    "What legal action can I take against my aged care provider?",
]


for question in questions:

    print("=" * 60)
    print(f"QUESTION: {question}")
    print("=" * 60)

    sources = retrieve_context(question)

    print(f"Retrieved sources: {len(sources)}")

    answerable = check_answerability(
        question,
        sources,
    )

    print(f"Answerable: {answerable}")
    print()

