from abc import ABC, abstractmethod


class AbstractRetriever(ABC):
    def retrieve(
            self, device: str, data_from: str, data_to: str, attributes: list | None = None, raw: bool = True
    ) -> dict:
        raw_data = self._retrieve_raw(device, data_from, data_to, attributes)

        return raw_data if raw else self._format(raw_data)

    @abstractmethod
    def _retrieve_raw(self, device: str, data_from: str, data_to: str, attributes: tuple | None = None):
        raise NotImplementedError

    @abstractmethod
    def _format(self, raw_data) -> list[dict]:
        raise NotImplementedError
