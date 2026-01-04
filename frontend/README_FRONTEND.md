# Frontend - Guru.ai Educational AI Tutor

Modern React frontend for the Guru.ai platform with an interactive chat interface for students.

## Quick Features

✨ **Interactive Chat** - Ask questions and get instant answers  
🎓 **Grade Selection** - Customize for Grade 9-12  
📚 **Subject Support** - Mathematics, Science, English, History, Chemistry  
💬 **Chat History** - Track all questions and answers  
🎨 **Beautiful UI** - Modern, responsive design  

## Files Structure

```
frontend/
├── public/
│   └── index.html           # HTML template
├── src/
│   ├── components/
│   │   └── ChatInterface.js # Main chat component
│   ├── services/
│   │   └── api.js           # Backend API calls
│   ├── styles/
│   │   └── ChatInterface.css # Component styling
│   ├── App.js               # Main app component
│   ├── App.css
│   ├── index.js             # React entry point
│   └── index.css
├── package.json             # Dependencies
├── SETUP.md                 # Setup instructions
└── README.md                # Full documentation
```

## Quick Start

1. **Install dependencies:**
   ```bash
   cd frontend
   npm install
   ```

2. **Start development server:**
   ```bash
   npm start
   ```

3. **Open browser:**
   - Visit `http://localhost:3000`

## Configuration

Set backend API URL in `.env`:
```
REACT_APP_API_URL=http://localhost:8000
```

## Available Scripts

- `npm start` - Run development server
- `npm run build` - Create production build
- `npm test` - Run tests

## Requirements

- Node.js v14+
- npm v6+
- Backend running on port 8000

## Components

### ChatInterface
Main component handling:
- Grade/subject selection
- Question input
- Answer display
- Chat history management
- API communication

### API Service
Manages backend communication:
- Health checks
- Question submission
- Status updates

---

See [SETUP.md](SETUP.md) for detailed setup instructions.
