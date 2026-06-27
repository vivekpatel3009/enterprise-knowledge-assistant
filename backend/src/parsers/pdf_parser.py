from io import BytesIO

from pypdf import PdfReader

from src.parsers.base_parser import BaseParser


class PdfParser(BaseParser):

    def extract_text(
        self,
        file_content: bytes
    ) -> str:

        reader = PdfReader(
            BytesIO(file_content)
        )

        pages = []

        for page in reader.pages:
            pages.append(
                page.extract_text() or ""
            )

        return "\n".join(pages)