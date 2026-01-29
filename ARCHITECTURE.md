# Trading Backtesting Application - Architecture & Plan

**Project Date**: January 29, 2026

---

## Table of Contents
1. [Overview](#overview)
2. [Tech Stack](#tech-stack)
3. [Architecture](#architecture)
4. [Project Structure](#project-structure)
5. [Database Schema](#database-schema)
6. [API Contracts](#api-contracts)
7. [Implementation Roadmap](#implementation-roadmap)

---

## Overview

A full-stack trading backtesting application for Indian equity markets that allows users to:
- Select stocks from NSE
- Choose algorithmic trading strategies
- Tune algorithm parameters dynamically
- Run backtests with customizable date ranges and capital
- View trade logs, P&L analysis, and performance metrics
- Visualize algorithm signals and price movements in real-time

**Scope Constraints**:
- Intraday trading (5-minute intervals, hardcoded for now)
- Max 3-month backtest range
- Initial capital configurable
- Short selling allowed
- Brokerage fees & charges included in P&L

---

## Tech Stack

### Backend
- **Language**: Python 3.9+
- **Framework**: FastAPI (async, modern, fast, auto-documentation)
- **Web Server**: Uvicorn
- **Data Processing**: pandas, numpy, scipy
- **Broker API**: Zerodha Kite Connect
- **Database**: MySQL 8.0+
- **ORM**: SQLAlchemy
- **Validation**: Pydantic
- **Caching**: In-memory dictionaries/maps (no external dependencies)
- **Task Queue**: None (sync execution initially, can upgrade to Celery/RabbitMQ later)

**Why MySQL over PostgreSQL?**
- Simpler setup and maintenance for this use case
- Sufficient for structured financial data
- Better compatibility with common shared hosting
- Easier schema migrations for rapid prototyping

### Frontend
- **Framework**: React 18+ with TypeScript
- **State Management**: Zustand (lightweight, easier than Redux)
- **HTTP Client**: Axios
- **Charts**: Recharts (lightweight, responsive)
- **UI Components**: Material-UI v5 (comprehensive, professional)
- **Form Handling**: React Hook Form (simple, performant)
- **Real-time Updates**: Polling initially, WebSocket upgrade later

### Development Tools
- **Version Control**: Git
- **Testing**: pytest (backend), Vitest (frontend)
- **Linting**: pylint, ESLint
- **Formatting**: Black (Python), Prettier (JavaScript)

---

## Architecture

### System Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                     FRONTEND (React)                             │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐           │
│  │ Stock Select │  │ Algo Select  │  │ Param Form   │           │
│  └──────────────┘  └──────────────┘  └──────────────┘           │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │        Results Dashboard (Charts, Trade Log)             │   │
│  └──────────────────────────────────────────────────────────┘   │
└──────────────┬──────────────────────────────────────────────────┘
               │ HTTP REST API
               ▼
┌─────────────────────────────────────────────────────────────────┐
│                    BACKEND (FastAPI)                             │
├─────────────────────────────────────────────────────────────────┤
│  ┌─────────────────────────┐  ┌──────────────────────────────┐  │
│  │  API Routes Layer       │  │  Business Logic Layer        │  │
│  │ ─────────────────────── │  │ ──────────────────────────   │  │
│  │ /api/v1/stocks          │  │ • AlgorithmRegistry          │  │
│  │ /api/v1/algorithms      │  │ • BacktestEngine             │  │
│  │ /api/v1/backtest        │  │ • TradeExecutor              │  │
│  │ /api/v1/results         │  │ • PerformanceCalculator      │  │
│  │ /api/v1/trades          │  │ • ParameterValidator         │  │
│  └─────────────────────────┘  └──────────────────────────────┘  │
│                                                                   │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │  Data & Integration Layer                                │   │
│  │  ──────────────────────────────────────────────────────  │   │
│  │  • DataFetcher (Kite API)                                │   │
│  │  • DataCache (in-memory dict cache)                      │   │
│  │  • DataPreprocessor                                      │   │
│  └──────────────────────────────────────────────────────────┘   │
│                                                                   │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │  Core Algorithms                                         │   │
│  │  ──────────────────────────────────────────────────────  │   │
│  │  • BaseAlgorithm (abstract)                              │   │
│  │  • MeanReversionAlgorithm                                │   │
│  │  • MomentumAlgorithm (future)                            │   │
│  └──────────────────────────────────────────────────────────┘   │
└──────┬──────────────────────────────────────────────────────────┘
       │ SQL Queries (SQLAlchemy ORM)
       ▼
┌─────────────────────────────────────────────────────────────────┐
│                   MySQL Database                                 │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │ Tables:                                                  │   │
│  │ • algorithms - Algorithm metadata & parameters           │   │
│  │ • backtest_jobs - Backtest execution history            │   │
│  │ • backtest_results - Results & metrics                  │   │
│  │ • trades - Individual trade records                     │   │
│  └──────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
```

### Data Flow

```
1. User Request
   ↓
2. Frontend sends: POST /api/v1/backtest with parameters
   ↓
3. Backend validates inputs (Pydantic schemas)
   ↓
4. Fetch historical data from Kite API (cached if available)
   ↓
5. Create backtest job record in DB
   ↓
6. Run backtest synchronously:
   - Load algorithm (from registry)
   - Apply signals to price data
   - Execute trades based on logic
   - Calculate P&L and metrics
   ↓
7. Store results in DB (backtest_results, trades)
   ↓
8. Return job_id to frontend for result polling
   ↓
9. Frontend polls GET /api/v1/results/{job_id}
   ↓
10. Return full results with charts & trade log
```

### Data Caching Strategy

```
In-Memory Cache (Dictionary):
{
  "RELIANCE_5minute_2026-01-01_2026-01-31": DataFrame,
  "VOLTAS_5minute_2026-01-01_2026-01-31": DataFrame
}

Cache Key: {symbol}_{interval}_{from_date}_{to_date}
TTL: 24 hours (in-memory, expires on server restart)
```

---

## Project Structure

```
algo-trading-backtester/
│
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py                          # FastAPI app entry point
│   │   ├── config.py                        # Configuration (DB, API keys, etc.)
│   │   ├── dependencies.py                  # Shared dependencies
│   │   │
│   │   ├── api/
│   │   │   ├── __init__.py
│   │   │   ├── v1/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── endpoints/
│   │   │   │   │   ├── __init__.py
│   │   │   │   │   ├── stocks.py            # GET /api/v1/stocks
│   │   │   │   │   ├── algorithms.py        # GET /api/v1/algorithms
│   │   │   │   │   ├── backtest.py          # POST /api/v1/backtest
│   │   │   │   │   ├── results.py           # GET /api/v1/results
│   │   │   │   │   └── trades.py            # GET /api/v1/trades
│   │   │   │   └── schemas/
│   │   │   │       ├── __init__.py
│   │   │   │       ├── backtest.py          # Pydantic models
│   │   │   │       ├── results.py
│   │   │   │       ├── algorithm.py
│   │   │   │       └── trade.py
│   │   │
│   │   ├── core/
│   │   │   ├── __init__.py
│   │   │   │
│   │   │   ├── algorithms/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── base.py                  # BaseAlgorithm (abstract)
│   │   │   │   ├── mean_reversion.py        # Mean reversion implementation
│   │   │   │   └── registry.py              # Algorithm registry/loader
│   │   │   │
│   │   │   ├── backtest/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── engine.py                # Core backtest engine
│   │   │   │   ├── executor.py              # Trade execution logic
│   │   │   │   ├── calculator.py            # P&L & metrics calculation
│   │   │   │   └── validator.py             # Input validation
│   │   │   │
│   │   │   └── data/
│   │   │       ├── __init__.py
│   │   │       ├── fetcher.py               # Kite API integration
│   │   │       ├── cache.py                 # In-memory cache
│   │   │       └── preprocessor.py          # Data cleaning
│   │   │
│   │   ├── db/
│   │   │   ├── __init__.py
│   │   │   ├── base.py                      # SQLAlchemy base config
│   │   │   ├── session.py                   # DB session management
│   │   │   └── models/
│   │   │       ├── __init__.py
│   │   │       ├── algorithm.py             # Algorithm metadata
│   │   │       ├── backtest_job.py          # Backtest jobs
│   │   │       ├── backtest_result.py       # Results & metrics
│   │   │       └── trade.py                 # Individual trades
│   │   │
│   │   └── utils/
│   │       ├── __init__.py
│   │       ├── logger.py                    # Logging setup
│   │       └── exceptions.py                # Custom exceptions
│   │
│   ├── migrations/                          # Alembic migrations (future)
│   ├── tests/
│   │   ├── __init__.py
│   │   ├── test_algorithms.py
│   │   ├── test_backtest_engine.py
│   │   ├── test_api_routes.py
│   │   └── conftest.py
│   │
│   ├── requirements.txt
│   ├── .env.example
│   └── README.md
│
├── frontend/
│   ├── public/
│   │   ├── index.html
│   │   └── favicon.ico
│   │
│   ├── src/
│   │   ├── index.tsx
│   │   ├── App.tsx
│   │   ├── App.css
│   │   │
│   │   ├── components/
│   │   │   ├── StockSelector.tsx            # Stock dropdown
│   │   │   ├── AlgorithmSelector.tsx        # Algo selection
│   │   │   ├── ParameterForm.tsx            # Dynamic parameter form
│   │   │   ├── BacktestConfig.tsx           # Date range, capital config
│   │   │   ├── SubmitButton.tsx
│   │   │   ├── ResultsDisplay.tsx           # Main results view
│   │   │   ├── TradeLog.tsx                 # Trade table
│   │   │   ├── ChartContainer.tsx           # Chart display
│   │   │   └── LoadingSpinner.tsx
│   │   │
│   │   ├── pages/
│   │   │   ├── BacktestPage.tsx             # Main backtest page
│   │   │   └── ResultsPage.tsx              # Results dashboard
│   │   │
│   │   ├── hooks/
│   │   │   ├── useBacktest.ts               # Backtest submission
│   │   │   ├── useResults.ts                # Results polling
│   │   │   ├── useAlgorithms.ts             # Fetch algorithm metadata
│   │   │   ├── useStocks.ts                 # Fetch stock list
│   │   │   └── useApi.ts                    # Generic API hook
│   │   │
│   │   ├── services/
│   │   │   └── api.ts                       # API client (Axios)
│   │   │
│   │   ├── types/
│   │   │   ├── backtest.ts
│   │   │   ├── algorithm.ts
│   │   │   ├── results.ts
│   │   │   └── api.ts
│   │   │
│   │   └── styles/
│   │       └── index.css
│   │
│   ├── package.json
│   ├── tsconfig.json
│   ├── vite.config.ts
│   ├── .env.example
│   └── README.md
│
├── ARCHITECTURE.md                          # This file
├── .gitignore
└── README.md
```

---

## Database Schema

### 1. `algorithms` Table
Stores algorithm metadata and parameter definitions

```sql
CREATE TABLE algorithms (
  id VARCHAR(50) PRIMARY KEY,
  name VARCHAR(255) NOT NULL,
  description TEXT,
  version VARCHAR(20) DEFAULT '1.0',
  is_active BOOLEAN DEFAULT TRUE,
  parameters JSON,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

**Sample Data**:
```json
{
  "id": "mean_reversion",
  "name": "Mean Reversion",
  "description": "Detects price deviations from mean and reverts...",
  "version": "1.0",
  "is_active": true,
  "parameters": [
    {
      "name": "SMA_WINDOW",
      "type": "integer",
      "default": 20,
      "min": 5,
      "max": 100,
      "description": "Simple Moving Average window"
    },
    {
      "name": "Z_ENTRY",
      "type": "float",
      "default": 1.0,
      "min": 0.5,
      "max": 3.0,
      "description": "Z-score entry threshold"
    },
    {
      "name": "Z_EXIT_THRESHOLD",
      "type": "float",
      "default": 0.3,
      "min": 0.1,
      "max": 1.0,
      "description": "Z-score exit threshold"
    }
  ]
}
```

---

### 2. `backtest_jobs` Table
Tracks all backtest execution requests

```sql
CREATE TABLE backtest_jobs (
  id VARCHAR(36) PRIMARY KEY,
  symbol VARCHAR(20) NOT NULL,
  algorithm_id VARCHAR(50) NOT NULL,
  parameters JSON NOT NULL,
  start_date DATE NOT NULL,
  end_date DATE NOT NULL,
  initial_capital DECIMAL(12, 2) NOT NULL,
  allow_short BOOLEAN DEFAULT TRUE,
  brokerage_fee DECIMAL(8, 2) DEFAULT 20,
  status ENUM('queued', 'processing', 'completed', 'failed') DEFAULT 'queued',
  error_message TEXT,
  execution_time_ms INT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  
  FOREIGN KEY (algorithm_id) REFERENCES algorithms(id),
  INDEX idx_status (status),
  INDEX idx_created_at (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

---

### 3. `backtest_results` Table
Stores computed results and performance metrics

```sql
CREATE TABLE backtest_results (
  id VARCHAR(36) PRIMARY KEY,
  job_id VARCHAR(36) NOT NULL UNIQUE,
  final_capital DECIMAL(12, 2) NOT NULL,
  total_return DECIMAL(12, 2) NOT NULL,
  return_percentage DECIMAL(8, 4) NOT NULL,
  total_trades INT DEFAULT 0,
  winning_trades INT DEFAULT 0,
  losing_trades INT DEFAULT 0,
  win_rate DECIMAL(5, 2),
  max_drawdown DECIMAL(8, 4),
  min_capital DECIMAL(12, 2),
  sharpe_ratio DECIMAL(8, 4),
  profit_factor DECIMAL(8, 4),
  avg_trade_duration_minutes INT,
  best_trade_pnl DECIMAL(12, 2),
  worst_trade_pnl DECIMAL(12, 2),
  chart_data JSON,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  
  FOREIGN KEY (job_id) REFERENCES backtest_jobs(id) ON DELETE CASCADE,
  INDEX idx_job_id (job_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

---

### 4. `trades` Table
Individual trade records

```sql
CREATE TABLE trades (
  id VARCHAR(36) PRIMARY KEY,
  job_id VARCHAR(36) NOT NULL,
  trade_sequence INT NOT NULL,
  trade_type ENUM('BUY', 'SELL', 'EXIT') NOT NULL,
  symbol VARCHAR(20) NOT NULL,
  trade_time TIMESTAMP NOT NULL,
  price DECIMAL(10, 2) NOT NULL,
  quantity INT NOT NULL,
  brokerage_fee DECIMAL(8, 2) DEFAULT 0,
  capital_after DECIMAL(12, 2),
  pnl DECIMAL(12, 2),
  pnl_percentage DECIMAL(8, 4),
  z_score DECIMAL(8, 4),
  sma DECIMAL(10, 2),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  
  FOREIGN KEY (job_id) REFERENCES backtest_jobs(id) ON DELETE CASCADE,
  INDEX idx_job_id (job_id),
  INDEX idx_trade_time (trade_time)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

---

## API Contracts

### Base URL: `http://localhost:8000/api/v1`

### 1. Get Available Stocks

```
GET /stocks

Response: 200 OK
Content-Type: application/json

{
  "data": [
    {
      "symbol": "RELIANCE",
      "name": "Reliance Industries",
      "exchange": "NSE",
      "sector": "Energy"
    },
    {
      "symbol": "VOLTAS",
      "name": "Voltas Limited",
      "exchange": "NSE",
      "sector": "Electrical Equipment"
    }
  ],
  "count": 2
}
```

---

### 2. Get Algorithms & Parameters

```
GET /algorithms

Response: 200 OK
Content-Type: application/json

{
  "data": [
    {
      "id": "mean_reversion",
      "name": "Mean Reversion",
      "description": "Detects overextension and trades reversal...",
      "version": "1.0",
      "parameters": [
        {
          "name": "SMA_WINDOW",
          "type": "integer",
          "default": 20,
          "min": 5,
          "max": 100,
          "description": "Moving average window"
        },
        {
          "name": "Z_ENTRY",
          "type": "float",
          "default": 1.0,
          "min": 0.5,
          "max": 3.0,
          "description": "Z-score entry threshold"
        },
        {
          "name": "Z_EXIT_THRESHOLD",
          "type": "float",
          "default": 0.3,
          "min": 0.1,
          "max": 1.0,
          "description": "Z-score exit threshold"
        }
      ]
    }
  ],
  "count": 1
}
```

---

### 3. Submit Backtest

```
POST /backtest

Request:
Content-Type: application/json

{
  "symbol": "RELIANCE",
  "algorithm_id": "mean_reversion",
  "parameters": {
    "SMA_WINDOW": 20,
    "Z_ENTRY": 1.0,
    "Z_EXIT_THRESHOLD": 0.3
  },
  "start_date": "2026-01-01",
  "end_date": "2026-01-15",
  "initial_capital": 50000,
  "allow_short": true,
  "brokerage_fee": 20
}

Response: 202 Accepted
Content-Type: application/json

{
  "job_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "queued",
  "message": "Backtest submitted successfully"
}
```

---

### 4. Get Backtest Results

```
GET /results/{job_id}

Response: 200 OK (when completed)
Content-Type: application/json

{
  "job_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "completed",
  "data": {
    "symbol": "RELIANCE",
    "algorithm_id": "mean_reversion",
    "initial_capital": 50000,
    "final_capital": 52350.50,
    "total_return": 2350.50,
    "return_percentage": 4.7,
    "total_trades": 15,
    "winning_trades": 10,
    "losing_trades": 5,
    "win_rate": 66.67,
    "max_drawdown": -2.1,
    "sharpe_ratio": 1.23,
    "profit_factor": 2.15,
    "avg_trade_duration_minutes": 45,
    "best_trade_pnl": 450.50,
    "worst_trade_pnl": -150.25,
    "execution_time_ms": 1250,
    "chart_data": {
      "timestamps": [
        "2026-01-01 09:15",
        "2026-01-01 09:20",
        "2026-01-01 09:25"
      ],
      "prices": [2500.0, 2510.5, 2505.25],
      "sma": [2502.5, 2505.25, 2507.0],
      "z_scores": [0.5, -0.2, 1.1],
      "signals": ["HOLD", "BUY", "HOLD"]
    }
  }
}

Response: 202 Accepted (when still processing)
Content-Type: application/json

{
  "job_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "processing",
  "progress": 65
}
```

---

### 5. Get Trade Log

```
GET /trades/{job_id}?limit=50&offset=0

Response: 200 OK
Content-Type: application/json

{
  "job_id": "550e8400-e29b-41d4-a716-446655440000",
  "trades": [
    {
      "id": "trade-001",
      "sequence": 1,
      "type": "BUY",
      "symbol": "RELIANCE",
      "time": "2026-01-01 10:30:00",
      "price": 2500.50,
      "quantity": 20,
      "brokerage_fee": 20,
      "capital_after": 49979.00,
      "pnl": null,
      "z_score": -1.2,
      "sma": 2505.0
    },
    {
      "id": "trade-002",
      "sequence": 2,
      "type": "EXIT",
      "symbol": "RELIANCE",
      "time": "2026-01-01 11:15:00",
      "price": 2510.25,
      "quantity": 20,
      "brokerage_fee": 20,
      "capital_after": 50175.50,
      "pnl": 175.50,
      "pnl_percentage": 0.35,
      "z_score": 0.5,
      "sma": 2508.0
    }
  ],
  "pagination": {
    "total": 15,
    "limit": 50,
    "offset": 0,
    "pages": 1
  }
}
```

---

## Implementation Roadmap

### Phase 1: Backend Setup & Core Engine (Week 1-2)
- [ ] Initialize FastAPI project structure
- [ ] Setup MySQL database and SQLAlchemy models
- [ ] Implement database models: algorithms, backtest_jobs, backtest_results, trades
- [ ] Create data fetching layer (Kite API integration)
- [ ] Implement in-memory caching for historical data
- [ ] Build base algorithm abstract class

### Phase 2: Algorithm Implementation (Week 2-3)
- [ ] Implement MeanReversionAlgorithm from existing code
- [ ] Create AlgorithmRegistry for dynamic loading
- [ ] Implement parameter validation
- [ ] Build BacktestEngine (core execution logic)
- [ ] Implement TradeExecutor (entry/exit logic)
- [ ] Create PerformanceCalculator (P&L, metrics)

### Phase 3: API Endpoints (Week 3)
- [ ] GET /api/v1/stocks - Stock list
- [ ] GET /api/v1/algorithms - Algorithm metadata
- [ ] POST /api/v1/backtest - Submit backtest job
- [ ] GET /api/v1/results/{job_id} - Get results & metrics
- [ ] GET /api/v1/trades/{job_id} - Get trade log
- [ ] Add error handling & validation

### Phase 4: Frontend Setup & UI (Week 3-4)
- [ ] Initialize React + TypeScript project
- [ ] Create component structure
- [ ] Build API client (Axios hooks)
- [ ] Implement form components for parameter tuning
- [ ] Build results display with charts (Recharts)
- [ ] Add polling mechanism for backtest results

### Phase 5: Integration & Testing (Week 4)
- [ ] End-to-end testing (submit backtest → view results)
- [ ] Unit tests for algorithms & engine
- [ ] Performance optimization
- [ ] Error handling & edge cases
- [ ] Documentation

### Phase 6: Future Enhancements
- [ ] Add more algorithms (Momentum, RSI, etc.)
- [ ] WebSocket support for real-time updates
- [ ] Async task queue (Celery) for heavy loads
- [ ] User authentication & multi-user support
- [ ] Result comparison & backtesting templates
- [ ] Containerization (Docker)

---

## Key Design Decisions

1. **In-Memory Caching**: Simple dictionary-based cache to avoid external dependencies. Perfect for this phase since data is fetched once per backtest.

2. **MySQL Choice**: 
   - Simpler setup compared to PostgreSQL
   - Sufficient for this structured financial data
   - Better for rapid prototyping and iteration
   - Easier migration path if needed

3. **Synchronous Execution**: Backtests run synchronously for now. Frontend polls results using job_id. Can upgrade to Celery/RabbitMQ when scale demands it.

4. **Algorithm Registry Pattern**: Dynamic algorithm loading allows easy addition of new strategies without modifying core engine.

5. **Parameter Validation**: Pydantic schemas ensure all inputs are valid before backtest execution, preventing runtime errors.

6. **Hardcoded Constraints**: 
   - 5-minute interval (hardcoded, easy to make configurable later)
   - 3-month max backtest range (enforced at API level)
   - NSE market hours only

7. **Separation of Concerns**:
   - Algorithms are self-contained and testable
   - Engine handles signal generation & execution logic
   - Calculator handles all P&L & metric computations
   - API layer is thin and focused on routing/validation

---

## Database Initialization

```sql
-- Create algorithms table and insert defaults
INSERT INTO algorithms (id, name, description, version, parameters) VALUES
('mean_reversion', 'Mean Reversion', 'Detects price deviations and trades reversal', '1.0', 
  JSON_ARRAY(
    JSON_OBJECT('name', 'SMA_WINDOW', 'type', 'integer', 'default', 20, 'min', 5, 'max', 100),
    JSON_OBJECT('name', 'Z_ENTRY', 'type', 'float', 'default', 1.0, 'min', 0.5, 'max', 3.0),
    JSON_OBJECT('name', 'Z_EXIT_THRESHOLD', 'type', 'float', 'default', 0.3, 'min', 0.1, 'max', 1.0)
  )
);
```

---

## Configuration Files

### Backend `.env.example`
```
DATABASE_URL=mysql+pymysql://user:password@localhost:3306/algo_trading
API_KEY=your_kite_api_key
API_SECRET=your_kite_api_secret
ACCESS_TOKEN=your_kite_access_token
DEBUG=True
LOG_LEVEL=INFO
```

### Frontend `.env.example`
```
VITE_API_BASE_URL=http://localhost:8000/api/v1
VITE_POLLING_INTERVAL=2000
```

---

## Deployment (Future - Post-Development)

Once code is complete:
1. Containerize with Docker
2. Use docker-compose for local dev
3. Deploy backend to cloud (AWS/GCP/Azure)
4. Deploy frontend to CDN
5. Setup CI/CD pipeline

---

## Next Steps

1. **Review this architecture** with any questions or modifications
2. **Start Phase 1** - Backend setup and database
3. **Create initial MySQL schema** and test connection
4. **Build algorithm registry** and port existing mean reversion code

---

**Last Updated**: January 29, 2026
**Status**: Architecture Approved, Ready for Implementation
