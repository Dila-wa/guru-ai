"""
Chat routes - FastAPI endpoints for question answering
"""
import logging
from fastapi import APIRouter, HTTPException, status
from app.models.schema import AskQuestionRequest, AskQuestionResponse, TextbookChunk
from app.services.guardrail import Guardrail
from app.services.vector_store import VectorStore
from app.services.ai_engine import AIEngine
from app import config

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1", tags=["chat"])

# Initialize services (in production, use dependency injection)
guardrail = Guardrail()
vector_store = VectorStore()
ai_engine = AIEngine()

# Global flag for initialization
_initialized = False


def initialize_services():
    """Initialize all services"""
    global _initialized

    if _initialized:
        return

    try:
        # Load guardrail model
        guardrail.load_model()
        logger.info("Guardrail initialized")

        # Load vector store
        if config.FAISS_INDEX_PATH.exists() and config.EMBEDDINGS_PATH.exists():
            vector_store.load(str(config.FAISS_INDEX_PATH), str(config.EMBEDDINGS_PATH))
            logger.info("Vector store initialized")

        _initialized = True
        logger.info("All services initialized successfully")

    except Exception as e:
        logger.error(f"Failed to initialize services: {e}")
        _initialized = False


@router.post("/ask", response_model=AskQuestionResponse)
async def ask_question(request: AskQuestionRequest) -> AskQuestionResponse:
    """
    Ask a question about the textbook content

    Args:
        request: AskQuestionRequest with grade, subject, and question

    Returns:
        AskQuestionResponse with answer and metadata
    """
    if not _initialized:
        initialize_services()

    try:
        # Validate grade and subject
        if request.grade not in config.SUPPORTED_GRADES:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Unsupported grade. Supported: {config.SUPPORTED_GRADES}",
            )

        if request.subject not in config.SUPPORTED_SUBJECTS:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Unsupported subject. Supported: {config.SUPPORTED_SUBJECTS}",
            )

        logger.info(f"Processing question for {request.grade} {request.subject}")
        logger.debug(f"Question: {request.question[:100]}...")

        # Step 1: Check if question is in syllabus using guardrail
        is_in_syllabus, confidence = guardrail.is_in_syllabus(request.question)

        # Step 2: Retrieve relevant chunks from vector store
        source_chunks = []
        page_references = []

        if is_in_syllabus and not vector_store.is_empty():
            # For MVP, we'll use simple keyword matching instead of embeddings
            # In production, use actual semantic similarity
            chunks = _retrieve_chunks_keyword(request.question, request.grade, request.subject)

            for chunk_dict in chunks:
                chunk = TextbookChunk(**chunk_dict)
                source_chunks.append(chunk)
                if chunk.page_number not in page_references:
                    page_references.append(chunk.page_number)

        # Step 3: Generate answer
        if is_in_syllabus:
            if source_chunks:
                chunks_dicts = [chunk.dict() for chunk in source_chunks]
                answer = ai_engine.generate_answer(
                    request.question, chunks_dicts, request.grade, request.subject
                )
                status_str = "success"
            else:
                answer = config.MSG_NO_CONTENT
                status_str = "no_content"
        else:
            answer = config.MSG_OUT_OF_SYLLABUS
            status_str = "out_of_syllabus"

        # Build response
        response = AskQuestionResponse(
            question=request.question,
            grade=request.grade,
            subject=request.subject,
            is_in_syllabus=is_in_syllabus,
            confidence=confidence,
            answer=answer,
            source_chunks=source_chunks,
            page_references=sorted(page_references),
            status=status_str,
        )

        logger.info(f"Question processed | Status: {status_str} | Confidence: {confidence:.3f}")

        return response

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error processing question: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=config.MSG_PROCESSING_ERROR,
        )


def _retrieve_chunks_keyword(question: str, grade: str, subject: str) -> list:
    """
    Retrieve chunks using keyword matching (MVP approach)

    In production, this would use semantic search with embeddings

    Args:
        question: Question text
        grade: Grade level
        subject: Subject name

    Returns:
        List of chunk dictionaries
    """
    # For MVP, return empty list
    # In production, implement actual retrieval using FAISS
    logger.debug(
        f"Retrieving chunks for: {question[:50]}... | "
        f"Grade: {grade} | Subject: {subject}"
    )

    return []


@router.get("/health")
async def health_check() -> dict:
    """Health check endpoint"""
    try:
        initialize_services()

        return {
            "status": "healthy",
            "message": "Guru.ai backend is running",
            "services": {
                "guardrail": "ready" if _initialized else "not_ready",
                "vector_store": "ready" if not vector_store.is_empty() else "empty",
                "ai_engine": "ready",
            },
        }
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Service not available",
        )


@router.get("/status")
async def status_endpoint() -> dict:
    """Get service status and statistics"""
    initialize_services()

    return {
        "status": "running",
        "version": config.API_VERSION,
        "services": {
            "guardrail": {
                "loaded": _initialized,
            },
            "vector_store": vector_store.get_stats(),
            "ai_engine": ai_engine.get_stats(),
        },
    }
