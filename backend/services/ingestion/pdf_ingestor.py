import os
import fitz  # PyMuPDF
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO
)  # You can adjust level to DEBUG or ERROR as needed


class PDFIngestor:
    """
    A class for extracting metadata and text from a PDF document.
    """

    def __init__(self, file_path):
        self.file_path = file_path
        self.doc = None

    def __enter__(self):
        self._validate_pdf_file()
        try:
            self.doc = fitz.open(self.file_path)
            logger.info(f"Successfully opened PDF: {self.file_path}")
            return self
        except Exception as e:
            logger.error(f"Failed to open PDF '{self.file_path}': {e}")
            raise ValueError(f"Could not open PDF file: {e}")

    def __exit__(self, exc_type, exc_value, traceback):
        if self.doc is not None:
            self.doc.close()
            logger.info(f"Closed PDF: {self.file_path}")

    def _validate_pdf_file(self):
        if not os.path.isfile(self.file_path):
            logger.error(f"File not found: {self.file_path}")
            raise FileNotFoundError(f"File not found: {self.file_path}")
        if not self.file_path.lower().endswith(".pdf"):
            logger.error(f"Invalid file type (not a PDF): {self.file_path}")
            raise ValueError("The provided file must be a PDF.")

    def extract_metadata(self):
        """
        Extract metadata from the PDF document.
        """
        if self.doc is None:
            logger.error("PDF document is not opened.")
            raise RuntimeError("PDF document is not opened.")
        return self.doc.metadata

    def extract_text(self):
        """
        Extract text from each page of the PDF document.
        """
        if self.doc is None:
            logger.error("PDF document is not opened.")
            raise RuntimeError("PDF document is not opened.")

        text_data = []
        for page_num in range(len(self.doc)):
            try:
                page = self.doc.load_page(page_num)
                text = page.get_text()
                text_data.append({"page_number": page_num + 1, "text": text})
            except Exception as e:
                logger.warning(f"Failed to extract text from page {page_num + 1}: {e}")
                text_data.append(
                    {"page_number": page_num + 1, "text": "", "error": str(e)}
                )
        return text_data

    def extract_all(self):
        """
        Extract both metadata and text from the PDF document.
        """
        metadata = self.extract_metadata()
        pages = self.extract_text()
        return {"metadata": metadata, "pages": pages}
