from src.parsers.base_parser import BaseParser


class TextParser(BaseParser):

    def extract_text(
        self,
        file_content: bytes
    ) -> str:

        return file_content.decode(
            "utf-8",
            errors="ignore"
        )