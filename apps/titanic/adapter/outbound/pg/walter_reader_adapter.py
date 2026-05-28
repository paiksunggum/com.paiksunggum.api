from ....app.use_cases.reader_use_case import WalterReader


class WalterReaderAdapter:
    def __init__(self) -> None:
        self._reader = WalterReader()

    def get_data(self):
        return self._reader.get_data()

    def get_count(self) -> int:
        return self._reader.get_count()
