import os
import logging
from typing import List, Dict, Optional
import chromadb
from chromadb.errors import ChromaError

# Set up logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class ChromaManager:
    def __init__(
        self,
        persist_directory: str = "backend/db",
        collection_name: str = "multimodal_collection",
    ):
        self.persist_directory = persist_directory
        self.collection_name = collection_name

        try:
            os.makedirs(self.persist_directory, exist_ok=True)

            # NEW: use PersistentClient instead of deprecated Settings
            self.client = chromadb.PersistentClient(path=self.persist_directory)

            self.collection = self.client.get_or_create_collection(
                name=self.collection_name
            )
            logger.info(f"Connected to ChromaDB. Collection: '{self.collection_name}'")
        except Exception as e:
            logger.error(f"Failed to initialize ChromaManager: {e}")
            raise

    def add_documents(
        self, texts: List[str], metadatas: List[Dict], ids: List[str]
    ) -> None:
        if not (len(texts) == len(metadatas) == len(ids)):
            raise ValueError("Length of texts, metadatas, and ids must be the same.")

        try:
            self.collection.add(documents=texts, metadatas=metadatas, ids=ids)
            logger.info(f"Added {len(texts)} documents to the collection.")
        except ChromaError as e:
            logger.error(f"ChromaDB error during add_documents: {e}")
            raise

    def query(self, query_text: str, n_results: int = 3) -> Optional[Dict]:
        try:
            results = self.collection.query(
                query_texts=[query_text], n_results=n_results
            )
            logger.info(
                f"Query successful. Found {len(results['documents'][0])} results."
            )
            return results
        except Exception as e:
            logger.error(f"Error during query: {e}")
            return None
