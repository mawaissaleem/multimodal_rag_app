# app/services/query_service.py

from typing import List, Optional
import logging

from backend.core.vector_store import (
    get_chroma_collection,
)

logger = logging.getLogger(__name__)


def semantic_search(query: str, filename: Optional[str], top_k: int) -> List[str]:
    try:
        collection = get_chroma_collection()

        filter_by = {"filename": filename} if filename else {}

        # Use ChromaDB's internal embedding model
        search_results = collection.query(
            query_texts=[query],  # Chroma embed the query
            n_results=top_k,
            # where=filter_by,
        )

        documents = search_results.get("documents", [[]])[0]
        if not documents:
            logger.info(f"No documents found for query: {query}, filename: {filename}")
            return []
        return documents

    except Exception as e:
        logger.error(f"Search failed: {e}")
        raise
