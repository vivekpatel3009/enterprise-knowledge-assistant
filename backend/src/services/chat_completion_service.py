from openai import AzureOpenAI

from src.config.settings import settings


class ChatCompletionService:
    def __init__(self):
        self.client = AzureOpenAI(
            api_key=settings.azure_openai_api_key.get_secret_value(),
            api_version=settings.azure_openai_api_version,
            azure_endpoint=settings.azure_openai_endpoint
        )

    def generate_answer(
        self,
        question: str,
        context: str
    ) -> str:
    
     try:
        response = self.client.chat.completions.create(
            model=settings.azure_openai_deployment_name, temperature=0,
            messages=[
                {
                    "role": "system",
                    "content": """
You are an Enterprise Knowledge Assistant.

Rules:
1. Answer only from the provided context.
2. Do not make assumptions.
3. Do not use outside knowledge.
4. If the answer is not present in the context, respond exactly:
   'The requested information is not available in the knowledge base.'
5. Do not mention chunk numbers.
6. Do not generate citations or references unless explicitly provided in the context.
7. Keep answers concise and factual.
"""
                },
                {
                    "role": "user",
                    "content": f"""
Context:
{context}

Question:
{question}
"""
                }
            ]
        )

        return response.choices[0].message.content or ""

     except Exception as ex:
        raise RuntimeError(
            f"Failed to generate answer: {str(ex)}"
        ) from ex