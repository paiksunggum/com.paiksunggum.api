from typing import Any, Protocol


class TitanicDataReaderPort(Protocol):
    def get_data(self) -> Any:
        ...

    def get_count(self) -> int:
        ...
