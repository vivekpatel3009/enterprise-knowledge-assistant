from pydantic import BaseModel


class DocumentChunk(BaseModel):
    chunk_id: str
    document_id: str
    document_name: str
    chunk_index: int
    content: str