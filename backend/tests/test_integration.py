"""
Integration Tests for Trading Backtester
Tests the complete workflow from API submission to results persistence
"""

import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.db.session import SessionLocal
from app.db.models import BacktestJob, BacktestResult, Trade

client = TestClient(app)


class TestIntegration:
    """Integration tests for complete backtest workflow"""

    @pytest.fixture(autouse=True)
    def setup(self):
        """Setup for each test"""
        yield
        # Cleanup after each test
        db = SessionLocal()
        db.query(Trade).delete()
        db.query(BacktestResult).delete()
        db.query(BacktestJob).delete()
        db.commit()
        db.close()

    def test_complete_backtest_workflow(self):
        """Test complete workflow: submit -> execute -> retrieve results"""
        
        # Step 1: Submit backtest
        response = client.post(
            "/api/v1/backtest",
            json={
                "symbol": "TATVA",
                "algorithm_id": "mean_reversion",
                "start_date": "2024-01-01",
                "end_date": "2024-01-10",
                "initial_capital": 50000,
                "parameters": {
                    "SMA_WINDOW": 20,
                    "Z_ENTRY": 1.0,
                    "Z_EXIT_THRESHOLD": 0.3
                }
            }
        )
        
        assert response.status_code in [200, 202], f"Failed to submit backtest: {response.text}"
        data = response.json()
        assert "job_id" in data
        
        job_id = data["job_id"]
        
        # Step 2: Retrieve results
        response = client.get(f"/api/v1/results/{job_id}")
        assert response.status_code in [200, 202]
        
        results = response.json()
        assert results["job_id"] == job_id
        assert results["symbol"] == "TATVA"
        assert "initial_capital" in results
        assert "final_capital" in results
        assert "total_trades" in results
        
        # Step 3: Retrieve trades
        response = client.get(f"/api/v1/trades/{job_id}")
        assert response.status_code in [200, 202]
        
        trades = response.json()
        assert isinstance(trades, list)
        
        # Validate trade structure if trades exist
        if trades:
            trade = trades[0]
            assert "entry_price" in trade
            assert "exit_date" in trade
            assert "exit_price" in trade
            assert "pnl" in trade

    def test_multiple_stocks_backtest(self):
        """Test backtesting multiple stocks with same algorithm"""
        
        symbols = ["TATVA", "VOLTAS", "RELIANCE"]
        job_ids = []
        
        # Submit backtests for multiple stocks
        for symbol in symbols:
            response = client.post(
                "/api/v1/backtest",
                json={
                    "symbol": symbol,
                    "algorithm_id": "mean_reversion",
                    "start_date": "2024-01-01",
                    "end_date": "2024-01-10",
                    "initial_capital": 50000,
                    "parameters": {
                        "SMA_WINDOW": 20,
                        "Z_ENTRY": 1.0,
                        "Z_EXIT_THRESHOLD": 0.3
                    }
                }
            )
            
            assert response.status_code in [200, 202]
            job_ids.append(response.json()["job_id"])
        
        # Verify all results were created
        assert len(job_ids) == len(symbols)
        
        for i, job_id in enumerate(job_ids):
            response = client.get(f"/api/v1/results/{job_id}")
            assert response.status_code in [200, 202]
            assert response.json()["symbol"] == symbols[i]

    def test_different_parameters(self):
        """Test same stock with different parameters"""
        
        parameter_sets = [
            {"SMA_WINDOW": 10, "Z_ENTRY": 0.5, "Z_EXIT_THRESHOLD": 0.3},
            {"SMA_WINDOW": 20, "Z_ENTRY": 1.0, "Z_EXIT_THRESHOLD": 0.3},
            {"SMA_WINDOW": 30, "Z_ENTRY": 2.0, "Z_EXIT_THRESHOLD": 0.5},
        ]
        
        for params in parameter_sets:
            response = client.post(
                "/api/v1/backtest",
                json={
                    "symbol": "TATVA",
                    "algorithm_id": "mean_reversion",
                    "start_date": "2024-01-01",
                    "end_date": "2024-01-10",
                    "initial_capital": 50000,
                    "parameters": params
                }
            )
            
            assert response.status_code in [200, 202]
            assert response.json()["status"] == "completed"

    def test_different_date_ranges(self):
        """Test same stock with different date ranges"""
        
        date_ranges = [
            ("2024-01-01", "2024-01-05"),
            ("2024-01-05", "2024-01-10"),
            ("2024-01-01", "2024-01-15"),
        ]
        
        for start, end in date_ranges:
            response = client.post(
                "/api/v1/backtest",
                json={
                    "symbol": "TATVA",
                    "algorithm_id": "mean_reversion",
                    "start_date": start,
                    "end_date": end,
                    "initial_capital": 50000,
                    "parameters": {
                        "SMA_WINDOW": 20,
                        "Z_ENTRY": 1.0,
                        "Z_EXIT_THRESHOLD": 0.3
                    }
                }
            )
            
            assert response.status_code in [200, 202]

    def test_different_capital_amounts(self):
        """Test same backtest with different capital amounts"""
        
        capitals = [10000, 50000, 100000, 500000]
        
        for capital in capitals:
            response = client.post(
                "/api/v1/backtest",
                json={
                    "symbol": "TATVA",
                    "algorithm_id": "mean_reversion",
                    "start_date": "2024-01-01",
                    "end_date": "2024-01-10",
                    "initial_capital": capital,
                    "parameters": {
                        "SMA_WINDOW": 20,
                        "Z_ENTRY": 1.0,
                        "Z_EXIT_THRESHOLD": 0.3
                    }
                }
            )
            
            assert response.status_code in [200, 202]
            results = client.get(f"/api/v1/results/{response.json()['job_id']}").json()
            assert results["initial_capital"] == capital

    def test_invalid_stock_symbol(self):
        """Test with invalid stock symbol"""
        
        response = client.post(
            "/api/v1/backtest",
            json={
                "symbol": "INVALID_STOCK_THAT_DOES_NOT_EXIST",
                "algorithm_id": "mean_reversion",
                "start_date": "2024-01-01",
                "end_date": "2024-01-10",
                "initial_capital": 50000,
                "parameters": {
                    "SMA_WINDOW": 20,
                    "Z_ENTRY": 1.0,
                    "Z_EXIT_THRESHOLD": 0.3
                }
            }
        )
        
        # Should either return 400 or handle gracefully
        assert response.status_code in [200, 400, 422]

    def test_invalid_algorithm(self):
        """Test with invalid algorithm ID"""
        
        response = client.post(
            "/api/v1/backtest",
            json={
                "symbol": "TATVA",
                "algorithm_id": "invalid_algorithm",
                "start_date": "2024-01-01",
                "end_date": "2024-01-10",
                "initial_capital": 50000,
                "parameters": {}
            }
        )
        
        assert response.status_code in [200, 400, 422, 202]

    def test_invalid_date_range(self):
        """Test with invalid date range (end before start)"""
        
        response = client.post(
            "/api/v1/backtest",
            json={
                "symbol": "TATVA",
                "algorithm_id": "mean_reversion",
                "start_date": "2024-01-15",
                "end_date": "2024-01-10",  # End before start!
                "initial_capital": 50000,
                "parameters": {
                    "SMA_WINDOW": 20,
                    "Z_ENTRY": 1.0,
                    "Z_EXIT_THRESHOLD": 0.3
                }
            }
        )
        
        assert response.status_code in [200, 400, 422, 202]

    def test_missing_required_fields(self):
        """Test with missing required fields"""
        
        # Missing capital
        response = client.post(
            "/api/v1/backtest",
            json={
                "symbol": "TATVA",
                "algorithm_id": "mean_reversion",
                "start_date": "2024-01-01",
                "end_date": "2024-01-10",
                # missing capital
                "parameters": {}
            }
        )
        
        assert response.status_code in [422]

    def test_api_endpoints_availability(self):
        """Test that all API endpoints are available"""
        
        # GET /stocks
        response = client.get("/api/v1/stocks")
        assert response.status_code in [200, 202]
        assert isinstance(response.json(), list)
        
        # GET /algorithms
        response = client.get("/api/v1/algorithms")
        assert response.status_code in [200, 202]
        assert isinstance(response.json(), list)
        
        # POST /backtest (tested in other tests)
        # GET /results/{job_id} (tested in other tests)
        # GET /trades/{job_id} (tested in other tests)

    def test_result_metrics_calculation(self):
        """Test that result metrics are calculated correctly"""
        
        response = client.post(
            "/api/v1/backtest",
            json={
                "symbol": "TATVA",
                "algorithm_id": "mean_reversion",
                "start_date": "2024-01-01",
                "end_date": "2024-01-10",
                "initial_capital": 50000,
                "parameters": {
                    "SMA_WINDOW": 20,
                    "Z_ENTRY": 1.0,
                    "Z_EXIT_THRESHOLD": 0.3
                }
            }
        )
        
        job_id = response.json()["job_id"]
        results = client.get(f"/api/v1/results/{job_id}").json()
        
        # Verify metrics make sense
        assert results["initial_capital"] > 0
        assert results["final_capital"] > 0
        assert results["total_trades"] >= 0
        assert "return_percentage" in results
        assert "winning_trades" in results
        assert "losing_trades" in results
        assert results["winning_trades"] + results["losing_trades"] <= results["total_trades"]
        
        # Return percentage should be within reasonable bounds
        return_pct = results["return_percentage"]
        assert -100 <= return_pct <= 1000  # Allow up to 10x return

    def test_trade_log_consistency(self):
        """Test that trade logs are consistent with results"""
        
        response = client.post(
            "/api/v1/backtest",
            json={
                "symbol": "TATVA",
                "algorithm_id": "mean_reversion",
                "start_date": "2024-01-01",
                "end_date": "2024-01-10",
                "initial_capital": 50000,
                "parameters": {
                    "SMA_WINDOW": 20,
                    "Z_ENTRY": 1.0,
                    "Z_EXIT_THRESHOLD": 0.3
                }
            }
        )
        
        job_id = response.json()["job_id"]
        results = client.get(f"/api/v1/results/{job_id}").json()
        trades = client.get(f"/api/v1/trades/{job_id}").json()
        
        # Trade count should match
        assert len(trades) == results["total_trades"]
        
        # PnL sum should be reasonable
        if trades:
            total_pnl = sum(t["pnl"] for t in trades)
            expected_pnl = results["final_capital"] - results["initial_capital"]
            # Allow small difference due to brokerage fees
            assert abs(total_pnl - expected_pnl) < 1000


