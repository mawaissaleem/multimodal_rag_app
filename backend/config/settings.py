# backend/config/settings.py
from pathlib import Path
from pydantic_settings import BaseSettings  # ✅ Corrected import

class Settings(BaseSettings):
    EMBEDDING_MODEL: str = "all-MiniLM-L6-v2"
    CHROMA_COLLECTION: str = "your_collection_name"

    class Config:
        env_file = ".env"

settings = Settings()

# Still define file paths (optional)
UPLOAD_DIR = Path("data/uploads")
STATUS_FILE = Path("status_store/status.json")

