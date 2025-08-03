import os
import shutil
from fastapi import UploadFile
from backend.config.settings import UPLOAD_DIR
from pathlib import Path


def save_file(file: UploadFile, file_path: Path):
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
