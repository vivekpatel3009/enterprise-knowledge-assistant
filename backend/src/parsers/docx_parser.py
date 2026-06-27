from io import BytesIO

from docx import Document

from src.parsers.base_parser import BaseParser


class DocxParser(BaseParser):

    def extract_text(
        self,
        file_content: bytes
    ) -> str:

        document = Document(
            BytesIO(file_content)
        )

        paragraphs = [
            paragraph.text
            for paragraph in document.paragraphs
        ]

        return "\n".join(paragraphs)