class TestPerformance:
    """Performance and stress tests"""

    def test_backtest_execution_time(self):
        """Test that backtest execution is reasonably fast"""
        import time
        
        start = time.time()
        
        response = client.post(
            "/api/v1/backtest",
            json={
                "symbol": "TATVA",
                "algorithm_id": "mean_reversion",
                "start_date": "2024-01-01",
                "end_date": "2024-01-10",
                "initial_capital": 50000,
                "parameters": {
                    "SMA_WINDOW": 20,
                    "Z_ENTRY": 1.0,
                    "Z_EXIT_THRESHOLD": 0.3
                }
            }
        )
        
        elapsed = time.time() - start
        
        assert response.status_code in [200, 202]
        # Should complete within 30 seconds
        assert elapsed < 30, f"Backtest took {elapsed:.2f}s (limit: 30s)"

    def test_concurrent_requests(self):
        """Test handling of multiple concurrent requests"""
        import concurrent.futures
        
        def submit_backtest():
            return client.post(
                "/api/v1/backtest",
                json={
                    "symbol": "TATVA",
                    "algorithm_id": "mean_reversion",
                    "start_date": "2024-01-01",
                    "end_date": "2024-01-10",
                    "initial_capital": 50000,
                    "parameters": {
                        "SMA_WINDOW": 20,
                        "Z_ENTRY": 1.0,
                        "Z_EXIT_THRESHOLD": 0.3
                    }
                }
            )
        
        # Submit 5 concurrent requests
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            futures = [executor.submit(submit_backtest) for _ in range(5)]
            results = [f.result() for f in concurrent.futures.as_completed(futures)]
        
        # All should succeed
        assert all(r.status_code == 200 for r in results)
        assert len(results) == 5
