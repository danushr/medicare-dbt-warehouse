import os
from pathlib import Path

PROJECT_DIR = Path(os.environ["MEDICARE_PROJECT_DIR"])
DATA_DIR = Path(os.environ["MEDICARE_DATA_DIR"])
RAW_DIR = DATA_DIR / "raw"
DB = DATA_DIR / "warehouse.duckdb"
SAMPLE_DIR = PROJECT_DIR / "sample"
DAGS_DIR = PROJECT_DIR / "dags"
