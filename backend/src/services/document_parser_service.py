from pathlib import Path

from src.parsers.parser_factory import ParserFactory


class DocumentParserService:

    def parse(
        self,
        file_name: str,
        content: bytes
    ) -> str:

        extension = Path(
            file_name
        ).suffix

        parser = ParserFactory.get_parser(
            extension
        )

        return parser.extract_text(
            content
        )