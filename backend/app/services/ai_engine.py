"""
AI Engine - Generates answers based on textbook content
"""
import logging
from typing import List, Dict, Optional
from app import config
from app.models.schema import TextbookChunk

logger = logging.getLogger(__name__)


class AIEngine:
    """Generates answers based on retrieved textbook chunks"""

    def __init__(self):
        """Initialize AI engine"""
        self.model_name = "text-generation-model"  # Placeholder for actual model
        self.temperature = 0.7
        self.max_tokens = 500

    def generate_answer(
        self,
        question: str,
        chunks: List[Dict],
        grade: str,
        subject: str,
    ) -> str:
        """
        Generate an answer based on question and retrieved chunks

        Args:
            question: The student's question
            chunks: List of relevant textbook chunks
            grade: Grade level
            subject: Subject name

        Returns:
            Generated answer string
        """
        if not chunks:
            logger.warning(f"No chunks provided for question: {question}")
            return config.MSG_NO_CONTENT

        # Build context from chunks
        context = self._build_context(chunks)

        if not context.strip():
            return config.MSG_NO_CONTENT

        # Generate answer using simple retrieval + template
        # In production, this would use an actual LLM
        answer = self._generate_from_context(question, context, grade, subject)

        return answer

    def _build_context(self, chunks: List[Dict]) -> str:
        """
        Build context string from chunks

        Args:
            chunks: List of chunk dictionaries

        Returns:
            Context string
        """
        context_parts = []

        for chunk in chunks[:config.FAISS_TOP_K_CHUNKS]:
            content = chunk.get("content", "")
            page_num = chunk.get("page_number", "?")

            context_parts.append(f"[Page {page_num}]:\n{content}")

        return "\n\n".join(context_parts)

    def _generate_from_context(
        self, question: str, context: str, grade: str, subject: str
    ) -> str:
        """
        Generate answer from context (template-based for MVP)

        Args:
            question: Question text
            context: Context from textbook
            grade: Grade level
            subject: Subject name

        Returns:
            Generated answer
        """
        # For MVP, use template-based generation
        # In production, this would use an actual LLM API

        answer = f"""Based on the {grade} {subject} textbook content:

{context}

In summary, {self._extract_summary_from_context(context)}"""

        return answer

    @staticmethod
    def _extract_summary_from_context(context: str) -> str:
        """
        Extract a summary from context (simple heuristic)

        Args:
            context: Context string

        Returns:
            Summary
        """
        # Simple heuristic: take first 3 sentences
        sentences = context.split(".")
        summary_sentences = [s.strip() for s in sentences[:3] if s.strip()]
        summary = ". ".join(summary_sentences).strip()

        if not summary:
            return context[:200]

        return summary

    def validate_answer(
        self, answer: str, original_question: str, chunks: List[Dict]
    ) -> bool:
        """
        Validate that answer is grounded in provided chunks

        Args:
            answer: Generated answer
            original_question: Original question
            chunks: Chunks used for generation

        Returns:
            True if answer is grounded, False otherwise
        """
        if not answer or not chunks:
            return False

        # Simple validation: check if answer contains content from chunks
        answer_lower = answer.lower()

        for chunk in chunks:
            content = chunk.get("content", "").lower()
            # Check if any significant portion of chunk text appears in answer
            words = content.split()
            for word in words[:10]:  # Check first 10 words
                if len(word) > 4 and word in answer_lower:
                    return True

        return False

    def get_stats(self) -> Dict:
        """Get engine statistics"""
        return {
            "model_name": self.model_name,
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
            "status": "ready",
        }
