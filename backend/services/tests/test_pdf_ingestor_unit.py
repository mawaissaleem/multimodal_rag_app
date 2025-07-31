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
