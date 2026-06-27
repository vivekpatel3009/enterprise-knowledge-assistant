class ContextBuilder:
    def build(
        self,
        documents: list[str]
    ) -> str:

        context_parts = []

        for index, document in enumerate(documents, start=1):
            context_parts.append(
                f"[Chunk {index}]\n{document}"
            )

        return "\n\n".join(context_parts)