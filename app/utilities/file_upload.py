from pathlib import Path
from uuid import uuid4

from fastapi import HTTPException, UploadFile

UPLOAD_DIR = Path("uploads/resumes")
ALLOWED_EXTENSIONS = {".pdf", ".doc", ".docx"}
MAX_FILE_SIZE = 5 * 1024 * 1024


async def save_resume(file: UploadFile) -> str:
    extension = Path(file.filename).suffix.lower()

    if extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400, detail="Only PDF and Word files are allowed"
        )

    content = await file.read(MAX_FILE_SIZE + 1)

    if len(content) > MAX_FILE_SIZE:
        raise HTTPException(status_code=400, detail="Resume size must be below 5 MB")

    UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

    filename = f"{uuid4()}.{extension}"
    file_path = UPLOAD_DIR / filename

    file_path.write_bytes(content)

    await file.seek(0)

    return str(file_path)
