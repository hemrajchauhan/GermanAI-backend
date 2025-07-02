import json
from pathlib import Path

DWDS_VOCAB = {}

for level in ["A1", "A2", "B1"]:
    path = Path(f"app/data/{level}.json")
    with open(path, "r", encoding="utf-8") as f:
        DWDS_VOCAB[level] = json.load(f)