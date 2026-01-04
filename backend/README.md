# Guru.ai - Closed-Syllabus AI Backend

A production-ready MVP backend for an education AI platform providing safe, in-syllabus answers to Sri Lankan students.

## 🎯 Project Vision

**Guru.ai** is a closed-syllabus AI system designed for Sri Lankan students (Grades 6-13) that:

- ✅ **Only answers in-syllabus questions** using government textbook content
- ✅ **Refuses out-of-syllabus questions** safely and respectfully
- ✅ **Never hallucidates** - all answers grounded in textbook content
- ✅ **Provides page references** so students can verify sources
- ✅ **Supports multiple subjects** (Mathematics, Science, English, History, Geography, etc.)

## 🛡️ Safety-First Architecture

The core innovation is the **Random Forest Guardrail** - a machine learning classifier that:

1. **Checks every question** against trained in-syllabus vs out-of-syllabus patterns
2. **Blocks out-of-syllabus questions** before they reach the LLM
3. **Returns confidence scores** so the API can handle edge cases
4. **Uses TF-IDF vectorization** for robust text classification
5. **Prevents hallucination** by refusing to answer questions with no textbook content

### Why Random Forest?

- ✅ Interpretable (shows feature importance)
- ✅ Fast inference (sub-millisecond predictions)
- ✅ No hallucination risk
- ✅ Production-proven for binary classification
- ✅ Works well with limited training data

## 📊 System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    FastAPI Application                       │
│                      /api/v1/ask                             │
└────────────────────────┬────────────────────────────────────┘
                         │
          ┌──────────────┼──────────────┐
          │              │              │
          ▼              ▼              ▼
    ┌──────────┐   ┌──────────┐   ┌──────────┐
    │Guardrail │   │  Vector  │   │   AI     │
    │ (RF ML)  │   │  Store   │   │  Engine  │
    │          │   │  (FAISS) │   │          │
    └──────────┘   └──────────┘   └──────────┘
          │              │              │
          ▼              ▼              ▼
    TF-IDF +    Embeddings +    Textbook
    Random     Semantic Search   Templates
    Forest
```

## 🏗️ Project Structure

```
backend/
├── app/
│   ├── __init__.py                 # Package initialization
│   ├── main.py                     # FastAPI application
│   ├── config.py                   # Configuration & constants
│   ├── routes/
│   │   ├── __init__.py
│   │   └── chat.py                 # Chat endpoints
│   ├── services/
│   │   ├── __init__.py
│   │   ├── textbook_loader.py      # PDF extraction (pdfplumber)
│   │   ├── chunker.py              # Text chunking (300-500 words)
│   │   ├── vector_store.py         # FAISS index & embeddings
│   │   ├── syllabus_classifier.py  # Random Forest classifier
│   │   ├── guardrail.py            # Safety guardrail
│   │   └── ai_engine.py            # Answer generation
│   └── models/
│       ├── __init__.py
│       └── schema.py               # Pydantic models
├── data/
│   ├── textbooks/
│   │   └── raw_pdfs/               # Place your textbook PDFs here
│   └── training/
│       ├── models/                 # Trained models (created at runtime)
│       └── question_labels.csv     # Training data (26 samples included)
├── requirements.txt
└── README.md
```

## 🔧 Tech Stack

| Component | Technology | Purpose |
|-----------|-----------|---------|
| **Web Framework** | FastAPI + Uvicorn | REST API server |
| **ML Classification** | Scikit-learn Random Forest | In-syllabus detection |
| **Text Vectorization** | TF-IDF | Convert text to features |
| **Vector Search** | FAISS | Semantic similarity search |
| **PDF Processing** | pdfplumber | Extract text from PDFs |
| **Embeddings** | Sentence-transformers | Semantic embeddings |
| **Data Processing** | Pandas | Training data handling |
| **Model Persistence** | joblib | Save/load models |

## 📦 Installation

### Prerequisites
- Python 3.12+
- Windows/Linux/macOS

### Setup

1. **Clone and navigate to project:**
```bash
cd backend
```

2. **Create virtual environment:**
```bash
python -m venv venv
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Download NLTK data (for text processing):**
```python
python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords')"
```

## 🚀 Quick Start

### 1. Train the Guardrail Model

```python
from app.services.syllabus_classifier import SyllabusClassifier
from app import config
import pandas as pd

# Load training data
df = pd.read_csv("data/training/question_labels.csv")

# Initialize and train classifier
classifier = SyllabusClassifier()
classifier.train(df['question'].tolist(), df['label'].tolist())

# Save model
config.MODELS_DIR.mkdir(exist_ok=True)
classifier.save(
    str(config.CLASSIFIER_MODEL_PATH),
    str(config.VECTORIZER_MODEL_PATH)
)

print("✅ Guardrail model trained and saved!")
```

### 2. Start the Backend Server

```bash
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at: `http://localhost:8000`

### 3. Test the API

```bash
# Health check
curl http://localhost:8000/health

# Ask a question
curl -X POST http://localhost:8000/api/v1/ask \
  -H "Content-Type: application/json" \
  -d '{
    "grade": "Grade 10",
    "subject": "Mathematics",
    "question": "What is the Pythagorean theorem?"
  }'
```

### 4. Interactive API Docs

Visit `http://localhost:8000/docs` for interactive Swagger UI

## 📚 API Reference

### Endpoint: POST /api/v1/ask

Ask a question about textbook content.

**Request:**
```json
{
  "grade": "Grade 10",
  "subject": "Mathematics",
  "question": "What is the formula for the area of a circle?"
}
```

