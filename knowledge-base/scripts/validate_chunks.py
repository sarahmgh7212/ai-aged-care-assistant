
import json
from pathlib import Path


# To ensure that:

# 1.Chunks were generated.

# 2.IDs are unique.

# 3.There are no empty chunks.

# 4.The text is readable.

# 5.Page numbers look reasonable.

processed_dir = (
    Path(__file__).resolve().parents[1] / "processed"
)

for path in processed_dir.glob("*.jsonl"):
    records = [
        json.loads(line)
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]

    print(f"\nFile: {path.name}")
    print(f"Total chunks: {len(records)}")

    if not records:
        print("WARNING: No chunks found.")
        continue

    print("First chunk:")
    print(json.dumps(records[0], indent=2, ensure_ascii=False))

    ids = [record["chunk_id"] for record in records]
    print(f"Unique IDs: {len(set(ids)) == len(ids)}")

    empty_chunks = [
        record for record in records
        if not record["text"].strip()
    ]
    print(f"Empty chunks: {len(empty_chunks)}")