from pathlib import Path

from fastapi import HTTPException
from fastapi import UploadFile


class FileValidator:
    ALLOWED_EXTENSIONS = {
        ".pdf",
        ".docx",
        ".txt"
    }

    MAX_FILE_SIZE_MB = 20
    MAX_FILE_SIZE_BYTES = MAX_FILE_SIZE_MB * 1024 * 1024

    @classmethod
    async def validate(cls, file: UploadFile) -> None:
        if not file.filename:
            raise HTTPException(
                status_code=400,
                detail="File name is required."
            )

        extension = Path(file.filename).suffix.lower()

        if extension not in cls.ALLOWED_EXTENSIONS:
            raise HTTPException(
                status_code=400,
                detail=(
                    f"Unsupported file type '{extension}'. "
                    f"Allowed types: {', '.join(cls.ALLOWED_EXTENSIONS)}"
                )
            )

        content = await file.read()

        if len(content) == 0:
            raise HTTPException(
                status_code=400,
                detail="Uploaded file is empty."
            )

        if len(content) > cls.MAX_FILE_SIZE_BYTES:
            raise HTTPException(
                status_code=400,
                detail=(
                    f"File size exceeds "
                    f"{cls.MAX_FILE_SIZE_MB} MB limit."
                )
            )

        await file.seek(0)