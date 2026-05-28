from fastapi import FastAPI

from doro.app.dorow import Dorow


app = FastAPI(title="한국도로공사_교통사고통계")


class Doroj:
    def __init__(self):
        pass


    def get_data(self):
        dw = Dorow()
        return dw.get_data()