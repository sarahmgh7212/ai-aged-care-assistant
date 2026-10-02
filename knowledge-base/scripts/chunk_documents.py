
import json
import re
from pathlib import Path

from pypdf import PdfReader


PROJECT_ROOT = Path(__file__).resolve().parents[2]
RAW_DIR = PROJECT_ROOT / "knowledge-base" / "raw"
OUTPUT_DIR = PROJECT_ROOT / "knowledge-base" / "processed"

CHUNK_SIZE = 1200
CHUNK_OVERLAP = 200


def clean_text(text: str) -> str:
    """Clean extracted PDF text without removing paragraph boundaries."""
    text = text.replace("\x00", "")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def split_into_paragraphs(text: str) -> list[str]:
    """Split text into non-empty paragraphs."""
    return [
        paragraph.strip()
        for paragraph in re.split(r"\n\s*\n", text)
        if paragraph.strip()
    ]


def split_long_paragraph(
    paragraph: str,
    max_size: int,
) -> list[str]:
    """Split oversized paragraphs at sentence boundaries when possible."""
    sentences = re.split(r"(?<=[.!?])\s+", paragraph)

    pieces = []
    current = ""

    for sentence in sentences:
        if len(sentence) > max_size:
            if current:
                pieces.append(current)
                current = ""

            # Fallback for a single very long sentence.
            for start in range(0, len(sentence), max_size):
                pieces.append(sentence[start:start + max_size])

        elif not current:
            current = sentence

        elif len(current) + len(sentence) + 1 <= max_size:
            current += " " + sentence

        else:
            pieces.append(current)
            current = sentence

    if current:
        pieces.append(current)

    return pieces


def chunk_page_text(
    text: str,
    chunk_size: int = CHUNK_SIZE,
    overlap: int = CHUNK_OVERLAP,
) -> list[str]:
    """Create paragraph-aware chunks with character overlap."""
    paragraphs = split_into_paragraphs(text)

    chunks = []
    current = ""

    for paragraph in paragraphs:
        if len(paragraph) > chunk_size:
            if current:
                chunks.append(current)
                current = ""

            chunks.extend(
                split_long_paragraph(paragraph, chunk_size)
            )
            continue

        candidate = (
            f"{current}\n\n{paragraph}" if current else paragraph
        )

        if len(candidate) <= chunk_size:
            current = candidate
        else:
            if current:
                chunks.append(current)

            # Keep trailing context from the previous chunk.
            prefix = current[-overlap:] if current else ""
            current = f"{prefix}\n\n{paragraph}".strip()

            # If overlap makes the chunk too large, start cleanly.
            if len(current) > chunk_size:
                current = paragraph

    if current:
        chunks.append(current)

    return chunks


def process_pdf(pdf_path: Path) -> list[dict]:
    """Extract each PDF page and create source-aware chunks."""
    reader = PdfReader(pdf_path)
    records = []

    for page_number, page in enumerate(reader.pages, start=1):
        extracted = page.extract_text() or ""
        cleaned = clean_text(extracted)

        if not cleaned:
            continue

        page_chunks = chunk_page_text(cleaned)

        for chunk_index, chunk in enumerate(page_chunks, start=1):
            records.append({
                "chunk_id": (
                    f"{pdf_path.stem}-p{page_number}-c{chunk_index}"
                ),
                "text": chunk,
                "metadata": {
                    "source": pdf_path.name,
                    "document_title": pdf_path.stem.replace("-", " "),
                    "page": page_number,
                    "chunk_index": chunk_index,
                },
            })

    return records


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    pdf_files = sorted(RAW_DIR.glob("*.pdf"))

    if not pdf_files:
        print(f"No PDFs found in {RAW_DIR}")
        return

    for pdf_path in pdf_files:
        print(f"Processing: {pdf_path.name}")

        records = process_pdf(pdf_path)

        output_path = OUTPUT_DIR / f"{pdf_path.stem}.jsonl"

        with output_path.open("w", encoding="utf-8") as file:
            for record in records:
                file.write(json.dumps(record, ensure_ascii=False) + "\n")

        print(f"Chunks created: {len(records)}")
        print(f"Saved to: {output_path}")


if __name__ == "__main__":
    main()