# backend/services/embedder.py

from typing import List, Union
from sentence_transformers import SentenceTransformer
import numpy as np
import logging

logger = logging.getLogger(__name__)


class Embedder:
    def __init__(self, model_name: str = "BAAI/bge-small-en"):
        """
        Initializes the embedding model.
        """
        try:
            self.model = SentenceTransformer(model_name)
            logger.info(f"Loaded embedding model: {model_name}")
        except Exception as e:
            logger.exception("Failed to load embedding model.")
            raise RuntimeError("Could not load embedding model.") from e

    def encode(self, texts: Union[str, List[str]]) -> np.ndarray:
        """
        Accepts a single string or list of strings and returns embeddings as NumPy array.
        """
        if isinstance(texts, str):
            texts = [texts]
        elif not isinstance(texts, list):
            raise TypeError("Input must be a string or list of strings.")

        if not texts:
            raise ValueError("Input list of texts is empty.")

        return self.model.encode(
            texts,
            show_progress_bar=False,
            convert_to_numpy=True,
            normalize_embeddings=True,  # Optional but recommended for similarity
        )
