import sys
import os
import logging

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../..")))

from backend.services.ingestion.pdf_ingestor import PDFIngestor
from backend.services.ingestion.video_ingestor import VideoIngestor
from backend.services.embedding.chroma_manager import ChromaManager
from langchain_core.documents import Document

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def run_pdf_pipeline(pdf_path):
    try:
        with PDFIngestor(pdf_path) as ingestor:
            # Extract text chunks using chunk_text method
            text_chunks = ingestor.chunk_text()
            # Create Document objects for compatibility with ChromaManager
            documents = [
                Document(
                    page_content=text, metadata={"source": pdf_path, "chunk_id": i}
                )
                for i, text in enumerate(text_chunks)
            ]
            texts = [doc.page_content for doc in documents]
            metadatas = [doc.metadata for doc in documents]
            ids = [f"pdf_{i}" for i in range(len(documents))]

            chroma = ChromaManager()
            chroma.add_documents(texts, metadatas, ids)
            logger.info(f"Processed PDF: {pdf_path}")
    except Exception as e:
        logger.error(f"Error processing PDF {pdf_path}: {e}")
        raise


def run_video_pipeline(video_path):
    try:
        with VideoIngestor(video_path) as ingestor:
            # Get dictionary with transcript segments
            result = ingestor.ingest()
            segments = result["transcript"]
            # Log video segment text for debugging
            logger.info(f"Video segments: {[seg['text'] for seg in segments]}")
            # Convert segments to Document objects, using 'text' field for page_content
            documents = [
                Document(
                    page_content=seg["text"],
                    metadata={"source": video_path, "segment_id": i, **seg},
                )
                for i, seg in enumerate(segments)
            ]
            texts = [doc.page_content for doc in documents]
            metadatas = [doc.metadata for doc in documents]
            ids = [f"video_{i}" for i in range(len(documents))]

            chroma = ChromaManager()
            chroma.add_documents(texts, metadatas, ids)
            logger.info(f"Processed video: {video_path}")
    except Exception as e:
        logger.error(f"Error processing video {video_path}: {e}")
        raise


if __name__ == "__main__":
    # Use absolute paths to ensure files are found
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../.."))
    pdf_path = os.path.join(base_dir, "data", "uploads", "Evaluation Task.pdf")
    video_path = os.path.join(base_dir, "data", "raw", "video01.mp4")

    run_pdf_pipeline(pdf_path)
    run_video_pipeline(video_path)

    chroma = ChromaManager()
    # Query for PDF content
    pdf_query = "evaluation criteria?"
    pdf_result = chroma.query(query_text=pdf_query, n_results=50)
    if pdf_result and pdf_result["documents"]:
        filtered_pdf_result = {
            "ids": [],
            "documents": [],
            "metadatas": [],
            "distances": [],
        }
        for i in range(len(pdf_result["ids"][0])):
            if pdf_result["metadatas"][0][i]["source"] == pdf_path:
                filtered_pdf_result["ids"].append(pdf_result["ids"][0][i])
                filtered_pdf_result["documents"].append(pdf_result["documents"][0][i])
                filtered_pdf_result["metadatas"].append(pdf_result["metadatas"][0][i])
                filtered_pdf_result["distances"].append(pdf_result["distances"][0][i])
        filtered_pdf_result["ids"] = filtered_pdf_result["ids"][:3]
        filtered_pdf_result["documents"] = filtered_pdf_result["documents"][:3]
        filtered_pdf_result["metadatas"] = filtered_pdf_result["metadatas"][:3]
        filtered_pdf_result["distances"] = filtered_pdf_result["distances"][:3]

        if filtered_pdf_result["documents"]:
            logger.info(f"PDF query results: {filtered_pdf_result}")
            print(f"PDF query results ('{pdf_query}'): {filtered_pdf_result}")
        else:
            logger.warning(f"No PDF chunks found for the query '{pdf_query}'.")
            print(f"No PDF chunks found for the query '{pdf_query}'.")

    # Query for video content
    video_query = "Successful"
    video_result = chroma.query(query_text=video_query, n_results=50)
    if video_result and video_result["documents"]:
        filtered_video_result = {
            "ids": [],
            "documents": [],
            "metadatas": [],
            "distances": [],
        }
        for i in range(len(video_result["ids"][0])):
            if video_result["metadatas"][0][i]["source"] == video_path:
                filtered_video_result["ids"].append(video_result["ids"][0][i])
                filtered_video_result["documents"].append(
                    video_result["documents"][0][i]
                )
                filtered_video_result["metadatas"].append(
                    video_result["metadatas"][0][i]
                )
                filtered_video_result["distances"].append(
                    video_result["distances"][0][i]
                )
        filtered_video_result["ids"] = filtered_video_result["ids"][:3]
        filtered_video_result["documents"] = filtered_video_result["documents"][:3]
        filtered_video_result["metadatas"] = filtered_video_result["metadatas"][:3]
        filtered_video_result["distances"] = filtered_video_result["distances"][:3]

        if filtered_video_result["documents"]:
            logger.info(f"Video query results: {filtered_video_result}")
            print(f"Video query results ('{video_query}'): {filtered_video_result}")
        else:
            logger.warning(f"No video segments found for the query '{video_query}'.")
            print(f"No video segments found for the query '{video_query}'.")
    else:
        logger.warning(f"No results found for the query '{video_query}'.")
        print(f"No results found for the query '{video_query}'.")
