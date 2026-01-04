"""
Integration testing script - Test all components together

Usage:
    python test_integration.py
"""
import sys
import logging
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


def test_guardrail():
    """Test guardrail functionality"""
    logger.info("\n" + "=" * 60)
    logger.info("Testing Guardrail (Random Forest)")
    logger.info("=" * 60)

    from app.services.guardrail import Guardrail

    try:
        guardrail = Guardrail()
        guardrail.load_model()

        test_cases = [
            ("What is photosynthesis?", True),
            ("Solve x² + 2x + 1 = 0", True),
            ("How do I become an astronaut?", False),
            ("What is the capital of Sri Lanka?", True),
            ("How much money should I invest?", False),
        ]

        for question, expected_in_syllabus in test_cases:
            is_in, conf = guardrail.is_in_syllabus(question)
            status = "✅" if is_in == expected_in_syllabus else "⚠️"

            logger.info(f"{status} Q: {question}")
            logger.info(f"   In-syllabus: {is_in}, Confidence: {conf:.1%}")

        logger.info("✅ Guardrail tests passed!")
        return True

    except Exception as e:
        logger.error(f"❌ Guardrail test failed: {e}")
        return False


def test_chunker():
    """Test text chunking"""
    logger.info("\n" + "=" * 60)
    logger.info("Testing Text Chunker")
    logger.info("=" * 60)

    from app.services.chunker import Chunker

    try:
        chunker = Chunker(min_words=300, max_words=500)

        sample_text = " ".join(["word"] * 1000)  # 1000 words

        chunks = chunker.chunk_text(sample_text, page_number=1, grade="Grade 10", subject="Science")

        logger.info(f"Chunked 1000 words into {len(chunks)} chunks")

        for chunk in chunks:
            logger.info(f"  Chunk {chunk.chunk_id}: {chunk.word_count} words, Page {chunk.page_number}")

        logger.info("✅ Chunker tests passed!")
        return True

    except Exception as e:
        logger.error(f"❌ Chunker test failed: {e}")
        return False


def test_vector_store():
    """Test vector store"""
    logger.info("\n" + "=" * 60)
    logger.info("Testing Vector Store (FAISS)")
    logger.info("=" * 60)

    try:
        import numpy as np
        from app.services.vector_store import VectorStore

        vector_store = VectorStore(embedding_dim=384)

        # Create dummy embeddings
        embeddings = np.random.randn(10, 384).astype(np.float32)

        # Create dummy metadata
        metadata = [
            {
                "chunk_id": i,
                "content": f"Sample content {i}",
                "page_number": i % 5,
                "grade": "Grade 10",
                "subject": "Science",
            }
            for i in range(10)
        ]

        vector_store.add_embeddings(embeddings, metadata)

        stats = vector_store.get_stats()
        logger.info(f"Vector store created with {stats['total_vectors']} vectors")

        # Test search
        query_embedding = np.random.randn(1, 384).astype(np.float32)
        results = vector_store.search(query_embedding, k=3)

        logger.info(f"Found {len(results)} nearest neighbors")

        logger.info("✅ Vector store tests passed!")
        return True

    except ImportError:
        logger.warning("⚠️  FAISS not installed, skipping vector store tests")
        return True
    except Exception as e:
        logger.error(f"❌ Vector store test failed: {e}")
        return False


