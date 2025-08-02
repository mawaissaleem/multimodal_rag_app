import os
import pytest
from backend.services.ingestion.pdf_ingestor import PDFIngestor

TEST_PDF_PATH = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../../../data/raw/file01.pdf")
)


@pytest.fixture
def pdf_ingestor():
    with PDFIngestor(TEST_PDF_PATH) as ingestor:
        yield ingestor


def test_metadata_extraction(pdf_ingestor):
    metadata = pdf_ingestor.extract_metadata()
    assert isinstance(metadata, dict)
    assert "title" in metadata or "producer" in metadata  # Typical metadata fields


def test_text_extraction(pdf_ingestor):
    pages = pdf_ingestor.extract_text()
    assert isinstance(pages, list)
    assert len(pages) > 0
    assert "text" in pages[0]


def test_chunking(pdf_ingestor):
    chunks = pdf_ingestor.chunk_text(chunk_size=500, chunk_overlap=50)
    assert isinstance(chunks, list)
    assert len(chunks) > 0

    for i, chunk in enumerate(chunks):
        assert isinstance(chunk, str)
        assert len(chunk) <= 500  # Max length
        if i > 0:
            # Check some overlap (not precise, but helps ensure behavior)
            overlap = len(set(chunks[i]) & set(chunks[i - 1]))
            assert overlap > 0
