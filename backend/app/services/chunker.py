"""
Text chunker - splits textbook content into manageable chunks
"""
import logging
from typing import List, Dict, Tuple

logger = logging.getLogger(__name__)


class TextChunk:
    """Represents a chunk of text with metadata"""

    def __init__(
        self,
        chunk_id: int,
        content: str,
        page_number: int,
        grade: str,
        subject: str,
        start_word_index: int,
        end_word_index: int,
    ):
        self.chunk_id = chunk_id
        self.content = content
        self.page_number = page_number
        self.grade = grade
        self.subject = subject
        self.start_word_index = start_word_index
        self.end_word_index = end_word_index
        self.word_count = len(content.split())

    def to_dict(self) -> Dict:
        """Convert chunk to dictionary"""
        return {
            "chunk_id": self.chunk_id,
            "content": self.content,
            "page_number": self.page_number,
            "grade": self.grade,
            "subject": self.subject,
            "start_word_index": self.start_word_index,
            "end_word_index": self.end_word_index,
            "word_count": self.word_count,
        }


class Chunker:
    """Splits textbook content into chunks with metadata preservation"""

    def __init__(self, min_words: int = 300, max_words: int = 500, overlap_words: int = 50):
        """
        Initialize chunker

        Args:
            min_words: Minimum words per chunk (default: 300)
            max_words: Maximum words per chunk (default: 500)
            overlap_words: Word overlap between chunks (default: 50)
        """
        self.min_words = min_words
        self.max_words = max_words
        self.overlap_words = overlap_words
        self.chunk_counter = 0

    def chunk_text(
        self, text: str, page_number: int, grade: str, subject: str
    ) -> List[TextChunk]:
        """
        Chunk text into fixed-size blocks with metadata

        Args:
            text: Text to chunk
            page_number: Page number for metadata
            grade: Grade level for metadata
            subject: Subject name for metadata

        Returns:
            List of TextChunk objects
        """
        words = text.split()

        if len(words) < self.min_words:
            logger.warning(
                f"Text has {len(words)} words, below minimum {self.min_words}. "
                f"Will create single chunk anyway."
            )

        chunks = []
        chunk_id = self.chunk_counter
        step = max(1, self.max_words - self.overlap_words)

        for start_idx in range(0, len(words), step):
            end_idx = min(start_idx + self.max_words, len(words))

            # Ensure minimum chunk size (except for the last chunk)
            if end_idx - start_idx < self.min_words and end_idx < len(words):
                continue

            chunk_words = words[start_idx:end_idx]
            chunk_text = " ".join(chunk_words)

            chunk = TextChunk(
                chunk_id=chunk_id,
                content=chunk_text,
                page_number=page_number,
                grade=grade,
                subject=subject,
                start_word_index=start_idx,
                end_word_index=end_idx,
            )

            chunks.append(chunk)
            chunk_id += 1
            self.chunk_counter = chunk_id

            logger.debug(
                f"Created chunk {chunk.chunk_id} | Page {page_number} | "
                f"Words: {chunk.word_count} | Grade: {grade} | Subject: {subject}"
            )

        if not chunks and len(words) > 0:
            # Create at least one chunk if text exists
            chunk = TextChunk(
                chunk_id=chunk_id,
                content=text,
                page_number=page_number,
                grade=grade,
                subject=subject,
                start_word_index=0,
                end_word_index=len(words),
            )
            chunks.append(chunk)
            self.chunk_counter = chunk_id + 1

        return chunks

    def chunk_pages(
        self, page_texts: Dict[int, str], grade: str, subject: str
    ) -> List[TextChunk]:
        """
        Chunk multiple pages

        Args:
            page_texts: Dictionary mapping page number to text
            grade: Grade level
            subject: Subject name

        Returns:
            List of all chunks
        """
        all_chunks = []

        for page_num in sorted(page_texts.keys()):
            text = page_texts[page_num]
            page_chunks = self.chunk_text(text, page_num, grade, subject)
            all_chunks.extend(page_chunks)

        logger.info(
            f"Created {len(all_chunks)} chunks for {len(page_texts)} pages | "
            f"Grade: {grade} | Subject: {subject}"
        )

        return all_chunks

    def reset_counter(self):
        """Reset chunk counter (useful when processing new documents)"""
        self.chunk_counter = 0
