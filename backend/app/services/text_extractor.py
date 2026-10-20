from pypdf import PdfReader
from docx import Document


def extract_text(file_path: str):

    if file_path.endswith(".pdf"):
        reader = PdfReader(file_path)
        text = ""
        for page in reader.pages:
            text += page.extract_text() or ""
        return text

    elif file_path.endswith(".docx"):
        doc = Document(file_path)
        return "\n".join(
            p.text for p in doc.paragraphs
        )

    elif file_path.endswith(".txt"):
        with open(file_path, "r") as f:
            return f.read()

    return ""