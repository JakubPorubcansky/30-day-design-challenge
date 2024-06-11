import pandas as pd
from app import process_data

class Model:
    def __init__(self):
        self.data: pd.DataFrame = None
        self.processed_data: pd.DataFrame = None

    def load_data(self, file_path: str):
        self.data = pd.read_csv(file_path)

    def process_data(self, option: str):
        self.processed_data = process_data(self.data, option)