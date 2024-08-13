from abc import ABC, abstractmethod


class AbstractRetriever(ABC):
    @abstractmethod
    def retrieve(
            self, device: str, data_from: str, data_to: str, attributes: tuple | None = None, raw: bool = True
    ) -> dict:
        raise NotImplementedError
