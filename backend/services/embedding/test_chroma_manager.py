# test_chroma_manager.py
from chroma_manager import ChromaManager  # if in same directory


def run_tests():
    cm = ChromaManager(persist_directory="test_db")

    texts = ["Hello world", "Multimodal RAG is powerful", "Python is great"]
    metadatas = [{"source": "test1"}, {"source": "test2"}, {"source": "test3"}]
    ids = ["id1", "id2", "id3"]

    cm.add_documents(texts=texts, metadatas=metadatas, ids=ids)

    print("\nQuerying...\n")
    result = cm.query("Multimodal", n_results=2)
    print(result)


if __name__ == "__main__":
    run_tests()
