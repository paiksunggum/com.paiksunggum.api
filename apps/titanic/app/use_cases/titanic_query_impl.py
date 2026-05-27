from typing import Any

from ..ports.output.titanic_data_reader_port import TitanicDataReaderPort
from ..ports.output.titanic_model_port import TitanicModelPort


class TitanicQueryImpl:
    def __init__(
        self,
        data_reader: TitanicDataReaderPort,
        model: TitanicModelPort,
    ) -> None:
        self._data_reader = data_reader
        self._model = model

    def get_data(self) -> Any:
        return self._data_reader.get_data()

    def get_count(self) -> int:
        return self._data_reader.get_count()

    def has_decision_tree_model(self) -> bool:
        return self._model.has_decision_tree_model()

    def get_model_name_and_accuracy(self) -> dict[str, str]:
        return {"model": self._model.get_model_name()}
