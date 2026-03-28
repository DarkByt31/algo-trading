# Backend Tests

Test suite for the trading backtester backend.

## Running Tests

### All Tests
```bash
pytest tests/ -v
```

### Specific Test File
```bash
pytest tests/test_algorithms.py -v
```

### With Coverage
```bash
pytest tests/ --cov=app --cov-report=html
```

### Run Single Test
```bash
pytest tests/test_algorithms.py::TestMeanReversionAlgorithm::test_initialization_valid_params -v
```

## Test Structure

### `test_algorithms.py`
Tests for Mean Reversion Algorithm:
- Parameter validation (valid, missing, invalid ranges)
- Signal generation
- DataFrame column validation
- Z-score calculation
- String representation

### `test_cache.py`
Tests for In-Memory Data Cache:
- Cache initialization
- Get/set operations
- Cache expiry
- Cache key generation
- Cache statistics
- Data isolation (separate symbols/dates)

### `test_registry.py`
Tests for Algorithm Registry:
- Algorithm retrieval
- List algorithms
- Register new algorithms
- Error handling for non-existent algorithms

### `test_validator.py`
Tests for Parameter Validation:
- Date range validation
- Capital validation
- Brokerage fee validation
- Boundary conditions

### `test_fetcher.py`
Tests for Mock Data Fetcher:
- Data generation
- Required columns
- Date filtering
- Market hours filtering
- Weekend filtering
- Data sorting
- Realistic price relationships

### `test_database.py`
Tests for Database Models:
- Configuration
- Connection
- Model structure
- CRUD operations

### `test_exceptions.py`
Tests for Custom Exceptions:
- Exception hierarchy
- Raising exceptions
- Exception messages

## Test Fixtures

From `conftest.py`:
- `test_db`: SQLite in-memory database
- `db_session`: Database session
- `sample_dataframe`: Mock OHLCV data
- `algorithm_params`: Standard algorithm parameters

## Test Coverage Goals

- **Algorithms**: 100% of validation and signal logic
- **Data Layer**: 100% of cache operations
- **Validators**: 100% of parameter checks
- **Database**: Model structure and operations

## Notes

- Tests use SQLite in-memory database for speed
- Mock data fetcher used instead of real Kite API
- All tests are independent and can run in any order
