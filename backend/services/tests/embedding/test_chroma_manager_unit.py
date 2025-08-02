import os
import sys

# Ensure project root is in sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../..")))
from unittest import TestCase
from unittest.mock import MagicMock
from backend.services.embedding.chroma_manager import ChromaManager


class TestChromaManager(TestCase):
    def setUp(self):
        # Debug: Print sys.path to verify project root inclusion
        print(f"sys.path: {sys.path}")

        # Instantiate ChromaManager
        self.manager = ChromaManager(
            persist_directory="test_dir", collection_name="test_collection"
        )

        # Create mock collection and assign it directly to manager.collection
        self.mock_collection = MagicMock()
        self.manager.collection = self.mock_collection

        # Debug: Verify manager's collection is the mocked one
        print(f"Manager collection: {self.manager.collection}")

    def test_add_documents_invalid_length(self):
        texts = ["doc1", "doc2"]
        metadatas = [{"source": "s1"}]  # mismatch
        ids = ["id1", "id2"]

        with self.assertRaises(ValueError):
            self.manager.add_documents(texts, metadatas, ids)

    def test_add_documents_success(self):
        texts = ["Hello world", "Python is awesome"]
        metadatas = [{"source": "test1"}, {"source": "test2"}]
        ids = ["id1", "id2"]

        self.manager.add_documents(texts, metadatas, ids)

        # Debug: Print mock calls for add
        print(f"Mock add calls: {self.mock_collection.add.mock_calls}")

        self.mock_collection.add.assert_called_once_with(
            documents=texts, metadatas=metadatas, ids=ids
        )

    def test_query_success(self):
        expected_response = {
            "documents": [["doc1", "doc2"]],
            "metadatas": [[{"source": "src1"}, {"source": "src2"}]],
            "ids": [["id1", "id2"]],
            "distances": [[0.1, 0.2]],
        }

        self.mock_collection.query.return_value = expected_response

        result = self.manager.query("test query")

        # Debug: Print mock calls for query
        print(f"Mock query calls: {self.mock_collection.query.mock_calls}")

        self.mock_collection.query.assert_called_once_with(
            query_texts=["test query"], n_results=3
        )
        self.assertEqual(result, expected_response)
