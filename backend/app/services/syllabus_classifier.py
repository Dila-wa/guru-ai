"""
Syllabus classifier - Random Forest model for checking if questions are in-syllabus
"""
import logging
from typing import Tuple
import numpy as np
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import TfidfVectorizer

logger = logging.getLogger(__name__)


class SyllabusClassifier:
    """Random Forest classifier for binary classification (in-syllabus vs out-of-syllabus)"""

    def __init__(
        self,
        n_estimators: int = 100,
        max_depth: int = 20,
        min_samples_split: int = 5,
        min_samples_leaf: int = 2,
        tfidf_max_features: int = 5000,
        tfidf_min_df: int = 2,
        tfidf_max_df: float = 0.8,
    ):
        """
        Initialize classifier with hyperparameters

        Args:
            n_estimators: Number of trees in forest
            max_depth: Maximum tree depth
            min_samples_split: Minimum samples to split node
            min_samples_leaf: Minimum samples in leaf
            tfidf_max_features: Max features for TF-IDF
            tfidf_min_df: Min document frequency for TF-IDF
            tfidf_max_df: Max document frequency for TF-IDF
        """
        self.tfidf_vectorizer = TfidfVectorizer(
            max_features=tfidf_max_features,
            min_df=tfidf_min_df,
            max_df=tfidf_max_df,
            ngram_range=(1, 2),
            lowercase=True,
            stop_words="english",
        )

        self.classifier = RandomForestClassifier(
            n_estimators=n_estimators,
            max_depth=max_depth,
            min_samples_split=min_samples_split,
            min_samples_leaf=min_samples_leaf,
            random_state=42,
            n_jobs=-1,
            verbose=0,
        )

        self.is_trained = False

    def train(self, questions: list, labels: list) -> None:
        """
        Train the classifier

        Args:
            questions: List of question texts
            labels: List of binary labels (1=in-syllabus, 0=out-of-syllabus)
        """
        if len(questions) != len(labels):
            raise ValueError("Number of questions must match number of labels")

        if len(questions) < 10:
            logger.warning(
                f"Training with only {len(questions)} samples. "
                "Recommend at least 100 samples for robust model."
            )

        logger.info(f"Training classifier with {len(questions)} samples")

        # Fit TF-IDF vectorizer and transform questions
        X = self.tfidf_vectorizer.fit_transform(questions)

        # Train Random Forest
        self.classifier.fit(X, labels)

        self.is_trained = True

        # Log class distribution
        unique, counts = np.unique(labels, return_counts=True)
        for label, count in zip(unique, counts):
            label_name = "In-Syllabus" if label == 1 else "Out-of-Syllabus"
            logger.info(f"{label_name}: {count} samples ({100*count/len(labels):.1f}%)")

    def predict(self, question: str) -> Tuple[int, float]:
        """
        Predict if question is in-syllabus

        Args:
            question: Question text

        Returns:
            Tuple of (prediction, confidence)
            - prediction: 1 (in-syllabus) or 0 (out-of-syllabus)
            - confidence: Confidence score (0-1)
        """
        if not self.is_trained:
            raise RuntimeError("Classifier must be trained before making predictions")

        X = self.tfidf_vectorizer.transform([question])
        prediction = self.classifier.predict(X)[0]
        probabilities = self.classifier.predict_proba(X)[0]

        # Get confidence for the predicted class
        confidence = probabilities[prediction]

        return int(prediction), float(confidence)

    def predict_batch(self, questions: list) -> Tuple[list, list]:
        """
        Batch predict

        Args:
            questions: List of question texts

        Returns:
            Tuple of (predictions, confidences)
        """
        if not self.is_trained:
            raise RuntimeError("Classifier must be trained before making predictions")

        predictions = []
        confidences = []

        for question in questions:
            pred, conf = self.predict(question)
            predictions.append(pred)
            confidences.append(conf)

        return predictions, confidences

    def save(self, classifier_path: str, vectorizer_path: str) -> None:
        """
        Save model and vectorizer to disk

        Args:
            classifier_path: Path to save classifier
            vectorizer_path: Path to save vectorizer
        """
        if not self.is_trained:
            logger.warning("Saving untrained model")

        try:
            joblib.dump(self.classifier, classifier_path)
            joblib.dump(self.tfidf_vectorizer, vectorizer_path)
            logger.info(f"Saved classifier to {classifier_path}")
            logger.info(f"Saved vectorizer to {vectorizer_path}")
        except Exception as e:
            logger.error(f"Failed to save model: {e}")
            raise

    def load(self, classifier_path: str, vectorizer_path: str) -> None:
        """
        Load model and vectorizer from disk

        Args:
            classifier_path: Path to classifier
            vectorizer_path: Path to vectorizer
        """
        try:
            self.classifier = joblib.load(classifier_path)
            self.tfidf_vectorizer = joblib.load(vectorizer_path)
            self.is_trained = True
            logger.info(f"Loaded classifier from {classifier_path}")
            logger.info(f"Loaded vectorizer from {vectorizer_path}")
        except Exception as e:
            logger.error(f"Failed to load model: {e}")
            raise

    def get_feature_importance(self, top_n: int = 20) -> list:
        """
        Get top N most important features

        Args:
            top_n: Number of top features to return

        Returns:
            List of (feature_name, importance) tuples
        """
        if not self.is_trained:
            raise RuntimeError("Classifier must be trained to get feature importance")

        importances = self.classifier.feature_importances_
        feature_names = self.tfidf_vectorizer.get_feature_names_out()

        top_indices = np.argsort(importances)[-top_n:][::-1]

        return [(feature_names[i], importances[i]) for i in top_indices]
