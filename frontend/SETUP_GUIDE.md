# Frontend Setup Guide

## Problem: Node.js/npm Not Available

If Node.js is not available on your system, you have several options:

### Option 1: Using Docker (Recommended)

Create a `Dockerfile` in the frontend directory:

```dockerfile
FROM node:20-alpine

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .

EXPOSE 3000

CMD ["npm", "run", "dev"]
```

Build and run:
```bash
cd frontend
docker build -t algo-trading-frontend .
docker run -p 3000:3000 -v $(pwd):/app algo-trading-frontend
```

### Option 2: Using Docker Compose

Create a `docker-compose.yml` in the root directory:

```yaml
version: '3.8'

services:
  backend:
    image: python:3.9
    working_dir: /app
    command: >
      sh -c "pip install -r requirements.txt &&
             uvicorn app.main:app --host 0.0.0.0 --port 8000"
    ports:
      - "8000:8000"
    volumes:
      - ./backend:/app
    environment:
      - DATABASE_URL=sqlite:///./test.db

  frontend:
    image: node:20-alpine
    working_dir: /app
    command: npm run dev
    ports:
      - "3000:3000"
    volumes:
      - ./frontend:/app
    depends_on:
      - backend
```

Run with:
```bash
docker-compose up
```

### Option 3: Local Installation (Ubuntu/Debian)

```bash
# Update package manager
sudo apt update

# Install Node.js 20 (LTS)
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt-get install -y nodejs

# Verify installation
node --version
npm --version
```

### Option 4: Using nvm (Node Version Manager)

```bash
# Install nvm
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash

# Reload shell
source ~/.bashrc

# Install Node.js 20
nvm install 20
nvm use 20

# Verify
node --version
npm --version
```

## After Installing Node.js

```bash
cd frontend

# Install dependencies
npm install

# Run development server
npm run dev

# Frontend will be available at http://localhost:3000
```

## Frontend Features

Once running, the frontend provides:

- **Stock Selection**: Choose from NSE stocks
- **Algorithm Selection**: Pick mean reversion or other algorithms
- **Dynamic Parameters**: Configure algorithm parameters in real-time
- **Backtest Submission**: Submit backtest with custom date ranges and capital
- **Real-time Results**: View comprehensive backtest metrics and trade logs
- **Capital Growth Chart**: Visualize portfolio performance
- **Trade Log**: Detailed table of all executed trades

## API Endpoints Used

The frontend communicates with the backend at `http://localhost:8000/api/v1`:

- `GET /stocks` - Available stocks
- `GET /algorithms` - Algorithm metadata
- `POST /backtest` - Submit backtest
- `GET /results/{job_id}` - Get results
- `GET /trades/{job_id}` - Get trade log

## Troubleshooting

### CORS Issues
If you see CORS errors, ensure:
1. Backend is running on `http://localhost:8000`
2. Frontend vite.config.ts has the proxy configured
3. Check browser console for specific errors

### Connection Refused
Ensure the backend is running:
```bash
cd backend
python -m uvicorn app.main:app --reload
```

### Module Not Found
If you see module errors after npm install:
```bash
rm -rf node_modules package-lock.json
npm install
```

## Production Build

```bash
npm run build

# Output will be in dist/
# Serve with any static server:
npx serve dist
```
