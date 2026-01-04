# Guru.ai Frontend Setup Guide

## Installation

1. Install Node.js (v14 or higher) from https://nodejs.org/

2. Navigate to the frontend directory:
```bash
cd frontend
```

3. Install dependencies:
```bash
npm install
```

## Running the Application

### Development Mode
```bash
npm start
```
- Opens at `http://localhost:3000`
- Auto-reloads on file changes

### Production Build
```bash
npm run build
```
- Creates optimized build in `build/` folder
- Ready for deployment

## Configuration

Create `.env` file to customize:
```
REACT_APP_API_URL=http://localhost:8000
```

## Requirements

- Node.js v14+
- npm v6+
- Backend running at http://localhost:8000

## Troubleshooting

### "npm: command not found"
- Install Node.js from https://nodejs.org/

### "Cannot find module 'react'"
```bash
npm install
```

### Backend connection error
- Verify backend is running: `curl http://localhost:8000/health`
- Check `REACT_APP_API_URL` in `.env`
- Check CORS settings in backend

## Next Steps

1. ✅ Setup complete!
2. Run the backend first: `python run.py` (in backend folder)
3. Run the frontend: `npm start` (in frontend folder)
4. Open http://localhost:3000 in your browser
