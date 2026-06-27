import json
from pathlib import Path

from src.models.document_chunk import DocumentChunk


class ChunkStorageService:
    def __init__(self):
        self.base_path = (
            Path(__file__).resolve().parents[3]
            / "data"
            / "chunks"
        )
        self.base_path.mkdir(
            parents=True,
            exist_ok=True
        )

    def save_chunks(
        self,
        document_id: str,
        chunks: list[DocumentChunk]
    ) -> str:
        file_path = self.base_path / f"{document_id}.json"
        payload = [
            chunk.model_dump()
            for chunk in chunks
        ]
        with open(
            file_path,
            "w",
            encoding="utf-8"
        ) as file:
            json.dump(
                payload,
                file,
                indent=4,
                ensure_ascii=False
            )

        return str(file_path)