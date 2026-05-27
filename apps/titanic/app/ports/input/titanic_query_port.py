from typing import Any, Protocol


class TitanicQueryPort(Protocol):
    def get_data(self) -> Any:
        ...

    def get_count(self) -> int:
        ...

    def has_decision_tree_model(self) -> bool:
        ...

    def get_model_name_and_accuracy(self) -> dict[str, str]:
        ...
