from src.parsers.pdf_parser import PdfParser
from src.parsers.docx_parser import DocxParser
from src.parsers.text_parser import TextParser


class ParserFactory:

    @staticmethod
    def get_parser(
        extension: str
    ):
        extension = extension.lower()

        parsers = {
            ".pdf": PdfParser(),
            ".docx": DocxParser(),
            ".txt": TextParser()
        }

        parser = parsers.get(extension)

        if parser is None:
            raise ValueError(
                f"No parser found for {extension}"
            )

        return parser