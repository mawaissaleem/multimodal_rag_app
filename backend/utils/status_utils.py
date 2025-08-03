import json
from backend.config.settings import STATUS_FILE
import os


def init_status_file():
    os.makedirs(STATUS_FILE.parent, exist_ok=True)
    if not STATUS_FILE.exists():
        with open(STATUS_FILE, "w") as f:
            json.dump({}, f)


def update_status(filename: str, status: str):
    with open(STATUS_FILE, "r+") as f:
        status_data = json.load(f)
        status_data[filename] = status
        f.seek(0)
        json.dump(status_data, f, indent=2)
        f.truncate()
