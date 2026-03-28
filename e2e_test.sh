#!/bin/bash

# Phase 5: End-to-End Integration Testing
# Tests the complete backtest flow: Submit → Wait → Verify Results

set -e  # Exit on error

API_BASE="http://localhost:8000/api/v1"
RESULTS_DIR="./e2e_test_results"
mkdir -p "$RESULTS_DIR"

# Color codes for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Helper functions
log_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

log_error() {
    echo -e "${RED}❌ $1${NC}"
}

log_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

log_test() {
    echo -e "${YELLOW}🧪 $1${NC}"
}

# Test 1: Verify API is running
test_api_health() {
    log_test "Test 1: API Health Check"
    
    response=$(curl -s -w "\n%{http_code}" "$API_BASE/stocks")
    http_code=$(echo "$response" | tail -n1)
    body=$(echo "$response" | head -n-1)
    
    if [ "$http_code" = "200" ]; then
        log_success "API is running"
        echo "Response: $body" | head -c 100
        echo ""
    else
        log_error "API health check failed (HTTP $http_code)"
        exit 1
    fi
}

# Test 2: Get available stocks
test_get_stocks() {
    log_test "Test 2: Get Available Stocks"
    
    stocks=$(curl -s "$API_BASE/stocks")
    stock_count=$(echo "$stocks" | jq 'length')
    
    if [ "$stock_count" -gt 0 ]; then
        log_success "Found $stock_count stocks"
        echo "Stocks: $(echo "$stocks" | jq -r '.[]' | head -3 | tr '\n' ', ')"
        echo ""
    else
        log_error "No stocks found"
        exit 1
    fi
}

# Test 3: Get available algorithms
test_get_algorithms() {
    log_test "Test 3: Get Available Algorithms"
    
    algorithms=$(curl -s "$API_BASE/algorithms")
    algo_count=$(echo "$algorithms" | jq 'length')
    
    if [ "$algo_count" -gt 0 ]; then
        log_success "Found $algo_count algorithms"
        algo_id=$(echo "$algorithms" | jq -r '.[0].id')
        algo_name=$(echo "$algorithms" | jq -r '.[0].name')
        echo "First algorithm: $algo_name (id: $algo_id)"
        echo ""
    else
        log_error "No algorithms found"
        exit 1
    fi
}

# Test 4: Submit backtest job
test_submit_backtest() {
    local symbol=$1
    local algo=$2
    local start_date=$3
    local end_date=$4
    
    log_test "Test 4: Submit Backtest - $symbol with $algo"
    
    payload=$(cat <<EOF
{
    "symbol": "$symbol",
    "algorithm": "$algo",
    "start_date": "$start_date",
    "end_date": "$end_date",
    "capital": 50000,
    "parameters": {
        "SMA_WINDOW": "20",
        "Z_ENTRY": "-2.0",
        "Z_EXIT_THRESHOLD": "0.5"
    }
}
EOF
)
    
    response=$(curl -s -X POST "$API_BASE/backtest" \
        -H "Content-Type: application/json" \
        -d "$payload")
    
    job_id=$(echo "$response" | jq -r '.job_id // empty')
    
    if [ -n "$job_id" ]; then
        log_success "Backtest submitted: $job_id"
        echo ""
        echo "$job_id"  # Return job_id
    else
        log_error "Failed to submit backtest"
        echo "Response: $response"
        exit 1
    fi
}

# Test 5: Wait for backtest completion
test_wait_for_results() {
    local job_id=$1
    local max_wait=$2  # in seconds
    
    log_test "Test 5: Wait for Backtest Completion (Job: $job_id)"
    
    elapsed=0
    interval=2
    
    while [ $elapsed -lt $max_wait ]; do
        results=$(curl -s "$API_BASE/results/$job_id")
        status=$(echo "$results" | jq -r '.status // "unknown"')
        
        if [ "$status" = "completed" ] || [ "$status" = "failed" ]; then
            log_success "Backtest $status"
            echo "$results"
            return 0
        fi
        
        echo -n "."
        sleep $interval
        elapsed=$((elapsed + interval))
    done
    
    log_error "Timeout waiting for backtest (${max_wait}s exceeded)"
    exit 1
}

