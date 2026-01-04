# Guru.ai Frontend

A modern React-based frontend for the Guru.ai educational AI tutor platform.

## Quick Start

### 1. Install Dependencies
```bash
cd frontend
npm install
```

### 2. Configure API URL (Optional)
Create a `.env` file in the frontend directory:
```
REACT_APP_API_URL=http://localhost:8000
```

### 3. Start Development Server
```bash
npm start
```

The app will open at `http://localhost:3000`

## Features

- 🎓 Interactive chat interface
- 📚 Grade and subject selection
- 🚀 Real-time question answering
- 💬 Chat history tracking
- 🎨 Modern, responsive design

## Build for Production

```bash
npm run build
```

This creates an optimized production build in the `build/` folder.

## Project Structure

```
src/
├── components/
│   └── ChatInterface.js    # Main chat component
├── services/
│   └── api.js              # API communication
├── styles/
│   └── ChatInterface.css   # Component styles
├── App.js                  # Main app component
├── App.css                 # App styles
├── index.js                # Entry point
└── index.css               # Global styles

public/
└── index.html              # HTML template
```

## API Integration

The frontend communicates with the backend API at `http://localhost:8000`.

### Endpoints Used:
- `GET /health` - Health check
- `POST /api/v1/ask` - Submit a question
- `GET /api/v1/status` - Service status

## Customization

### Grades and Subjects
Edit the `grades` and `subjects` arrays in [src/components/ChatInterface.js](src/components/ChatInterface.js)

### Styling
Modify [src/styles/ChatInterface.css](src/styles/ChatInterface.css) for custom themes

## Troubleshooting

### "Failed to get answer"
- Ensure the backend is running on `http://localhost:8000`
- Check network tab in browser DevTools
- Verify `REACT_APP_API_URL` environment variable

### Port 3000 already in use
```bash
npm start -- --port 3001
```

---

**Happy learning with Guru.ai! 🎓**
