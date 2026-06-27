from src.services.retrieval_service import RetrievalService
from src.services.context_builder import ContextBuilder
from src.services.chat_completion_service import ChatCompletionService


class KnowledgeAssistantService:
    SIMILARITY_THRESHOLD = 1.2

    def __init__(self):
        self.retrieval_service = RetrievalService()
        self.context_builder = ContextBuilder()
        self.chat_service = ChatCompletionService()

    def ask(
        self,
        question: str,
        top_k: int = 5
    ):
        results = self.retrieval_service.retrieve(
            question,
            top_k
        )

        if not results["documents"] or not results["documents"][0]:
            return (
                "The requested information is not available in the knowledge base.",
                [],
                0.0
            )

        documents = results["documents"][0]
        metadatas = results["metadatas"][0]
        distances = results["distances"][0]
        best_distance = min(distances)
        confidence = max(
            0.0,
            min(
                1.0,
                1.2 - (best_distance / 2)
            )
        )

        print(distances)

        filtered_documents = []
        filtered_metadatas = []

        for document, metadata, distance in zip(
            documents,
            metadatas,
            distances
        ):
            print(
                f"{metadata['document_name']} "
                f"Distance={distance}"
            )

            if distance <= self.SIMILARITY_THRESHOLD:
                filtered_documents.append(document)
                filtered_metadatas.append(metadata)

        if not filtered_documents:
            return (
                "The requested information is not available in the knowledge base.",
                [],
                0.0
            )

        context = self.context_builder.build(
            filtered_documents
        )

        answer = self.chat_service.generate_answer(
            question,
            context
        )

        return answer, filtered_metadatas, round(confidence, 2)