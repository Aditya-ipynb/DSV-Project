import pandas as pd
import matplotlib as plt
from pathlib import Path

import json


CURRENT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = CURRENT_DIR.parent

INPUT_JSON = (
    PROJECT_ROOT
    / "image_organization"
    / "pokemon_cleaned_images.json"
)


class JsonLoader:
    def __init__(self, input_json: Path = INPUT_JSON):
        self.input_json = input_json
        self.data = self.load_data()

    def load_data(self) -> pd.DataFrame:
        """
        Loads the JSON data into a pandas DataFrame.
        """
        with open(self.input_json, "r", encoding="utf-8") as f:
            data = json.load(f)
        return pd.DataFrame(data)


loader = JsonLoader()
loaded_data = loader.data
print(loaded_data.head())