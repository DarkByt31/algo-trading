#!/bin/bash

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}===== Backtest API Testing =====${NC}\n"

# Test 1: VOLTAS
echo -e "${GREEN}Test 1: VOLTAS Stock${NC}"
RESPONSE1=$(curl -s -X POST http://127.0.0.1:8000/api/v1/backtest \
  -H "Content-Type: application/json" \
  -d '{
    "symbol": "VOLTAS",
    "algorithm_id": "mean_reversion",
    "start_date": "2024-01-01",
    "end_date": "2024-01-15",
    "initial_capital": 50000,
    "parameters": {
      "SMA_WINDOW": 20,
      "Z_ENTRY": 1.2,
      "Z_EXIT_THRESHOLD": 0.4
    }
  }')
JOB1=$(echo "$RESPONSE1" | grep -o '"job_id":"[^"]*' | cut -d'"' -f4)
echo "Job ID: $JOB1"
echo "Status: $(echo "$RESPONSE1" | grep -o '"status":"[^"]*' | cut -d'"' -f4)"
RESULTS1=$(curl -s "http://127.0.0.1:8000/api/v1/results/$JOB1")
echo "Final Capital: $(echo "$RESULTS1" | grep -o '"final_capital":[^,]*' | cut -d':' -f2)"
echo "Total Trades: $(echo "$RESULTS1" | grep -o '"total_trades":[^,]*' | cut -d':' -f2)"
echo ""

# Test 2: TATVA
echo -e "${GREEN}Test 2: TATVA Stock${NC}"
RESPONSE2=$(curl -s -X POST http://127.0.0.1:8000/api/v1/backtest \
  -H "Content-Type: application/json" \
  -d '{
    "symbol": "TATVA",
    "algorithm_id": "mean_reversion",
    "start_date": "2024-01-01",
    "end_date": "2024-01-20",
    "initial_capital": 75000,
    "parameters": {
      "SMA_WINDOW": 20,
      "Z_ENTRY": 1.5,
      "Z_EXIT_THRESHOLD": 0.5
    }
  }')
JOB2=$(echo "$RESPONSE2" | grep -o '"job_id":"[^"]*' | cut -d'"' -f4)
echo "Job ID: $JOB2"
echo "Status: $(echo "$RESPONSE2" | grep -o '"status":"[^"]*' | cut -d'"' -f4)"
RESULTS2=$(curl -s "http://127.0.0.1:8000/api/v1/results/$JOB2")
echo "Final Capital: $(echo "$RESULTS2" | grep -o '"final_capital":[^,]*' | cut -d':' -f2)"
echo "Total Trades: $(echo "$RESULTS2" | grep -o '"total_trades":[^,]*' | cut -d':' -f2)"
echo ""

# Test 3: RELIANCE
echo -e "${GREEN}Test 3: RELIANCE Stock${NC}"
RESPONSE3=$(curl -s -X POST http://127.0.0.1:8000/api/v1/backtest \
  -H "Content-Type: application/json" \
  -d '{
    "symbol": "RELIANCE",
    "algorithm_id": "mean_reversion",
    "start_date": "2024-01-01",
    "end_date": "2024-01-25",
    "initial_capital": 100000,
    "parameters": {
      "SMA_WINDOW": 20,
      "Z_ENTRY": 1.0,
      "Z_EXIT_THRESHOLD": 0.3
    }
  }')
JOB3=$(echo "$RESPONSE3" | grep -o '"job_id":"[^"]*' | cut -d'"' -f4)
echo "Job ID: $JOB3"
echo "Status: $(echo "$RESPONSE3" | grep -o '"status":"[^"]*' | cut -d'"' -f4)"
RESULTS3=$(curl -s "http://127.0.0.1:8000/api/v1/results/$JOB3")
echo "Final Capital: $(echo "$RESULTS3" | grep -o '"final_capital":[^,]*' | cut -d':' -f2)"
echo "Total Trades: $(echo "$RESULTS3" | grep -o '"total_trades":[^,]*' | cut -d':' -f2)"
echo ""

# Test 4: VOLTAS with different parameters
echo -e "${GREEN}Test 4: VOLTAS Stock (Different Parameters)${NC}"
RESPONSE4=$(curl -s -X POST http://127.0.0.1:8000/api/v1/backtest \
  -H "Content-Type: application/json" \
  -d '{
    "symbol": "VOLTAS",
    "algorithm_id": "mean_reversion",
    "start_date": "2024-01-05",
    "end_date": "2024-01-31",
    "initial_capital": 100000,
    "parameters": {
      "SMA_WINDOW": 15,
      "Z_ENTRY": 2.0,
      "Z_EXIT_THRESHOLD": 0.8
    }
  }')
JOB4=$(echo "$RESPONSE4" | grep -o '"job_id":"[^"]*' | cut -d'"' -f4)
echo "Job ID: $JOB4"
echo "Status: $(echo "$RESPONSE4" | grep -o '"status":"[^"]*' | cut -d'"' -f4)"
RESULTS4=$(curl -s "http://127.0.0.1:8000/api/v1/results/$JOB4")
echo "Final Capital: $(echo "$RESULTS4" | grep -o '"final_capital":[^,]*' | cut -d':' -f2)"
echo "Total Trades: $(echo "$RESULTS4" | grep -o '"total_trades":[^,]*' | cut -d':' -f2)"
echo ""

echo -e "${BLUE}===== Testing Complete =====${NC}"