# Test 6: Verify results structure
test_verify_results() {
    local results=$1
    
    log_test "Test 6: Verify Results Structure"
    
    # Check required fields
    required_fields=("job_id" "symbol" "initial_capital" "final_capital" "total_trades" "return_percentage" "status")
    
    for field in "${required_fields[@]}"; do
        value=$(echo "$results" | jq -r ".$field // empty")
        if [ -z "$value" ]; then
            log_error "Missing field: $field"
            exit 1
        fi
    done
    
    log_success "All required fields present"
    
    # Display key metrics
    symbol=$(echo "$results" | jq -r '.symbol')
    initial=$(echo "$results" | jq -r '.initial_capital')
    final=$(echo "$results" | jq -r '.final_capital')
    trades=$(echo "$results" | jq -r '.total_trades')
    return=$(echo "$results" | jq -r '.return_percentage')
    
    echo "Symbol: $symbol"
    echo "Initial Capital: ₹$initial"
    echo "Final Capital: ₹$final"
    echo "Total Trades: $trades"
    echo "Return: ${return}%"
    echo ""
}

# Test 7: Get trade log
test_get_trades() {
    local job_id=$1
    
    log_test "Test 7: Get Trade Log (Job: $job_id)"
    
    trades=$(curl -s "$API_BASE/trades/$job_id")
    trade_count=$(echo "$trades" | jq 'length')
    
    if [ "$trade_count" -gt 0 ]; then
        log_success "Found $trade_count trades"
        
        # Display first trade
        echo "Sample trade:"
        echo "$trades" | jq '.[0]'
    else
        log_info "No trades in this backtest"
    fi
    echo ""
}

# Test 8: Test multiple stocks
test_multiple_stocks() {
    log_test "Test 8: Test Multiple Stocks"
    
    stocks=("TATVA" "VOLTAS" "RELIANCE")
    
    for stock in "${stocks[@]}"; do
        echo "Testing stock: $stock"
        
        job_id=$(test_submit_backtest "$stock" "mean_reversion" "2024-01-01" "2024-01-10")
        results=$(test_wait_for_results "$job_id" 60)
        
        symbol=$(echo "$results" | jq -r '.symbol')
        final=$(echo "$results" | jq -r '.final_capital')
        return=$(echo "$results" | jq -r '.return_percentage')
        
        echo "  Final Capital: ₹$final, Return: ${return}%"
        
        # Save result
        echo "$results" > "$RESULTS_DIR/${stock}_result.json"
    done
    
    echo ""
}

# Test 9: Concurrent backtest requests
test_concurrent_requests() {
    log_test "Test 9: Concurrent Requests (3 simultaneous)"
    
    job_ids=()
    
    for i in {1..3}; do
        job_id=$(test_submit_backtest "TATVA" "mean_reversion" "2024-01-0$i" "2024-01-1$i" &)
        job_ids+=("$job_id")
    done
    
    wait
    
    log_success "Submitted 3 concurrent backtest requests"
    echo "Job IDs: ${job_ids[@]}"
    echo ""
}

# Main test execution
main() {
    echo "╔════════════════════════════════════════╗"
    echo "║  PHASE 5: E2E INTEGRATION TESTING       ║"
    echo "║  Trading Backtester - Full Stack       ║"
    echo "╚════════════════════════════════════════╝"
    echo ""
    
    # Run all tests
    test_api_health
    test_get_stocks
    test_get_algorithms
    
    # Test single backtest
    log_info "Running single backtest test..."
    job_id=$(test_submit_backtest "TATVA" "mean_reversion" "2024-01-01" "2024-01-10")
    results=$(test_wait_for_results "$job_id" 60)
    test_verify_results "$results"
    test_get_trades "$job_id"
    
    # Save main test result
    echo "$results" > "$RESULTS_DIR/main_result.json"
    
    # Test multiple stocks
    log_info "Running multiple stock tests..."
    test_multiple_stocks
    
    # Summary
    echo "╔════════════════════════════════════════╗"
    echo "║  TEST EXECUTION COMPLETE               ║"
    echo "╚════════════════════════════════════════╝"
    echo ""
    log_success "All tests passed! ✨"
    echo "Results saved to: $RESULTS_DIR/"
    echo ""
}

# Run main if script is executed directly
if [ "${BASH_SOURCE[0]}" = "${0}" ]; then
    main "$@"
fi