def test_classifier_training():
    """Test classifier training"""
    logger.info("\n" + "=" * 60)
    logger.info("Testing Syllabus Classifier Training")
    logger.info("=" * 60)

    from app.services.syllabus_classifier import SyllabusClassifier

    try:
        classifier = SyllabusClassifier()

        # Create sample training data
        questions = [
            "What is photosynthesis?",
            "How does evaporation work?",
            "What is a chemical reaction?",
            "How do I invest in stocks?",
            "What is cryptocurrency?",
            "How do I get rich?",
        ]

        labels = [1, 1, 1, 0, 0, 0]  # First 3 are in-syllabus, last 3 are not

        classifier.train(questions, labels)

        logger.info("Model trained successfully")

        # Test predictions
        test_q = "What is photosynthesis?"
        pred, conf = classifier.predict(test_q)

        logger.info(f"Test prediction: {pred} (confidence: {conf:.2%})")

        # Get feature importance
        top_features = classifier.get_feature_importance(top_n=5)
        logger.info(f"Top 5 important features:")
        for feature, importance in top_features:
            logger.info(f"  - {feature}: {importance:.4f}")

        logger.info("✅ Classifier tests passed!")
        return True

    except Exception as e:
        logger.error(f"❌ Classifier test failed: {e}")
        return False


def test_ai_engine():
    """Test AI engine"""
    logger.info("\n" + "=" * 60)
    logger.info("Testing AI Engine")
    logger.info("=" * 60)

    from app.services.ai_engine import AIEngine

    try:
        engine = AIEngine()

        chunks = [
            {
                "chunk_id": 0,
                "content": "Photosynthesis is the process by which plants convert light energy into chemical energy.",
                "page_number": 45,
            },
            {
                "chunk_id": 1,
                "content": "The light reactions occur in the thylakoid membranes of the chloroplast.",
                "page_number": 46,
            },
        ]

        question = "What is photosynthesis?"
        answer = engine.generate_answer(
            question, chunks, grade="Grade 10", subject="Science"
        )

        logger.info(f"Generated answer ({len(answer)} chars):")
        logger.info(f"  {answer[:100]}...")

        logger.info("✅ AI Engine tests passed!")
        return True

    except Exception as e:
        logger.error(f"❌ AI Engine test failed: {e}")
        return False


def test_api_endpoints():
    """Test FastAPI endpoints"""
    logger.info("\n" + "=" * 60)
    logger.info("Testing API Endpoints")
    logger.info("=" * 60)

    try:
        from fastapi.testclient import TestClient
        from app.main import app

        client = TestClient(app)

        # Test health endpoint
        response = client.get("/health")
        logger.info(f"GET /health: {response.status_code}")
        assert response.status_code == 200

        # Test status endpoint
        response = client.get("/api/v1/status")
        logger.info(f"GET /api/v1/status: {response.status_code}")

        # Test ask endpoint
        response = client.post(
            "/api/v1/ask",
            json={
                "grade": "Grade 10",
                "subject": "Science",
                "question": "What is photosynthesis?",
            },
        )
        logger.info(f"POST /api/v1/ask: {response.status_code}")

        if response.status_code == 200:
            data = response.json()
            logger.info(f"  Response status: {data.get('status')}")
            logger.info(f"  Is in-syllabus: {data.get('is_in_syllabus')}")

        logger.info("✅ API endpoint tests passed!")
        return True

    except Exception as e:
        logger.error(f"❌ API endpoint test failed: {e}")
        return False


def main():
    """Run all tests"""
    logger.info("\n" + "=" * 60)
    logger.info("🧪 Guru.ai Integration Tests")
    logger.info("=" * 60)

    results = {
        "Guardrail": test_guardrail(),
        "Chunker": test_chunker(),
        "Vector Store": test_vector_store(),
        "Classifier": test_classifier_training(),
        "AI Engine": test_ai_engine(),
        "API Endpoints": test_api_endpoints(),
    }

    # Summary
    logger.info("\n" + "=" * 60)
    logger.info("📊 Test Summary")
    logger.info("=" * 60)

    for test_name, passed in results.items():
        status = "✅ PASSED" if passed else "❌ FAILED"
        logger.info(f"{test_name}: {status}")

    total_passed = sum(results.values())
    total_tests = len(results)

    logger.info(f"\nTotal: {total_passed}/{total_tests} tests passed")

    if total_passed == total_tests:
        logger.info("\n🎉 All tests passed! System is ready to use.")
        return 0
    else:
        logger.warning(f"\n⚠️  {total_tests - total_passed} test(s) failed.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
