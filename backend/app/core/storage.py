from pathlib import Path
from pathlib import PureWindowsPath


BACKEND_DIR = Path(__file__).resolve().parents[2]
UPLOAD_DIR = BACKEND_DIR / "uploads"


def resolve_document_path(file_path: str) -> Path:
    path = Path(file_path)
    if path.exists():
        return path

    windows_parts = PureWindowsPath(file_path).parts
    upload_index = next(
        (
            index
            for index, part in enumerate(windows_parts)
            if part.lower() == "uploads"
        ),
        None,
    )
    if upload_index is not None:
        return UPLOAD_DIR.joinpath(*windows_parts[upload_index + 1 :])

    if not path.is_absolute():
        return BACKEND_DIR / path
    return path
