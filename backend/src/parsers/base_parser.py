from abc import ABC
from abc import abstractmethod


class BaseParser(ABC):

    @abstractmethod
    def extract_text(
        self,
        file_content: bytes
    ) -> str:
        pass