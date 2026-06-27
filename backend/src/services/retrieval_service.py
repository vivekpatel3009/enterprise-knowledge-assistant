from src.repositories.chroma_repository import ChromaRepository
from src.services.embedding_service import EmbeddingService


class RetrievalService:
    def __init__(self):
        self.embedding_service = EmbeddingService()
        self.chroma_repository = ChromaRepository()

    def retrieve(
        self,
        question: str,
        top_k: int = 5
    ) -> dict:

        query_embedding = (
            self.embedding_service.generate_embedding(
                question
            )
        )

        results = self.chroma_repository.search(
            embedding=query_embedding,
            top_k=top_k
        )

        return results