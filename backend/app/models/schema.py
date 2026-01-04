"""
Pydantic models for request/response validation
"""
from typing import List, Optional
from pydantic import BaseModel, Field, validator


class AskQuestionRequest(BaseModel):
    """Request model for asking a question"""
    grade: str = Field(..., description="Student grade level (e.g., Grade 10)")
    subject: str = Field(..., description="Subject area (e.g., Mathematics)")
    question: str = Field(..., description="The question to ask", min_length=10, max_length=2000)

    @validator("question")
    def question_not_empty(cls, v):
        if not v.strip():
            raise ValueError("Question cannot be empty")
        return v.strip()


class TextbookChunk(BaseModel):
    """Model for a chunk of textbook content"""
    chunk_id: int
    content: str
    page_number: int
    grade: str
    subject: str
    start_word_index: int
    end_word_index: int


class AskQuestionResponse(BaseModel):
    """Response model for question answering"""
    question: str
    grade: str
    subject: str
    is_in_syllabus: bool
    confidence: float = Field(..., description="Confidence score of syllabus classification (0-1)")
    answer: str
    source_chunks: List[TextbookChunk] = Field(default_factory=list)
    page_references: List[int] = Field(default_factory=list)
    status: str = Field(..., description="Status of the response (success, out_of_syllabus, no_content)")


class HealthCheckResponse(BaseModel):
    """Response model for health check endpoint"""
    status: str
    message: str


class TrainingData(BaseModel):
    """Model for training data"""
    question: str
    label: int = Field(..., description="Binary label: 1=in_syllabus, 0=out_of_syllabus")
    grade: str
    subject: str
