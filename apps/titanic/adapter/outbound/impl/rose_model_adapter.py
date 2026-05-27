from ....app.models.rose_model import RoseModel


class RoseModelAdapter:
    def __init__(self) -> None:
        self._model = RoseModel()

    def has_decision_tree_model(self) -> bool:
        return self._model.has_decision_tree_model()

    def get_model_name(self) -> str:
        return self._model.get_model_name()