**Response (In-Syllabus):**
```json
{
  "question": "What is the formula for the area of a circle?",
  "grade": "Grade 10",
  "subject": "Mathematics",
  "is_in_syllabus": true,
  "confidence": 0.95,
  "answer": "Based on the Grade 10 Mathematics textbook content:\n\n[Page 45]:\nThe area of a circle is calculated using the formula A = πr², where r is the radius...",
  "source_chunks": [
    {
      "chunk_id": 0,
      "content": "The area of a circle is calculated using the formula A = πr²...",
      "page_number": 45,
      "grade": "Grade 10",
      "subject": "Mathematics"
    }
  ],
  "page_references": [45],
  "status": "success"
}
```

**Response (Out-of-Syllabus):**
```json
{
  "question": "How do I become a professional footballer?",
  "grade": "Grade 10",
  "subject": "Mathematics",
  "is_in_syllabus": false,
  "confidence": 0.88,
  "answer": "This question is not covered in your selected textbook.",
  "source_chunks": [],
  "page_references": [],
  "status": "out_of_syllabus"
}
```

### Supported Grades
- Grade 6, 7, 8, 9, 10, 11, 12, 13

### Supported Subjects
- Mathematics
- Science
- English
- Sinhala
- Tamil
- History
- Civics
- Geography

## 🔐 Safety Features

### 1. **Random Forest Guardrail**
- Classifies questions as in-syllabus (1) or out-of-syllabus (0)
- Blocks out-of-syllabus before generating answers
- Returns confidence scores for every decision

### 2. **Textbook-Only Grounding**
- Only uses content from uploaded government textbooks
- Retrieves relevant chunks using FAISS semantic search
- Returns page references for verification

### 3. **Refusal Responses**
- Out-of-syllabus: *"This question is not covered in your selected textbook."*
- No content: *"No relevant content found in the textbook for this question."*
- Error: *"An error occurred while processing your question. Please try again."*

## 🔄 Processing Pipeline

```
Question Input
    ↓
[1] Guardrail Check (Random Forest)
    ├─ In-syllabus? → Continue
    └─ Out-of-syllabus? → Return refusal
    ↓
[2] Content Retrieval (FAISS)
    ├─ Find relevant chunks
    └─ Extract page numbers
    ↓
[3] Answer Generation (AI Engine)
    ├─ Combine chunks into context
    ├─ Generate answer from context
    └─ Validate grounding
    ↓
[4] Response Building
    ├─ Compile answer + metadata
    ├─ Add page references
    └─ Return to client
```

## 📊 Training Data Format

The training data CSV should have this format:

```csv
question,label,grade,subject
"What is photosynthesis?",1,Grade 10,Science
"How do I invest in Bitcoin?",0,Grade 10,Economics
```

- **label**: 1 = in-syllabus, 0 = out-of-syllabus
- Minimum recommended: 100 samples per grade-subject combination
- Provided sample: 26 questions (for MVP testing)

## 🧪 Testing

### Unit Test Example

```python
from app.services.guardrail import Guardrail

guardrail = Guardrail()
guardrail.load_model()

# Test in-syllabus question
is_in, conf = guardrail.is_in_syllabus("What is photosynthesis?")
assert is_in == True
assert conf > 0.5

# Test out-of-syllabus question
is_in, conf = guardrail.is_in_syllabus("How do I become a millionaire?")
assert is_in == False
```

## 🚀 Production Deployment

### Before Going Live:

1. **Collect more training data**
   - Minimum 500-1000 questions per grade-subject
   - Include diverse question types
   - Balance in-syllabus vs out-of-syllabus (60:40 ratio recommended)

2. **Add real textbooks**
   - Place PDF files in `data/textbooks/raw_pdfs/`
   - Chunk and embed all textbook content
   - Build FAISS index from textbook embeddings

3. **Integrate real LLM**
   - Replace template-based generation in `ai_engine.py`
   - Use API (OpenAI, Anthropic) or local model (Llama, Mistral)
   - Add response validation and fact-checking

4. **Set up monitoring**
   - Log all questions and answers
   - Track guardrail rejection rate
   - Monitor LLM inference latency
   - Alert on hallucination detection

5. **Configure environment**
   - Set appropriate CORS origins
   - Use environment variables for API keys
   - Enable rate limiting
   - Add authentication/authorization

### Docker Deployment

```dockerfile
FROM python:3.12-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## 📈 Performance Metrics

| Metric | Target | Notes |
|--------|--------|-------|
| Guardrail Latency | <10ms | TF-IDF + Random Forest |
| Vector Search Latency | <50ms | FAISS on CPU |
| LLM Generation Latency | <2s | Depends on model |
| Total E2E Latency | <3s | Entire pipeline |
| Guardrail Accuracy | >90% | On test set |
| False Negative Rate | <5% | Missing out-of-syllabus |
| False Positive Rate | <10% | Blocking valid questions |

## 🤝 Contributing

1. Follow PEP 8 style guide
2. Add type hints to all functions
3. Write docstrings for all modules
4. Test locally before committing
5. Use meaningful commit messages

## 📝 License

MIT License - See LICENSE file for details

## 🆘 Troubleshooting

### Issue: "Model files not found"
```
Solution: Train the guardrail model first (see "Train the Guardrail Model" section)
```

### Issue: FAISS import error
```
Solution: pip install faiss-cpu (or faiss-gpu for NVIDIA GPU)
```

### Issue: pdfplumber OCR issues
```
Solution: Ensure PDFs have selectable text (not scanned images)
         Use PDF optimization tools if needed
```

### Issue: Slow inference
```
Solution: Use batch processing for multiple questions
         Consider GPU acceleration for embeddings
         Reduce FAISS_TOP_K_CHUNKS in config.py
```

## 📞 Support

For issues, questions, or contributions, please create an issue in the repository.

---

**Built with ❤️ for Sri Lankan students | Guru.ai 2025**
