# 🚀 Local Setup & Testing Guide

## Prerequisites
- **Node.js**: v18+ (tested with v24.13.0)
- **npm**: v8+ (tested with npm 11.6.2)
- **Python**: 3.8+ (system Python is fine)
- **pip**: Python package manager
- **Git**: For version control

---

## Project Structure

```
Algo trading/
├── frontend/          # React + TypeScript + Vite (Port 3000)
├── backend/           # FastAPI + SQLAlchemy (Port 8000)
├── .gitignore         # Git ignore file
├── LOCAL_SETUP_GUIDE.md
└── README.md
```

---

## ⚡ Quick Start (Full Stack - 3 Steps)

### Step 1: Backend Setup

```bash
cd backend

# Install dependencies (one time only)
pip install -r requirements.txt

# Start the backend server
python3 -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

✅ **Backend ready on**: `http://127.0.0.1:8000`
- API Docs (Swagger UI): `http://127.0.0.1:8000/docs`
- ReDoc Docs: `http://127.0.0.1:8000/redoc`

**📝 Note:** 
- Uses SQLite for local development (no MySQL needed)
- `.env` file auto-configures database
- Server auto-reloads on code changes

---

### Step 2: Frontend Setup (New Terminal)

```bash
cd frontend

# Install dependencies (one time only)
npm install --legacy-peer-deps

# Start development server
npm run dev
```

✅ **Frontend ready on**: `http://localhost:3000`

**Auto Features:**
- Hot reload on file changes (Vite)
- CSS + TypeScript compilation
- Dev error overlay

---

### Step 3: Open in Browser

👉 **Go to**: **`http://localhost:3000`**

You should see the Trading Backtester UI with:
- 📊 Stock selector
- ⚙️ Algorithm selection
- 📅 Date range picker
- 📈 Results display
- 📋 Trade log

---

## 🧪 Running Tests

### Frontend Tests (18 tests - All Passing ✅)

```bash
cd frontend

# Run all tests once
npm test -- --run

# Run tests with coverage report
npm test -- --coverage

# Watch mode (re-run on changes)
npm test
```

Coverage reports in `frontend/coverage/` directory.

---

### Backend Integration Tests

```bash
cd backend

# Run all tests
pytest tests/test_integration.py -v

# Run specific test
pytest tests/test_integration.py::TestAPIEndpoints::test_get_stocks -v

# Run with coverage
pytest tests/ --cov=. --cov-report=html --cov-report=lcov
```

---

### E2E Tests (Full Stack)

Ensure both backend and frontend are running, then:

```bash
cd "Algo trading"
bash e2e_test.sh
```

---

## 🛠️ Common Testing Scenarios

### 1. Test Stock Selection
1. Open `http://localhost:3000`
2. Click "Select Stock" dropdown
3. Verify stocks load (TATVA, VOLTAS, RELIANCE, etc.)
4. Select a stock
5. Confirm selection shows in dropdown

### 2. Test Backtest Configuration
1. Select a stock
2. Fill backtest form:
   - **Start Date**: 2024-01-01
   - **End Date**: 2024-12-31
   - **Initial Capital**: ₹50,000
   - **Algorithm**: Select any algorithm
3. Click "Submit Backtest"
4. Check browser console (F12 → Console) for API calls

### 3. Test API Integration
1. Open browser DevTools: **F12** or **Ctrl+Shift+I**
2. Go to **Network** tab
3. Perform actions (select stock, submit backtest)
4. View requests/responses:
   - All requests to `http://127.0.0.1:8000`
   - Check response status codes (200, 400, etc.)

### 4. Test Results Display
1. After backtest submission
2. Results tab should show:
   - Final Capital
   - Total P&L (Profit/Loss)
   - Win Rate %
   - Max Drawdown
3. Trade Log tab should show individual trades:
   - Entry/Exit dates
   - Prices
   - Quantity
   - Profit/Loss per trade

---

## 🔍 Debugging

### Frontend Debugging
```bash
cd frontend

# Start with source maps
npm run dev

# Open DevTools (F12) and check:
# ✓ Console tab - for errors
# ✓ Network tab - for API calls
# ✓ Sources tab - for breakpoints
# ✓ React DevTools browser extension - for component tree
```

### Backend Debugging
```bash
cd backend

# Check logs in terminal where uvicorn is running
# Look for:
# ✓ ERROR: - indicates failures
# ✓ INFO: - request/response logs
# ✓ WARNING: - potential issues

# View API docs with test endpoints
# Open: http://127.0.0.1:8000/docs
# Test endpoints interactively
```

