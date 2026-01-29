import pytest
import sys
from pathlib import Path
from datetime import datetime, timedelta
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.db.base import Base
from app.db.models import Algorithm, BacktestJob, BacktestResult, Trade


@pytest.fixture(scope="session")
def test_db():
    """Create test database"""
    # Use SQLite for testing
    DATABASE_URL = "sqlite:///:memory:"
    engine = create_engine(
        DATABASE_URL, 
        connect_args={"check_same_thread": False}
    )
    Base.metadata.create_all(bind=engine)
    yield engine


@pytest.fixture
def db_session(test_db):
    """Create database session for tests"""
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_db)
    session = TestingSessionLocal()
    yield session
    session.close()


@pytest.fixture
def sample_dataframe():
    """Create sample OHLCV data"""
    dates = pd.date_range(start='2026-01-01 09:15', periods=100, freq='5min')
    prices = 2500 + (pd.Series(range(100)) * 0.5)
    
    df = pd.DataFrame({
        'datetime': dates,
        'close': prices,
        'open': prices + 1,
        'high': prices + 2,
        'low': prices - 1,
        'volume': [10000] * 100
    })
    return df


@pytest.fixture
def algorithm_params():
    """Standard algorithm parameters"""
    return {
        'SMA_WINDOW': 20,
        'Z_ENTRY': 1.0,
        'Z_EXIT_THRESHOLD': 0.3
    }
