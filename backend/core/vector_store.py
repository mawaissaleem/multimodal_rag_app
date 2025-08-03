# app/core/vector_store.py

from chromadb import PersistentClient
from functools import lru_cache
from backend.config.settings import settings


@lru_cache
def get_chroma_collection():
    client = PersistentClient(path="backend/db")
    return client.get_collection(name=settings.CHROMA_COLLECTION)
