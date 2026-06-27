from pathlib import Path
import chromadb
import os

class ChromaRepository:

    def __init__(self):

        base_dir = Path(__file__).resolve().parents[3]

        default_chroma_path = (
            base_dir / "data" / "chroma"
        )

        chroma_path = Path(
            os.getenv(
                "CHROMA_DB_PATH",
                str(default_chroma_path)
            )
        )

        self.client = chromadb.PersistentClient(
            path=str(chroma_path)
        )

        self.collection = (
            self.client.get_or_create_collection(
                name="documents"
            )
        )

    def add_chunk(
        self,
        chunk_id: str,
        content: str,
        embedding: list[float],
        metadata: dict
    ) -> None:

        self.collection.add(
            ids=[chunk_id],
            documents=[content],
            embeddings=[embedding],
            metadatas=[metadata]
        )

    def document_exists_by_hash(
        self,
        file_hash: str
    ) -> bool:

        result = self.collection.get(
            where={
                "file_hash": file_hash
            }
        )

        ids = result.get("ids", [])
        return bool(ids)

    def get_vector_count(self) -> int:
        return self.collection.count()
    
    def search(
        self,
        embedding: list[float],
        top_k: int = 5
    ) -> dict:
        try:
            return self.collection.query(
                query_embeddings=[embedding],
                n_results=top_k
            )
        except Exception as ex:
            raise RuntimeError(
                f"Failed to search ChromaDB: {str(ex)}"
            ) from ex
        
    def get_documents(self):

        result = self.collection.get()

        documents = {}

        for metadata in result["metadatas"]:

            document_id = metadata["document_id"]
            document_name = metadata["document_name"]

            if document_id not in documents:
                documents[document_id] = {
                    "document_id": document_id,
                    "document_name": document_name
                }

        return list(documents.values())