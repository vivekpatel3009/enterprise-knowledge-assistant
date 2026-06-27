import uuid
import hashlib
from fastapi import APIRouter, File, UploadFile

from src.services.storage_service import StorageService
from src.services.document_parser_service import DocumentParserService
from src.utils.file_validator import FileValidator
from src.services.document_chunking_service import DocumentChunkingService
from src.services.chunk_storage_service import ChunkStorageService
from src.services.embedding_service import EmbeddingService
from src.repositories.chroma_repository import ChromaRepository
from src.models.search_request import SearchRequest

router = APIRouter()

embedding_service = EmbeddingService()
storage_service = StorageService()
parser_service = DocumentParserService()
chroma_repository = ChromaRepository()
chunking_service = DocumentChunkingService()
chunk_storage_service = ChunkStorageService()


@router.post("/upload")
async def upload_document(
    file: UploadFile = File(...)
):
    await FileValidator.validate(file)

    document_id = str(uuid.uuid4())

    content = await file.read()
    file_hash = hashlib.sha256(content).hexdigest()
    exists = chroma_repository.document_exists_by_hash(
        file_hash
    )


    if exists:
        return {
            "message": "Document already exists."
        }

    file_name = (
        f"{document_id}_{file.filename}"
    )


    blob_url = await storage_service.upload_file(
        file_name=file_name,
        file_content=content
    )

    text = parser_service.parse(
        file_name=file.filename,
        content=content
    )

    chunks = chunking_service.chunk_document(
        document_id=document_id,
        document_name=file.filename,
        text=text
    )

    for chunk in chunks:
        embedding = embedding_service.generate_embedding(
            text=chunk.content
        )

        chroma_repository.add_chunk(
            chunk_id=chunk.chunk_id,
            content=chunk.content,
            embedding=embedding,
            metadata={
                "document_id": chunk.document_id,
                "document_name": chunk.document_name,
                "chunk_index": chunk.chunk_index,
                "file_hash": file_hash
            }
        )
    
    chunk_file = ( 
        chunk_storage_service.save_chunks( 
            document_id=document_id, chunks=chunks ) 
            )

    return {
        "message": "Document uploaded successfully.",
        "documentId": document_id,
        "fileName": file.filename,
        "contentType": file.content_type,
        "fileSize": len(content),
        "blobUrl": blob_url,
        "status": "Uploaded",
        "chunkCount": len(chunks),
        "chunkFile": chunk_file,
        "firstChunk": (
            chunks[0].content[:500]
            if chunks
            else ""
        )
    }


@router.get("")
async def get_documents():

    documents = (
        chroma_repository.get_documents()
    )

    return {
        "documents": documents
    }