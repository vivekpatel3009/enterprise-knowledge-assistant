import uuid

from langchain_text_splitters import (
    RecursiveCharacterTextSplitter
)

from src.models.document_chunk import DocumentChunk


class DocumentChunkingService:

    def __init__(self):
        self.text_splitter = (
            RecursiveCharacterTextSplitter(
                chunk_size=1000,
                chunk_overlap=200,
                length_function=len,
                is_separator_regex=False
            )
        )

    def chunk_document(
        self,
        document_id: str,
        document_name: str,
        text: str
    ) -> list[DocumentChunk]:

        chunks = self.text_splitter.split_text(text)

        return [
            DocumentChunk(
                chunk_id=str(uuid.uuid4()),
                document_id=document_id,
                document_name=document_name,
                chunk_index=index,
                content=chunk
            )
            for index, chunk in enumerate(chunks)
        ]