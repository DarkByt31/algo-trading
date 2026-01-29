# Trading Backtester - Backend

FastAPI-based backend for the trading backtesting platform.

## Setup

### Prerequisites
- Python 3.9+
- MySQL 8.0+

### Installation

1. **Create virtual environment**:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. **Install dependencies**:
```bash
pip install -r requirements.txt
```

3. **Setup MySQL database**:
```bash
mysql -u root -p
CREATE DATABASE algo_trading CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
EXIT;
```

4. **Create `.env` file** (from `.env.example`):
```bash
cp .env.example .env
# Edit .env with your settings and API credentials
```

5. **Initialize database tables**:
```bash
python -c "from app.db.session import engine; from app.db.base import Base; Base.metadata.create_all(bind=engine)"
```

### Running the Server

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Server will be available at: `http://localhost:8000`

- API Documentation: `http://localhost:8000/docs`
- Alternative Docs: `http://localhost:8000/redoc`

## Project Structure

```
app/
├── main.py              # FastAPI app entry point
├── config.py            # Configuration
│
├── api/
│   └── v1/              # API v1 routes (endpoints, schemas)
│
├── core/
│   ├── algorithms/      # Algorithm implementations
│   ├── backtest/        # Backtest engine & logic
│   └── data/            # Data fetching & caching
│
├── db/
│   ├── models/          # SQLAlchemy models
│   ├── base.py          # ORM setup
│   └── session.py       # DB session management
│
└── utils/               # Utilities & helpers
```

## Database

MySQL tables created automatically on startup:
- `algorithms` - Algorithm metadata
- `backtest_jobs` - Backtest execution requests
- `backtest_results` - Results & metrics
- `trades` - Individual trades

## API Endpoints (Phase 3)

```
GET  /api/v1/stocks               # List stocks
GET  /api/v1/algorithms           # List algorithms & parameters
POST /api/v1/backtest             # Submit backtest
GET  /api/v1/results/{job_id}     # Get results
GET  /api/v1/trades/{job_id}      # Get trade log
```

## Development

### Testing
```bash
pytest tests/
```

### Logging
Logs are configured via `LOG_LEVEL` in `.env` (default: INFO)

### Code Style
```bash
pylint app/
black app/
```

## Architecture

- **Data Layer**: Kite API integration with in-memory caching
- **Algorithm Layer**: Base class with implementations (Mean Reversion, etc.)
- **Backtest Engine**: Core execution & trade logic
- **API Layer**: FastAPI endpoints with Pydantic validation

## Key Components

### Algorithms
- `BaseAlgorithm`: Abstract base class for all algorithms
- `MeanReversionAlgorithm`: Mean reversion strategy implementation
- `AlgorithmRegistry`: Dynamic algorithm loading

### Data
- `DataFetcher`: Kite API integration
- `DataCache`: In-memory dictionary-based cache
- `MockDataFetcher`: For testing without API

### Database
- SQLAlchemy ORM models for MySQL
- Auto-migration on app startup

## Next Steps

1. Phase 2: Backtest engine & performance calculator
2. Phase 3: API endpoints
3. Phase 4: Frontend integration
