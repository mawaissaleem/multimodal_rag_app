from pdf_ingestor import PDFIngestor

if __name__ == "__main__":
    file_path = "./../../../data/raw/file01.pdf"

    try:
        with PDFIngestor(file_path) as ingestor:
            data = ingestor.extract_all()
            print("Metadata:", data["metadata"])
            print("First Page Text Preview:\n", data["pages"][0]["text"][:300])
    except Exception as e:
        print(f"[ERROR] {e}")
