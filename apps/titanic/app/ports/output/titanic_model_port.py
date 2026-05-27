from typing import Protocol


class TitanicModelPort(Protocol):
    def has_decision_tree_model(self) -> bool:
        ...

    def get_model_name(self) -> str:
        ...
