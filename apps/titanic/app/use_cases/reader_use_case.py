import pandas as pd


class WalterReader:
    def __init__(self) -> None:
        pass

    def get_data(self):
        raise RuntimeError("프로젝트 내부 파일(CSV)을 읽는 기능은 제거되었습니다.")

    def get_count(self):
        raise RuntimeError("프로젝트 내부 파일(CSV)을 읽는 기능은 제거되었습니다.")

    def get_dataframe(self) -> pd.DataFrame:
        """학습·검증용 전체 Titanic 데이터프레임."""
        raise RuntimeError("프로젝트 내부 파일(CSV)을 읽는 기능은 제거되었습니다.")
