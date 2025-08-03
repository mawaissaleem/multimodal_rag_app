# app/core/embedding.py

from sentence_transformers import SentenceTransformer
from functools import lru_cache
from backend.config.settings import settings


@lru_cache
def get_embedding_model():
    return SentenceTransformer(settings.EMBEDDING_MODEL)
