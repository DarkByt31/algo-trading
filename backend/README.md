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

#### Local (without Docker)
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

#### Docker & Docker Compose

1. **Build and run with docker-compose**:
```bash
# Copy the example docker env file
cp .env.local.example .env.local

# Edit .env.local with your API credentials (Kite Connect, DB passwords, etc.)
# These credentials are NOT included in the image—only used at runtime
vi .env.local

# Build and start services (DB + Backend)
docker-compose up --build
```

2. **Or build the image standalone**:
```bash
docker build -t backtester:latest .
docker run --env-file .env.local -p 8000:8000 -e DATABASE_URL="..." backtester:latest
```

3. **For development with live code reload**:
```bash
# Use docker-compose with volumes (already configured)
docker-compose up --build
```

4. **Run tests in container**:
```bash
docker-compose run backend pytest tests/
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

## Docker & Security

### Files Included in Git
- ✅ `Dockerfile` - Container image definition (no secrets)
- ✅ `.dockerignore` - Excludes sensitive files from image
- ✅ `docker-compose.yml` - Service orchestration (no hardcoded secrets)
- ✅ `.env.example` - Template for local environment
- ✅ `.env.local.example` - Template for Docker environment

### Files NOT Included in Git (Security-Critical)
- ❌ `.env` - Local development secrets
- ❌ `.env.local` - Docker environment secrets
- ❌ `.env.*.local` - Any local variant

These are already in `.gitignore` to prevent accidental commit.

### How Secrets Are Managed

1. **Container Images** (safe):
   - Images only contain application code, no `.env` files or secrets
   - Excluded via `.dockerignore`

2. **Runtime Secrets**:
   - Passed via environment variables or `.env.local` at runtime
   - `docker-compose` reads `.env.local` and injects into containers
   - Docker Compose passes `DATABASE_URL`, API keys via `environment:` section

3. **Production Deployment**:
   - Use Docker secrets (Swarm) or Kubernetes Secrets (K8s)
   - Or CI/CD platform secrets (GitHub Actions, GitLab CI, etc.)
   - Never hardcode credentials in `docker-compose.yml`

4. **Safe Workflow**:
   ```bash
   # Step 1: Clone repository (Dockerfile is included, .env is NOT)
   git clone <repo>
   cd backend
   
   # Step 2: Create .env.local with your secrets (NOT tracked by git)
   cp .env.local.example .env.local
   vi .env.local  # Edit with your API keys, DB passwords
   
   # Step 3: Build and run (secrets are only in .env.local, never in image)
   docker-compose up --build
   
   # Step 4: Verify .env.local is in .gitignore
   grep ".env.local" .gitignore  # Should exist
   ```

### Verifying Secrets Are Excluded

```bash
# Check that .dockerignore excludes .env files
grep ".env" .dockerignore

# Verify image doesn't contain secrets
docker build -t test . && docker run --rm test cat .env  # Should fail/be empty

# Check git won't track .env
git status .env.local  # Should show "ignored by git"
```

## Next Steps

1. Phase 2: Backtest engine & performance calculator
2. Phase 3: API endpoints
3. Phase 4: Frontend integration
