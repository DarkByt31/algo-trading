# Testing Guide - Phase 5

## Overview

This guide covers all testing approaches for the Trading Backtester application, including unit tests, integration tests, performance tests, and end-to-end tests.

---

## Table of Contents

1. [Quick Start](#quick-start)
2. [End-to-End Testing](#end-to-end-testing)
3. [Backend Unit Testing](#backend-unit-testing)
4. [Integration Testing](#integration-testing)
5. [Frontend Testing](#frontend-testing)
6. [Performance Testing](#performance-testing)
7. [Troubleshooting](#troubleshooting)

---

## Quick Start

### Prerequisites

```bash
# Backend
cd backend
pip install -r requirements.txt
pip install pytest pytest-cov pytest-benchmark pytest-asyncio

# Frontend
cd frontend
npm install
npm install --save-dev vitest @testing-library/react @testing-library/jest-dom
```

### Run All Tests

```bash
# Backend tests
cd backend
pytest tests/ -v --cov=app --cov-report=html

# Frontend tests
cd frontend
npm run test

# E2E tests
bash e2e_test.sh
```

---

## End-to-End Testing

### What It Tests

- Complete workflow from UI submission to results display
- API integration with database
- Real backtest execution
- Results consistency

### Running E2E Tests

```bash
# Make sure backend is running
cd backend
python -m uvicorn app.main:app --reload

# In another terminal
cd /path/to/project
bash e2e_test.sh
```

### E2E Test Output

```
✅ API is running
✅ Found 20 stocks
✅ Found 1 algorithms
✅ Backtest submitted: 123e4567-e89b-12d3-a456-426614174000
✅ Backtest completed
✅ All required fields present
Symbol: TATVA
Initial Capital: ₹50000.0
Final Capital: ₹48257.14
Total Trades: 6
Return: -3.49%
```

### E2E Test Results

Results are saved in `e2e_test_results/` directory:
- `main_result.json` - Primary test results
- `{STOCK}_result.json` - Individual stock results

---

## Backend Unit Testing

### Test Structure

```
backend/tests/
├── test_algorithms.py        # Algorithm logic (50+ tests)
├── test_backtest_engine.py   # Engine execution (30+ tests)
├── test_executor.py          # Trade execution (20+ tests)
├── test_calculator.py        # P&L calculations
├── test_data_fetcher.py      # Data fetching (25+ tests)
├── test_cache.py             # Caching logic (20+ tests)
├── test_database.py          # Database models (20+ tests)
├── test_api_endpoints.py     # API routes (15+ tests)
├── test_integration.py       # Full workflow (NEW - 20+ tests)
└── conftest.py               # Pytest fixtures
```

### Running Backend Tests

```bash
cd backend

# Run all tests
pytest tests/ -v

# Run specific test file
pytest tests/test_algorithms.py -v

# Run specific test
pytest tests/test_algorithms.py::test_mean_reversion_buy_signal -v

# Run with coverage report
pytest tests/ -v --cov=app --cov-report=html

# Run with output capture disabled (see prints)
pytest tests/ -v -s

# Run tests matching pattern
pytest tests/ -k "mean_reversion" -v

# Run tests in specific order
pytest tests/ -v --collect-only
```

### Coverage Report

After running tests with coverage:

```bash
# View HTML coverage report
open htmlcov/index.html  # macOS
xdg-open htmlcov/index.html  # Linux
start htmlcov/index.html  # Windows
```

### Example Test Output

```
tests/test_algorithms.py::test_mean_reversion_buy_signal PASSED [5%]
tests/test_algorithms.py::test_mean_reversion_sell_signal PASSED [10%]
tests/test_backtest_engine.py::test_backtest_execution PASSED [15%]
...
====== 82 passed in 15.23s ======
Coverage: 92%
```

---

## Integration Testing

### What It Tests

Integration tests verify the complete workflow with real data:

```python
# Test complete workflow
test_complete_backtest_workflow():
    1. Submit backtest via API
    2. Wait for execution
    3. Retrieve results
    4. Verify trade log
    5. Validate metrics
```

### Running Integration Tests

```bash
cd backend

# Run only integration tests
pytest tests/test_integration.py -v

# Run integration tests with details
pytest tests/test_integration.py -v -s

# Run specific integration test
pytest tests/test_integration.py::TestIntegration::test_complete_backtest_workflow -v
```

### Integration Test Coverage

- ✅ Complete backtest workflow
- ✅ Multiple stocks
- ✅ Different parameters
- ✅ Different date ranges
- ✅ Different capital amounts
- ✅ Invalid inputs handling
- ✅ API endpoint availability
- ✅ Metrics calculation
- ✅ Trade log consistency

---

## Frontend Testing

### Test Structure (To Be Implemented)

```
frontend/src/__tests__/
├── components/
│   ├── StockSelector.test.tsx
│   ├── AlgorithmSelector.test.tsx
│   ├── ParameterForm.test.tsx
│   ├── ResultsDisplay.test.tsx
│   ├── TradeLog.test.tsx
│   └── ChartContainer.test.tsx
├── hooks/
│   ├── useBacktest.test.ts
│   ├── useResults.test.ts
│   ├── useAlgorithms.test.ts
│   └── useStocks.test.ts
└── integration/
    ├── BacktestPage.test.tsx
    └── ResultsPage.test.tsx
```

### Frontend Test Example

```typescript
import { render, screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { StockSelector } from '../components/StockSelector';

describe('StockSelector', () => {
  it('renders with available stocks', async () => {
    render(<StockSelector value="" onChange={() => {}} />);
    
    await waitFor(() => {
      expect(screen.getByText('TATVA')).toBeInTheDocument();
      expect(screen.getByText('VOLTAS')).toBeInTheDocument();
    });
  });

  it('calls onChange when stock is selected', async () => {
    const onChange = jest.fn();
    render(<StockSelector value="" onChange={onChange} />);
    
    const tatvaOption = await screen.findByText('TATVA');
    await userEvent.click(tatvaOption);
    
    expect(onChange).toHaveBeenCalledWith('TATVA');
  });
});
```

---

## Performance Testing

### Key Metrics

| Metric | Target | Current |
|--------|--------|---------|
| Backtest Execution Time | < 30s | TBD |
| API Response Time (avg) | < 500ms | TBD |
| Database Query Time | < 100ms | TBD |
| Frontend Initial Load | < 3s | TBD |
| Bundle Size (gzipped) | < 500KB | TBD |

### Running Performance Tests

```bash
# Backend performance tests
cd backend
pytest tests/test_integration.py::TestPerformance -v

# Measure backtest execution time
pytest tests/test_integration.py::TestPerformance::test_backtest_execution_time -v

# Load testing (concurrent requests)
pytest tests/test_integration.py::TestPerformance::test_concurrent_requests -v

# Frontend bundle analysis
cd frontend
npm run build:analyze
```

### Performance Test Code

```python
def test_backtest_execution_time():
    """Verify backtest executes within time limit"""
    import time
    
    start = time.time()
    response = client.post("/api/v1/backtest", json={...})
    elapsed = time.time() - start
    
    assert response.status_code == 200
    assert elapsed < 30, f"Took {elapsed:.2f}s (limit: 30s)"
```

---

## Test Scenarios

### Basic Scenarios

✅ Single stock backtest  
✅ Multiple stocks  
✅ Different parameters  
✅ Different date ranges  
✅ Different capital amounts  

### Edge Cases

✅ Empty data range  
✅ Single candle  
✅ No trades executed  
✅ Maximum capital  
✅ Minimum capital  

### Error Scenarios

✅ Invalid stock symbol  
✅ Invalid algorithm  
✅ Date range validation  
✅ Missing required fields  
✅ Database failure  
✅ API timeout  
✅ Concurrent request limits  

### Stress Tests

✅ Large datasets  
✅ Concurrent requests  
✅ Memory usage  
✅ CPU usage  
✅ Database load  

---

## Continuous Integration

### Local Pre-Commit Testing

```bash
#!/bin/bash
# .git/hooks/pre-commit

# Run backend tests
cd backend
pytest tests/ -q || exit 1

# Run frontend tests
cd ../frontend
npm run test:ci || exit 1

echo "✅ All tests passed!"
```

### CI/CD Pipeline (Future)

```yaml
# .github/workflows/test.yml
name: Test
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Backend tests
        run: cd backend && pytest tests/ --cov
      - name: Frontend tests
        run: cd frontend && npm test
      - name: E2E tests
        run: bash e2e_test.sh
```

---

## Debugging Failed Tests

### Backend Test Debugging

```bash
# Run with verbose output
pytest tests/test_file.py -v -s

# Run specific test with print statements
pytest tests/test_file.py::test_name -v -s

# Drop into debugger on failure
pytest tests/test_file.py --pdb

# Show local variables on failure
pytest tests/test_file.py -l

# Show fixture setup/teardown
pytest tests/test_file.py -v --setup-show
```

### Frontend Test Debugging

```bash
# Run tests in watch mode
npm run test:watch

# Debug specific test
npm run test -- StockSelector.test.tsx

# Show coverage for specific file
npm run test:coverage -- StockSelector.test.tsx
```

### Common Issues

**Issue**: Tests fail with "Database locked"  
**Solution**: Clear database before tests, use transactions

**Issue**: "API connection refused"  
**Solution**: Ensure backend is running before tests

**Issue**: Timeout errors in E2E tests  
**Solution**: Increase timeout value in test configuration

---

## Test Report Generation

### Backend Coverage Report

```bash
cd backend
pytest tests/ --cov=app --cov-report=html --cov-report=term

# View report
open htmlcov/index.html
```

### Frontend Coverage Report

```bash
cd frontend
npm run test:coverage

# View report
open coverage/index.html
```

### Test Report Format

```
======================== Test Summary ========================
Total Tests: 150
Passed: 148 (98.7%)
Failed: 2 (1.3%)
Skipped: 0 (0%)
Duration: 45.23s
Coverage: 92%

Failed Tests:
  - test_concurrent_requests (timeout)
  - test_invalid_stock_handling (assertion error)

Coverage by Module:
  - app/core/algorithms: 95%
  - app/core/backtest: 92%
  - app/api: 88%
  - app/db: 90%
```

---

## Troubleshooting

### Database Issues

```bash
# Reset test database
cd backend
rm test.db
pytest tests/conftest.py

# Check database structure
sqlite3 test.db ".tables"
```

### Import Errors

```bash
# Verify Python path
python -c "import app"

# Verify virtual environment
which python

# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

### API Connection Issues

```bash
# Check if backend is running
curl http://localhost:8000/docs

# Check logs
tail -f server.log

# Restart backend
pkill -f "uvicorn"
python -m uvicorn app.main:app --reload
```

### Performance Issues

```bash
# Profile backend
python -m cProfile -s cumtime -m pytest tests/test_integration.py

# Memory profiling
pip install memory-profiler
python -m memory_profiler tests/test_integration.py

# Check database indexes
sqlite3 test.db ".indices"
```

---

## Best Practices

### Writing Tests

1. **Use clear names**: `test_mean_reversion_generates_buy_signal_when_z_score_below_threshold`
2. **One assertion per test** (when possible)
3. **Use fixtures** for common setup
4. **Mock external dependencies**
5. **Test edge cases** explicitly
6. **Keep tests isolated** (no dependencies between tests)

### Running Tests

1. **Run locally before committing**
2. **Run full suite before deployment**
3. **Check coverage regularly**
4. **Keep tests fast** (< 30 seconds total)
5. **Monitor CI/CD pipeline**

### Maintaining Tests

1. **Update tests with code changes**
2. **Remove obsolete tests**
3. **Refactor duplicate test code**
4. **Document complex test logic**
5. **Keep dependencies up to date**

---

## Next Steps

- [ ] Implement frontend component tests
- [ ] Add API load testing
- [ ] Setup CI/CD pipeline
- [ ] Create performance baseline
- [ ] Add real-time monitoring
- [ ] Implement contract testing
- [ ] Add visual regression testing

---

**Last Updated**: January 31, 2026  
**Test Suite Version**: 1.0  
**Coverage Target**: 90%+
