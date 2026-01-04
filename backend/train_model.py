"""
Script to train the guardrail Random Forest classifier

Usage:
    python train_model.py
"""
import sys
import logging
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

import pandas as pd
from app.services.syllabus_classifier import SyllabusClassifier
from app import config

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


def train_guardrail_model(csv_path: str = "data/training/question_labels.csv"):
    """
    Train the Random Forest guardrail classifier

    Args:
        csv_path: Path to training data CSV
    """
    csv_path = Path(csv_path)

    if not csv_path.exists():
        logger.error(f"Training data file not found: {csv_path}")
        return False

    try:
        # Load training data
        logger.info(f"Loading training data from {csv_path}")
        df = pd.read_csv(csv_path)

        logger.info(f"Loaded {len(df)} samples")
        logger.info(f"Columns: {df.columns.tolist()}")
        logger.info(f"Shape: {df.shape}")

        # Check for required columns
        required_columns = ["question", "label"]
        missing_cols = [col for col in required_columns if col not in df.columns]

        if missing_cols:
            logger.error(f"Missing required columns: {missing_cols}")
            return False

        # Extract questions and labels
        questions = df["question"].tolist()
        labels = df["label"].tolist()

        # Validate labels
        unique_labels = set(labels)
        if not unique_labels.issubset({0, 1}):
            logger.error(f"Invalid labels found: {unique_labels}. Must be 0 or 1.")
            return False

        logger.info(f"Unique labels: {sorted(unique_labels)}")

        # Initialize classifier with optimized hyperparameters
        logger.info("Initializing Random Forest classifier...")
        classifier = SyllabusClassifier(
            n_estimators=config.RF_N_ESTIMATORS,
            max_depth=config.RF_MAX_DEPTH,
            min_samples_split=config.RF_MIN_SAMPLES_SPLIT,
            min_samples_leaf=config.RF_MIN_SAMPLES_LEAF,
            tfidf_max_features=config.TFIDF_MAX_FEATURES,
            tfidf_min_df=config.TFIDF_MIN_DF,
            tfidf_max_df=config.TFIDF_MAX_DF,
        )

        # Train model
        logger.info("Training classifier...")
        classifier.train(questions, labels)

        # Get feature importance
        logger.info("\nTop 10 most important features:")
        top_features = classifier.get_feature_importance(top_n=10)
        for feature, importance in top_features:
            logger.info(f"  {feature}: {importance:.4f}")

        # Create models directory
        config.MODELS_DIR.mkdir(parents=True, exist_ok=True)

        # Save model
        logger.info(f"\nSaving model to {config.MODELS_DIR}")
        classifier.save(
            str(config.CLASSIFIER_MODEL_PATH),
            str(config.VECTORIZER_MODEL_PATH),
        )

        logger.info("✅ Model training completed successfully!")

        # Test the trained model
        logger.info("\n--- Testing trained model ---")
        test_questions = [
            "What is photosynthesis?",
            "How do I become a programmer?",
            "Solve x² + 5x + 6 = 0",
        ]

        for q in test_questions:
            pred, conf = classifier.predict(q)
            label = "IN-SYLLABUS" if pred == 1 else "OUT-OF-SYLLABUS"
            logger.info(f"Q: {q}")
            logger.info(f"   → {label} (confidence: {conf:.3f})")

        return True

    except Exception as e:
        logger.error(f"Error training model: {e}", exc_info=True)
        return False


if __name__ == "__main__":
    success = train_guardrail_model()
    sys.exit(0 if success else 1)
