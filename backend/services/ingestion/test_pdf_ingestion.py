from pdf_ingestor import PDFIngestor

if __name__ == "__main__":
    file_path = "./../../../data/raw/file01.pdf"

    try:
        with PDFIngestor(file_path) as ingestor:
            data = ingestor.extract_all()
            print("Metadata:", data["metadata"])
            print("First Page Text Preview:\n", data["pages"][0]["text"][:300])

            #  Chunking test
            chunks = ingestor.chunk_text(chunk_size=500, chunk_overlap=50)
            print(f"\nTotal Chunks: {len(chunks)}\n")

            print("Preview of First 3 Chunks:\n")
            for i, chunk in enumerate(chunks[:3]):
                print(f"--- Chunk {i+1} ---")
                print(chunk)
                print()

            # Inspect chunk lengths
            print("Chunk Lengths (first 10 chunks):", [len(c) for c in chunks[:10]])

    except Exception as e:
        print(f"[ERROR] {e}")
