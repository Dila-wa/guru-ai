# Guru.ai Backend - Setup & Quick Start Guide

This guide will help you get the Guru.ai backend running in 5 minutes.

## ⚡ Quick Start (5 Minutes)

### Step 1: Install Dependencies

```bash
cd backend
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install packages
pip install -r requirements.txt
```

### Step 2: Train the Model

```bash
python run.py --train
```

This will:
- Load the sample training data from `data/training/question_labels.csv`
- Train a Random Forest classifier
- Save models to `data/models/`
- Show you the most important features

### Step 3: Start the Server

```bash
python run.py
```

You should see:
```
🚀 Starting Guru.ai Backend Server
Host: 0.0.0.0
Port: 8000

📖 API Documentation:
   Swagger UI: http://localhost:8000/docs
   ReDoc: http://localhost:8000/redoc
```

### Step 4: Test the API

Open a new terminal and run:

```bash
# Health check
curl http://localhost:8000/health

# Ask a question
curl -X POST http://localhost:8000/api/v1/ask \
  -H "Content-Type: application/json" \
  -d '{
    "grade": "Grade 10",
    "subject": "Science",
    "question": "What is photosynthesis?"
  }'
```

Or visit the interactive API docs:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🔧 Advanced Setup

### Using Development Mode with Auto-Reload

```bash
python run.py --reload
```

This will restart the server automatically when you change code.

### Training with Custom Data

1. Prepare your CSV file with columns: `question`, `label`, `grade`, `subject`
2. Replace `data/training/question_labels.csv` with your data
3. Run:

```bash
python train_model.py
```

### Adding Textbook PDFs

1. Place your PDF files in `backend/data/textbooks/raw_pdfs/`
2. The system will extract text from PDFs (sample notebook coming soon)

## 📊 Project Structure Explained

```
backend/
├── app/                          # Main application package
│   ├── main.py                   # FastAPI app initialization
│   ├── config.py                 # Configuration & constants
│   ├── routes/
│   │   └── chat.py               # API endpoints
│   ├── services/
│   │   ├── guardrail.py          # Safety guardrail (uses Random Forest)
│   │   ├── syllabus_classifier.py # Random Forest training
│   │   ├── ai_engine.py          # Answer generation
│   │   ├── vector_store.py       # FAISS semantic search
│   │   ├── chunker.py            # Text chunking
│   │   └── textbook_loader.py    # PDF extraction
│   └── models/
│       └── schema.py             # Request/response schemas
├── data/
│   ├── textbooks/
│   │   └── raw_pdfs/             # Place PDFs here
│   ├── training/
│   │   ├── question_labels.csv   # Training data
│   │   └── models/               # Trained models (auto-created)
├── train_model.py                # Standalone training script
├── run.py                        # Startup script
└── requirements.txt              # Python dependencies
```

## 🧪 Testing the Guardrail

The guardrail Random Forest classifier blocks out-of-syllabus questions:

```python
# In Python REPL or script:
from app.services.guardrail import Guardrail

guardrail = Guardrail()
guardrail.load_model()

# Test in-syllabus
is_in, conf = guardrail.is_in_syllabus("What is photosynthesis?")
print(f"In-syllabus: {is_in}, Confidence: {conf:.2%}")
# Output: In-syllabus: True, Confidence: 92%

# Test out-of-syllabus
is_in, conf = guardrail.is_in_syllabus("How do I become a millionaire?")
print(f"In-syllabus: {is_in}, Confidence: {conf:.2%}")
# Output: In-syllabus: False, Confidence: 85%
```

## 📡 API Endpoints

### Health Check
```bash
GET /health
```

### Ask a Question
```bash
POST /api/v1/ask
Content-Type: application/json

{
  "grade": "Grade 10",
  "subject": "Mathematics",
  "question": "What is the Pythagorean theorem?"
}
```

### Service Status
```bash
GET /api/v1/status
```

## 🎓 Understanding the Guardrail

The Random Forest classifier works like this:

1. **Input**: Student's question (text)
2. **Processing**:
   - Convert text to TF-IDF features (word frequencies + importance)
   - Feed to trained Random Forest model
3. **Output**: 
   - Prediction: 1 = In-syllabus, 0 = Out-of-syllabus
   - Confidence: 0-1 score

**Why Random Forest?**
- ✅ Fast (1-10ms per question)
- ✅ No hallucination (deterministic)
- ✅ Interpretable (shows important words)
- ✅ Robust (handles varied question formats)

## 🚨 Troubleshooting

### "ModuleNotFoundError: No module named 'fastapi'"
```bash
pip install -r requirements.txt
```

### "FileNotFoundError: classifier.pkl not found"
```bash
python run.py --train
# or
python train_model.py
```

### "Port 8000 already in use"
```bash
python run.py --port 8001
```

### Slow performance
- Reduce `FAISS_TOP_K_CHUNKS` in `app/config.py` (currently 5)
- Use fewer Random Forest trees (`RF_N_ESTIMATORS`)
- Check if antivirus is scanning files

## 📚 Key Components

### 1. Guardrail (Random Forest)
Ensures ONLY in-syllabus questions are answered.

**File**: `app/services/guardrail.py`

### 2. AI Engine
Generates answers from textbook chunks.

**File**: `app/services/ai_engine.py`

### 3. Vector Store (FAISS)
Finds relevant textbook sections for questions.

**File**: `app/services/vector_store.py`

### 4. Syllabus Classifier
Trains the Random Forest model.

**File**: `app/services/syllabus_classifier.py`

## 🔑 Configuration

Edit `app/config.py` to customize:

```python
# Model hyperparameters
RF_N_ESTIMATORS = 100          # Number of trees
RF_MAX_DEPTH = 20              # Tree depth

# Text chunking
CHUNK_MIN_WORDS = 300          # Minimum chunk size
CHUNK_MAX_WORDS = 500          # Maximum chunk size

# Classification threshold
SYLLABUS_CONFIDENCE_THRESHOLD = 0.6  # Confidence cutoff
```

## 📈 Improving Accuracy

1. **Add more training data**
   - Goal: 500+ questions per grade-subject combination
   - Balance: 60% in-syllabus, 40% out-of-syllabus

2. **Tune hyperparameters**
   - Adjust `RF_MAX_DEPTH` in `config.py`
   - Modify `SYLLABUS_CONFIDENCE_THRESHOLD`

3. **Add real textbooks**
   - Place PDFs in `data/textbooks/raw_pdfs/`
   - System will automatically chunk and embed them

## 🎯 Next Steps

1. ✅ Get the server running (you're here!)
2. 📝 Add your own training data
3. 📚 Add government textbook PDFs
4. 🚀 Deploy to production (see README.md)

## ❓ Questions?

Check the main [README.md](README.md) for:
- Full API documentation
- Safety mechanisms explained
- Production deployment guide
- Performance benchmarks

---

**Happy learning with Guru.ai! 🎓**
