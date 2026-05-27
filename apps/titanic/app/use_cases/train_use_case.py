from ..models.rose_model import RoseModel

from .walter_reader import WalterReader


class JackService:
    def __init__(self) -> None:
        self.walter = WalterReader()
        self.rose = RoseModel()

    def get_data(self):
        return self.walter.get_data()

    def get_count(self):
        return self.walter.get_count()

    def has_decision_tree_model(self):
        return self.rose.has_decision_tree_model()

    def get_model_name_and_accuracy(self):
        return {"model": self.rose.get_model_name()}
