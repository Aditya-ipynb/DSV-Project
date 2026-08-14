import pandas as pd
from pathlib import Path

from json_loader import JsonLoader

loader = JsonLoader()
data = loader.data

print(data.head())
