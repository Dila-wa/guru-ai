"""
Guardrail - Safety mechanism to prevent out-of-syllabus answers
"""
import logging
from pathlib import Path
from typing import Optional, Tuple
from app.services.syllabus_classifier import SyllabusClassifier
from app import config

logger = logging.getLogger(__name__)


class Guardrail:
    """Guardrail to ensure questions are in-syllabus"""

    def __init__(self):
        """Initialize guardrail with pretrained Random Forest model"""
        self.classifier = SyllabusClassifier()
        self.model_loaded = False

    def load_model(self) -> None:
        """Load the trained Random Forest classifier from disk"""
        classifier_path = config.CLASSIFIER_MODEL_PATH
        vectorizer_path = config.VECTORIZER_MODEL_PATH

        if not Path(classifier_path).exists() or not Path(vectorizer_path).exists():
            logger.warning(
                f"Model files not found at {classifier_path} or {vectorizer_path}. "
                "Please train the model first using train_guardrail_model()."
            )
            return

        try:
            self.classifier.load(str(classifier_path), str(vectorizer_path))
            self.model_loaded = True
            logger.info("Guardrail model loaded successfully")
        except Exception as e:
            logger.error(f"Failed to load guardrail model: {e}")
            raise

    def is_in_syllabus(self, question: str, confidence_threshold: Optional[float] = None) -> Tuple[bool, float]:
        """
        Check if a question is within the syllabus

        Args:
            question: Question text to check
            confidence_threshold: Minimum confidence required (default: from config)

        Returns:
            Tuple of (is_in_syllabus, confidence)
            - is_in_syllabus: True if question is in syllabus, False otherwise
            - confidence: Confidence score (0-1)
        """
        if not self.model_loaded:
            logger.error("Model not loaded. Call load_model() first.")
            raise RuntimeError("Guardrail model not loaded")

        if confidence_threshold is None:
            confidence_threshold = config.SYLLABUS_CONFIDENCE_THRESHOLD

        prediction, confidence = self.classifier.predict(question)

        # Convert prediction (1/0) to boolean (in_syllabus)
        is_in_syllabus = bool(prediction == 1)

        logger.debug(f"Question: '{question[:50]}...' | In-syllabus: {is_in_syllabus} | Confidence: {confidence:.3f}")

        return is_in_syllabus, confidence

    def batch_check(self, questions: list, confidence_threshold: Optional[float] = None) -> list:
        """
        Check multiple questions

        Args:
            questions: List of question texts
            confidence_threshold: Minimum confidence required

        Returns:
            List of (is_in_syllabus, confidence) tuples
        """
        if not self.model_loaded:
            raise RuntimeError("Guardrail model not loaded")

        predictions, confidences = self.classifier.predict_batch(questions)

        if confidence_threshold is None:
            confidence_threshold = config.SYLLABUS_CONFIDENCE_THRESHOLD

        results = []
        for pred, conf in zip(predictions, confidences):
            is_in_syllabus = bool(pred == 1)
            results.append((is_in_syllabus, conf))

        return results
