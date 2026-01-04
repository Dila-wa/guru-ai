"""
Configuration settings for Guru.ai backend
"""
import os
from pathlib import Path

# Base paths
BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"
TEXTBOOKS_DIR = DATA_DIR / "textbooks"
RAW_PDFS_DIR = TEXTBOOKS_DIR / "raw_pdfs"
TRAINING_DIR = DATA_DIR / "training"

# Model paths
MODELS_DIR = DATA_DIR / "models"
CLASSIFIER_MODEL_PATH = MODELS_DIR / "syllabus_classifier.pkl"
VECTORIZER_MODEL_PATH = MODELS_DIR / "tfidf_vectorizer.pkl"
FAISS_INDEX_PATH = MODELS_DIR / "faiss_index.bin"
EMBEDDINGS_PATH = MODELS_DIR / "embeddings_metadata.pkl"

# Create models directory if it doesn't exist
MODELS_DIR.mkdir(parents=True, exist_ok=True)

# Chunking configuration
CHUNK_MIN_WORDS = 300
CHUNK_MAX_WORDS = 500
CHUNK_OVERLAP_WORDS = 50

# Embedding configuration
EMBEDDING_DIM = 384  # sentence-transformers default
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

# TF-IDF configuration
TFIDF_MAX_FEATURES = 5000
TFIDF_MIN_DF = 2
TFIDF_MAX_DF = 0.8

# Random Forest configuration
RF_N_ESTIMATORS = 100
RF_MAX_DEPTH = 20
RF_MIN_SAMPLES_SPLIT = 5
RF_MIN_SAMPLES_LEAF = 2

# Classification threshold
SYLLABUS_CONFIDENCE_THRESHOLD = 0.6

# FastAPI configuration
API_TITLE = "Guru.ai Backend"
API_DESCRIPTION = "Closed-syllabus AI system for Sri Lankan students"
API_VERSION = "1.0.0"

# Supported grades and subjects (Sri Lanka curriculum)
SUPPORTED_GRADES = ["Grade 6", "Grade 7", "Grade 8", "Grade 9", "Grade 10", "Grade 11", "Grade 12", "Grade 13"]
SUPPORTED_SUBJECTS = ["Mathematics", "Science", "English", "Sinhala", "Tamil", "History", "Civics", "Geography"]

# Response messages
MSG_OUT_OF_SYLLABUS = "This question is not covered in your selected textbook."
MSG_NO_CONTENT = "No relevant content found in the textbook for this question."
MSG_PROCESSING_ERROR = "An error occurred while processing your question. Please try again."

# FAISS configuration
FAISS_TOP_K_CHUNKS = 5  # Number of chunks to retrieve for context

# Logging
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
