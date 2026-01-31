# Local Setup & Testing Guide

## Prerequisites
- **Node.js**: v18+ (currently testing with v24.13.0)
- **npm**: v8+ (currently testing with npm 11.6.2)
- **Python**: 3.8+
- **pip**: Package manager for Python
- **Git**: For version control

---

## Project Structure

```
Algo trading/
├── frontend/          # React + TypeScript + Vite (Port 5173)
├── backend/           # FastAPI (Port 8000)
├── .gitignore         # Git ignore file
├── LOCAL_SETUP_GUIDE.md
└── README.md
```

---

## Quick Start (Full Stack)

### 1. Clone & Navigate to Project

```bash
cd ~/projects/"Algo trading"
```

### 2. Backend Setup

```bash
cd backend

# Create Python virtual environment
python -m venv venv

# Activate virtual environment
# On Linux/Mac:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Start the backend server
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

**Backend runs on**: `http://localhost:8000`
**API Docs**: `http://localhost:8000/docs` (Swagger UI)
**Alternative Docs**: `http://localhost:8000/redoc` (ReDoc)

### 3. Frontend Setup (New Terminal)

```bash
cd frontend

# Install dependencies
npm install --legacy-peer-deps

# Start development server
npm run dev
```

**Frontend runs on**: `http://localhost:5173`

### 4. Open in Browser

Navigate to: **`http://localhost:5173`**

---

## Running Tests Locally

### Frontend Tests

```bash
cd frontend

# Run all tests
npm test -- --run

# Run tests with coverage report
npm test -- --coverage

# Run tests in watch mode (auto-rerun on changes)
npm test
```

**Coverage reports will be generated in**: `frontend/coverage/`

### Backend Integration Tests

```bash
cd backend

# Activate virtual environment first
source venv/bin/activate

# Run all integration tests
pytest tests/test_integration.py -v

# Run specific test
pytest tests/test_integration.py::TestAPIEndpoints::test_get_stocks -v

# Run with coverage
pytest tests/ --cov=. --cov-report=html --cov-report=lcov
```

### E2E Tests (Full Stack)

Ensure both backend and frontend are running, then:

```bash
cd projects/"Algo trading"
bash e2e_test.sh
```

---

## Development Workflow

### Start Both Services at Once (Using Multiple Terminals)

**Terminal 1 - Backend:**
```bash
cd backend
source venv/bin/activate
python -m uvicorn main:app --reload
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
```

**Terminal 3 - Tests (Optional):**
```bash
cd frontend
npm test
```

### Watch Mode for Development

- **Frontend**: Automatically reloads on file changes (Vite hot reload)
- **Backend**: Automatically reloads on file changes (`--reload` flag)
- **Tests**: Run `npm test` without `--run` flag for watch mode

---

## Common Testing Scenarios

### 1. Test Stock Selection
1. Open `http://localhost:5173`
2. Stock dropdown should load available stocks
3. Select a stock (e.g., TATVA, VOLTAS)
4. Verify onChange handler fires

### 2. Test Backtest Configuration
1. Fill in:
   - Start Date: `2024-01-01`
   - End Date: `2024-12-31`
   - Initial Capital: `50000`
2. Select an algorithm
3. Click "Submit Backtest"
4. Check browser console for API calls

### 3. Test API Integration
1. Open browser DevTools: `F12` or `Ctrl+Shift+I`
2. Go to Network tab
3. Perform actions (select stock, submit backtest)
4. View requests/responses to backend

### 4. Test Results Display
1. After backtest submission
2. Results tab should show:
   - Final Capital
   - Total P&L
   - Win Rate
   - Max Drawdown
3. Trade Log should display individual trades

---

## Debugging Tips

### Frontend Debugging
```bash
cd frontend

# Start with source maps for better debugging
npm run dev

# Open DevTools (F12) and check:
# - Console for errors
# - Network for API calls
# - React DevTools (browser extension)
```

### Backend Debugging
```bash
cd backend

# View API docs with test endpoints
# Open: http://localhost:8000/docs

# Check logs in terminal where uvicorn is running
# Look for:
# - ERROR: indicates failures
# - INFO: request/response logs
```

### Check Port Conflicts
```bash
# If port 8000 (backend) is in use:
lsof -i :8000

# If port 5173 (frontend) is in use:
lsof -i :5173

# Kill process using port:
kill -9 <PID>
```

---

## Running with Different Configurations

### Backend with Specific Port
```bash
cd backend
python -m uvicorn main:app --reload --port 8001
```
Then update frontend API endpoint in `src/services/api.ts`

### Frontend Production Build
```bash
cd frontend
npm run build
npm run preview
```
Preview runs on: `http://localhost:4173`

---

## Test Coverage Reports

After running tests with coverage:

### Frontend
```bash
cd frontend
npm test -- --coverage

# Open coverage report
open coverage/index.html  # Mac
xdg-open coverage/index.html  # Linux
start coverage/index.html  # Windows
```

### Backend
```bash
cd backend
pytest tests/ --cov=. --cov-report=html

# Open coverage report
open htmlcov/index.html  # Mac
xdg-open htmlcov/index.html  # Linux
start htmlcov/index.html  # Windows
```

---

## Troubleshooting

### Issue: `Module not found` errors in frontend
**Solution:**
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install --legacy-peer-deps
npm run dev
```

### Issue: Backend port already in use
**Solution:**
```bash
# Find and kill process using port 8000
lsof -i :8000
kill -9 <PID>
python -m uvicorn main:app --reload --port 8000
```

### Issue: CORS errors when fetching from frontend
**Solution:** Backend should allow frontend origin. Check `main.py`:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Issue: Database connection errors
**Solution:**
```bash
# Check if database exists
ls -la backend/*.db

# If missing, run migrations or reset:
cd backend
python -c "from main import app, engine; Base.metadata.create_all(bind=engine)"
```

### Issue: Python virtual environment not activating
**Solution:**
```bash
# Ensure you're using the correct activation script
# Linux/Mac:
source venv/bin/activate

# Check with:
which python
python --version
```

---

## API Endpoints Quick Reference

| Method | Endpoint | Purpose |
|--------|----------|---------|
| GET | `/api/stocks` | Get available stocks |
| GET | `/api/algorithms` | Get available algorithms |
| POST | `/api/backtest/submit` | Submit backtest job |
| GET | `/api/backtest/results/{job_id}` | Get backtest results |
| GET | `/api/backtest/trades/{job_id}` | Get trade log |
| GET | `/health` | Health check |

**Full API Documentation**: `http://localhost:8000/docs`

---

## Performance Tips

1. **Frontend**: Use React DevTools to check for unnecessary re-renders
2. **Backend**: Use `/metrics` endpoint to check request latency
3. **Tests**: Run specific test file instead of full suite when debugging:
   ```bash
   npm test -- src/components/StockSelector.test.tsx --run
   ```

---

## Next Steps

1. **Run both services** following "Quick Start" above
2. **Open browser** at `http://localhost:5173`
3. **Test basic workflow**:
   - Select stock → Select algorithm → Configure dates → Submit → View results
4. **Check tests** pass locally:
   ```bash
   npm test -- --run  # Frontend
   pytest tests/  # Backend
   ```
5. **Review API docs** at `http://localhost:8000/docs`

---

## Need Help?

Check log output in terminals where services are running for detailed error messages.
