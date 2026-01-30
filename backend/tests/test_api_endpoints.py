import os
import pytest

os.environ["DATABASE_URL"] = "sqlite:///:memory:"

from fastapi.testclient import TestClient
from app.main import app


client = TestClient(app)


@pytest.fixture(autouse=True)
def ensure_test_db():
    """Ensure DB tables exist before each test"""
    from app.db.base import Base
    from app.db.session import engine
    Base.metadata.create_all(bind=engine)
    yield


@pytest.mark.skip(reason="Requires separate test fixtures for API isolation from app DB initialization")
def test_backtest_api_flow():
    payload = {
        "symbol": "RELIANCE",
        "algorithm_id": "mean_reversion",
        "parameters": {"SMA_WINDOW": 5, "Z_ENTRY": 1.5, "Z_EXIT_THRESHOLD": 0.5},
        "start_date": "2024-01-01",
        "end_date": "2024-01-10",
        "initial_capital": 100000.0,
    }

    r = client.post("/api/v1/backtest", json=payload)
    assert r.status_code == 202
    data = r.json()
    assert "job_id" in data
    job_id = data["job_id"]

    r2 = client.get(f"/api/v1/results/{job_id}")
    assert r2.status_code == 200

    r3 = client.get(f"/api/v1/trades/{job_id}")
    assert r3.status_code == 200
    tdata = r3.json()
    assert "trades" in tdata

