"""
Textbook loader - extracts text from PDF files
"""
import logging
from pathlib import Path
from typing import Dict, List, Tuple
import pdfplumber

logger = logging.getLogger(__name__)


class TextbookLoader:
    """Loads and extracts text from PDF textbooks"""

    def __init__(self):
        """Initialize the textbook loader"""
        self.loaded_textbooks = {}

    def load_pdf(self, pdf_path: str, grade: str, subject: str) -> Dict[int, str]:
        """
        Load a PDF file and extract text by page

        Args:
            pdf_path: Path to the PDF file
            grade: Grade level (e.g., "Grade 10")
            subject: Subject name (e.g., "Mathematics")

        Returns:
            Dictionary mapping page number to extracted text

        Raises:
            FileNotFoundError: If PDF file doesn't exist
            Exception: If PDF extraction fails
        """
        pdf_path = Path(pdf_path)

        if not pdf_path.exists():
            raise FileNotFoundError(f"PDF file not found: {pdf_path}")

        if not pdf_path.suffix.lower() == ".pdf":
            raise ValueError(f"File must be a PDF: {pdf_path}")

        page_texts = {}

        try:
            with pdfplumber.open(pdf_path) as pdf:
                total_pages = len(pdf.pages)
                logger.info(
                    f"Loading PDF: {pdf_path.name} | "
                    f"Grade: {grade} | Subject: {subject} | "
                    f"Total pages: {total_pages}"
                )

                for page_num, page in enumerate(pdf.pages, start=1):
                    try:
                        text = page.extract_text()
                        if text:
                            # Clean up text
                            text = self._clean_text(text)
                            page_texts[page_num] = text
                            logger.debug(
                                f"Extracted {len(text)} characters from page {page_num}"
                            )
                        else:
                            logger.warning(f"No text extracted from page {page_num}")
                            page_texts[page_num] = ""

                    except Exception as e:
                        logger.error(f"Error extracting text from page {page_num}: {e}")
                        page_texts[page_num] = ""

            logger.info(f"Successfully loaded {len(page_texts)} pages from {pdf_path.name}")
            return page_texts

        except Exception as e:
            logger.error(f"Failed to load PDF {pdf_path}: {e}")
            raise

    def extract_all_pages(self, pdf_path: str) -> List[Tuple[int, str]]:
        """
        Extract all pages from a PDF as (page_number, text) tuples

        Args:
            pdf_path: Path to the PDF file

        Returns:
            List of (page_number, text) tuples
        """
        page_texts = self.load_pdf(pdf_path, grade="", subject="")
        return [(page_num, text) for page_num, text in page_texts.items()]

    @staticmethod
    def _clean_text(text: str) -> str:
        """
        Clean extracted text

        Args:
            text: Raw extracted text

        Returns:
            Cleaned text
        """
        # Remove extra whitespace
        lines = text.split("\n")
        cleaned_lines = [line.strip() for line in lines if line.strip()]
        cleaned_text = " ".join(cleaned_lines)

        # Replace multiple spaces with single space
        while "  " in cleaned_text:
            cleaned_text = cleaned_text.replace("  ", " ")

        return cleaned_text

    def get_page_count(self, pdf_path: str) -> int:
        """
        Get total number of pages in a PDF

        Args:
            pdf_path: Path to the PDF file

        Returns:
            Number of pages in the PDF
        """
        pdf_path = Path(pdf_path)

        if not pdf_path.exists():
            raise FileNotFoundError(f"PDF file not found: {pdf_path}")

        try:
            with pdfplumber.open(pdf_path) as pdf:
                return len(pdf.pages)
        except Exception as e:
            logger.error(f"Failed to get page count for {pdf_path}: {e}")
            raise
