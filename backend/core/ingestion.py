import logging
from pathlib import Path
from langchain_core.documents import Document
from backend.services.ingestion.pdf_ingestor import PDFIngestor
from backend.services.ingestion.video_ingestor import VideoIngestor
from backend.services.embedding.chroma_manager import ChromaManager

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def ingest_file(file_path: str, file_ext: str):
    """
    Unified ingestion pipeline for PDF and MP4 files.
    """
    file_path = Path(file_path)

    if file_ext.lower() == "pdf":
        _run_pdf_pipeline(file_path)
    elif file_ext.lower() == "mp4":
        _run_video_pipeline(file_path)
    else:
        raise ValueError(f"Unsupported file type: {file_ext}")


def _run_pdf_pipeline(pdf_path: Path):
    try:
        with PDFIngestor(str(pdf_path)) as ingestor:
            chunks = ingestor.chunk_text()
            logger.info(f"Extracted {len(chunks)} chunks from {pdf_path}")
            documents = [
                Document(
                    page_content=chunk,
                    metadata={
                        "source": str(pdf_path),
                        "filename": pdf_path.name,  # Add filename
                        "chunk_id": idx,
                    },
                )
                for idx, chunk in enumerate(chunks)
            ]
            _store_in_chroma(documents, prefix="pdf")
            logger.info(f"Ingested PDF: {pdf_path}")
    except Exception as e:
        logger.error(f"Failed PDF ingestion ({pdf_path}): {e}")
        raise


def _run_video_pipeline(video_path: Path):
    try:
        with VideoIngestor(str(video_path)) as ingestor:
            result = ingestor.ingest()
            segments = result.get("transcript", [])

            documents = [
                Document(
                    page_content=segment["text"],
                    metadata={"source": str(video_path), "segment_id": idx, **segment},
                )
                for idx, segment in enumerate(segments)
            ]

            _store_in_chroma(documents, prefix="video")
            logger.info(f"Ingested video: {video_path}")
    except Exception as e:
        logger.error(f"Failed video ingestion ({video_path}): {e}")
        raise


def _store_in_chroma(documents: list[Document], prefix: str):
    chroma = ChromaManager()

    texts = [doc.page_content for doc in documents]
    metadatas = [doc.metadata for doc in documents]
    ids = [f"{prefix}_{i}" for i in range(len(documents))]

    chroma.add_documents(texts=texts, metadatas=metadatas, ids=ids)