### Check Port Conflicts
```bash
# If port 8000 (backend) is in use:
lsof -i :8000

# If port 3000 (frontend) is in use:
lsof -i :3000

# Kill process using port:
kill -9 <PID>
```

---

## 🚨 Troubleshooting

### ❌ Issue: `venv/bin/activate: No such file or directory`
**✅ Solution:**
- Skip venv! Use system Python
- Just run: `pip install -r requirements.txt`
- Then: `python3 -m uvicorn app.main:app --reload`

### ❌ Issue: Backend port 8000 already in use
**✅ Solution:**
```bash
# Find and kill existing process
lsof -i :8000
kill -9 <PID>

# Start backend again
python3 -m uvicorn app.main:app --reload --port 8000
```

### ❌ Issue: Frontend port 3000 already in use
**✅ Solution:**
```bash
# Find and kill existing process
lsof -i :3000
kill -9 <PID>

# Start frontend again
npm run dev
```

### ❌ Issue: `npm: command not found`
**✅ Solution:**
Ensure Node.js is installed:
```bash
node --version  # Should show v18.0.0 or higher
npm --version   # Should show 8.0.0 or higher
```
If not installed, download from: https://nodejs.org/

### ❌ Issue: `python3: command not found`
**✅ Solution:**
Ensure Python is installed:
```bash
python3 --version  # Should show 3.8+
```

### ❌ Issue: Module not found errors in frontend
**✅ Solution:**
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install --legacy-peer-deps
npm run dev
```

### ❌ Issue: `pip: command not found`
**✅ Solution:**
```bash
python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt
```

---

## 📊 API Endpoints Quick Reference

| Method | Endpoint | Purpose |
|--------|----------|---------|
| GET | `/api/stocks` | Get available stocks |
| GET | `/api/algorithms` | Get available algorithms |
| POST | `/api/backtest/submit` | Submit backtest job |
| GET | `/api/backtest/results/{job_id}` | Get backtest results |
| GET | `/api/backtest/trades/{job_id}` | Get trade log |
| GET | `/health` | Health check |
| GET | `/docs` | Interactive Swagger UI |

**Full API Documentation**: Visit `http://127.0.0.1:8000/docs` while backend is running

---

## 📈 Test Coverage Status

✅ **Frontend**: 18/18 tests passing (100%)
- App component rendering
- Stock selector functionality
- Backtest configuration form
- Results display component
- Trade log component

✅ **Backend**: 14+ integration tests (API schema, error handling, workflows)

✅ **Total**: 30+ automated tests covering key functionality

---

## 🚀 Running with Different Configurations

### Backend on Different Port
```bash
cd backend
python3 -m uvicorn app.main:app --reload --port 8001
```
Then update frontend API in `src/services/api.ts` to `http://127.0.0.1:8001`

### Frontend Production Build
```bash
cd frontend
npm run build      # Creates optimized build in dist/
npm run preview    # Test production build (port 4173)
```

### Backend Performance Testing
```bash
cd backend
pytest tests/ --durations=10  # Show slowest tests
```

---

## 💡 Pro Tips

1. **Keep servers running**: Open 2 terminals, one for backend, one for frontend
2. **Hot reload**: Changes save instantly during development
3. **API testing**: Use Swagger UI at `http://127.0.0.1:8000/docs` to test endpoints
4. **Browser DevTools**: F12 to inspect network requests and debug
5. **Watch logs**: Terminal logs show real-time errors and SQL queries
6. **Database**: SQLite file is at `backend/test.db` - can delete to reset

---

## ✅ Verification Checklist

Before considering setup complete:

- [ ] Backend running on `http://127.0.0.1:8000`
- [ ] Frontend running on `http://localhost:3000`
- [ ] Can access Swagger UI at `http://127.0.0.1:8000/docs`
- [ ] Frontend loads without console errors (F12)
- [ ] Stock selector dropdown shows stocks
- [ ] Can submit a backtest
- [ ] All 18 frontend tests pass: `npm test -- --run`
- [ ] API responds to requests in Network tab

---

## 🎓 Next Steps

1. **Explore the UI**: Play around with stock selection, backtest submission
2. **Test the API**: Use Swagger UI to test endpoints
3. **Review code**: Check `/frontend/src` and `/backend/app` for implementation
4. **Run tests**: Execute test suite to verify functionality
5. **Modify code**: Make changes and see hot reload in action

---

## 📞 Need Help?

Check log output in terminals where services are running for detailed error messages.

**Key files**:
- Backend config: `backend/.env` (database URL)
- Frontend config: `frontend/src/services/api.ts` (API endpoint)
- Backend main: `backend/app/main.py` (FastAPI setup)
- Frontend main: `frontend/src/main.tsx` (React setup)

