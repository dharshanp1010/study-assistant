from pathlib import Path
from pypdf import PdfReader

# Project's notes directory
NOTES_DIR = (
    Path(__file__).resolve().parent.parent
    / "data"
    / "notes"
)


def read_note(relative_path: str) -> str:
    """
    Read a TXT or Markdown study note.

    """

    file_path = (NOTES_DIR / relative_path).resolve()

    # Prevent access to files outside the notes directory
    if not file_path.is_relative_to(NOTES_DIR.resolve()):
        raise ValueError("Invalid note path.")

    # Check whether the file exists
    if not file_path.exists():
        raise FileNotFoundError(
            f"Note not found: {relative_path}"
        )

    # Support only TXT and Markdown files
    if file_path.suffix.lower() not in [".txt", ".md"]:
        raise ValueError("Only TXT and Markdown files are supported.")

    # Read and return file contents
    return file_path.read_text(encoding="utf-8")


def read_pdf_note(relative_path: str) -> str:
    """
    Extract text from a PDF study note.

    """

    file_path = (NOTES_DIR / relative_path).resolve()

    if not file_path.is_relative_to(NOTES_DIR.resolve()):
        raise ValueError("Invalid note path.")

    if not file_path.exists():
        raise FileNotFoundError(
            f"PDF note not found: {relative_path}"
        )

    if file_path.suffix.lower() != ".pdf":
        raise ValueError("Only PDF files are supported.")

    reader = PdfReader(str(file_path))

    extracted_pages = []

    for page_number, page in enumerate(reader.pages, start=1):
        page_text = page.extract_text()

        if page_text and page_text.strip():
            extracted_pages.append(
                f"\n--- Page {page_number} ---\n{page_text}"
            )

    if not extracted_pages:
        raise ValueError(
            "No extractable text found in this PDF. "
            "It may be scanned or image-based."
        )

    return "\n".join(extracted_pages)