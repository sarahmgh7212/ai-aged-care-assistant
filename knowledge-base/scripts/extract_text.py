from pathlib import Path

from pypdf import PdfReader


RAW_DIR = Path(__file__).resolve().parent.parent / "raw"
PROCESSED_DIR = Path(__file__).resolve().parent.parent / "processed"


def extract_pdf(pdf_path: Path) -> str:
    reader = PdfReader(pdf_path)

    pages = []

    for page in reader.pages:
        text = page.extract_text()

        if text:
            pages.append(text)

    return "\n\n".join(pages)


def main():
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

    pdf_files = list(RAW_DIR.glob("*.pdf"))

    if not pdf_files:
        print("No PDF documents found.")
        return

    for pdf_path in pdf_files:
        print(f"Processing: {pdf_path.name}")

        text = extract_pdf(pdf_path)

        output_path = PROCESSED_DIR / f"{pdf_path.stem}.txt"

        output_path.write_text(
            text,
            encoding="utf-8",
        )

        print(f"Saved: {output_path}")
        print(f"Characters extracted: {len(text)}")


if __name__ == "__main__":
    main()