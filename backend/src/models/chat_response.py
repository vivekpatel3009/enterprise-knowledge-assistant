from pydantic import BaseModel


class Citation(BaseModel):
    document_id: str
    document_name: str
    chunk_index: int


class ChatResponse(BaseModel):
    answer: str
    confidence: float
    sources: list[Citation]