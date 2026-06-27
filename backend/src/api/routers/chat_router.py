from fastapi import APIRouter

from src.models.chat_request import ChatRequest
from src.models.chat_response import (
    ChatResponse,
    Citation
)
from src.services.knowledge_assistant_service import (
    KnowledgeAssistantService
)

router = APIRouter()

assistant = KnowledgeAssistantService()


@router.post(
    "/query",
    response_model=ChatResponse
)
async def query(
    request: ChatRequest
):
    answer, metadata, confidence  = assistant.ask(
        request.question,
        request.top_k
    )

    sources = [
        Citation(
            document_id=item["document_id"],
            document_name=item["document_name"],
            chunk_index=item["chunk_index"]
        )
        for item in metadata
    ]

    return ChatResponse(
        answer=answer,
        confidence=confidence,
        sources=sources,
    )