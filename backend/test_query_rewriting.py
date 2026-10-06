from app.rag import rewrite_query


conversation = [
    {
        "role": "user",
        "content": "What rights do older people have when receiving aged care?",
    },
    {
        "role": "assistant",
        "content": (
            "Older people have rights relating to dignity, respect, "
            "choice and other aspects of their care."
        ),
    },
]


questions = [
    "What about their choices?",
    "Can you explain that in simpler terms?",
    "What can I do if those rights aren't respected?",
]


for question in questions:

    rewritten = rewrite_query(
        question,
        conversation,
    )

    print("=" * 60)
    print(f"Original:  {question}")
    print(f"Rewritten: {rewritten}")
    print()

