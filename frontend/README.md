# Trading Backtester Frontend

React + TypeScript frontend for the trading backtesting platform.

## Setup

### Prerequisites
- Node.js 18+
- npm or yarn

### Installation

1. **Install dependencies**:
```bash
npm install
```

2. **Create `.env` file** (from `.env.example`):
```bash
cp .env.example .env
# Update VITE_API_BASE_URL if backend is on different host/port
```

### Running the Development Server

```bash
npm run dev
```

Frontend will be available at: `http://localhost:3000`

The dev server has a proxy configured to forward `/api` requests to the backend at `http://localhost:8000`.

### Building for Production

```bash
npm run build
```

The optimized build will be in the `dist/` directory.

### Preview Production Build

```bash
npm run preview
```

## Project Structure

```
frontend/
├── src/
│   ├── components/          # Reusable UI components
│   ├── pages/               # Page components
│   ├── hooks/               # Custom React hooks
│   ├── services/            # API client and services
│   ├── types/               # TypeScript type definitions
│   ├── App.tsx              # Main App component
│   ├── main.tsx             # Entry point
│   └── App.css              # Global styles
├── public/                  # Static files
├── package.json
├── tsconfig.json
├── vite.config.ts
└── .env.example
```

## Features

- **Stock Selection**: Choose from available stocks
- **Algorithm Selection**: Pick trading algorithm with parameter tuning
- **Backtest Configuration**: Set date range and initial capital
- **Dynamic Parameters**: Automatically adjust algorithm parameters
- **Results Dashboard**: View comprehensive backtest metrics
- **Trade Log**: Detailed table of all executed trades
- **Capital Growth Chart**: Visualize portfolio performance over time
- **Real-time Polling**: Automatically fetch results as backtest completes

## API Integration

The frontend communicates with the backend API at `/api/v1` with the following endpoints:

- `GET /stocks` - List available stocks
- `GET /algorithms` - Get algorithm metadata
- `POST /backtest` - Submit backtest job
- `GET /results/{job_id}` - Get backtest results
- `GET /trades/{job_id}` - Get trade log
