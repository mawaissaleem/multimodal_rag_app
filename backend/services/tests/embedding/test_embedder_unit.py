from backend.services.embedding.embedder import Embedder
import numpy as np


def test_embedder_single_input():
    embedder = Embedder()
    emb = embedder.encode("Test sentence.")
    assert isinstance(emb, np.ndarray)
    assert emb.shape == (1, 384)


def test_embedder_multiple_input():
    embedder = Embedder()
    emb = embedder.encode(["Sentence 1", "Sentence 2"])
    assert emb.shape == (2, 384)
