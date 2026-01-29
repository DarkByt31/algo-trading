import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from app.config import settings
from app.db.session import SessionLocal, get_db, engine
from app.db.base import Base
from app.db.models import Algorithm, BacktestJob, BacktestResult, Trade


class TestDatabaseConfiguration:
    """Test suite for database configuration"""
    
    def test_settings_loaded(self):
        """Test settings are loaded"""
        assert settings.DATABASE_URL is not None
        assert settings.APP_NAME == "Trading Backtester API"
    
    def test_database_connection(self, test_db):
        """Test database connection"""
        # test_db fixture from conftest ensures connection works
        assert test_db is not None
    
    def test_session_creation(self, db_session):
        """Test database session creation"""
        assert db_session is not None
    
    def test_models_defined(self):
        """Test all models are properly defined"""
        models = [Algorithm, BacktestJob, BacktestResult, Trade]
        for model in models:
            assert hasattr(model, '__tablename__')
    
    def test_algorithm_model_columns(self):
        """Test Algorithm model has required columns"""
        assert hasattr(Algorithm, 'id')
        assert hasattr(Algorithm, 'name')
        assert hasattr(Algorithm, 'parameters')
        assert hasattr(Algorithm, 'is_active')
    
    def test_backtest_job_model_columns(self):
        """Test BacktestJob model has required columns"""
        assert hasattr(BacktestJob, 'id')
        assert hasattr(BacktestJob, 'symbol')
        assert hasattr(BacktestJob, 'algorithm_id')
        assert hasattr(BacktestJob, 'status')
    
    def test_backtest_result_model_columns(self):
        """Test BacktestResult model has required columns"""
        assert hasattr(BacktestResult, 'id')
        assert hasattr(BacktestResult, 'job_id')
        assert hasattr(BacktestResult, 'final_capital')
        assert hasattr(BacktestResult, 'total_return')
    
    def test_trade_model_columns(self):
        """Test Trade model has required columns"""
        assert hasattr(Trade, 'id')
        assert hasattr(Trade, 'job_id')
        assert hasattr(Trade, 'trade_type')
        assert hasattr(Trade, 'price')
        assert hasattr(Trade, 'quantity')


class TestDatabaseOperations:
    """Test suite for database operations"""
    
    def test_create_algorithm(self, db_session):
        """Test creating algorithm record"""
        algo = Algorithm(
            id="test_algo",
            name="Test Algorithm",
            description="Test description",
            parameters=[{"name": "param1", "default": 1}]
        )
        db_session.add(algo)
        db_session.commit()
        
        retrieved = db_session.query(Algorithm).filter_by(id="test_algo").first()
        assert retrieved is not None
        assert retrieved.name == "Test Algorithm"
    
    def test_create_backtest_job(self, db_session):
        """Test creating backtest job record"""
        from datetime import date
        job = BacktestJob(
            id="job123",
            symbol="RELIANCE",
            algorithm_id="mean_reversion",
            parameters={"SMA_WINDOW": 20},
            start_date=date(2026, 1, 1),
            end_date=date(2026, 1, 15),
            initial_capital=50000,
            status="completed"
        )
        db_session.add(job)
        db_session.commit()
        
        retrieved = db_session.query(BacktestJob).filter_by(id="job123").first()
        assert retrieved is not None
        assert retrieved.symbol == "RELIANCE"
    
    def test_create_backtest_result(self, db_session):
        """Test creating backtest result record"""
        result = BacktestResult(
            id="result123",
            job_id="job123",
            final_capital=52000,
            total_return=2000,
            return_percentage=4.0,
            total_trades=10
        )
        db_session.add(result)
        db_session.commit()
        
        retrieved = db_session.query(BacktestResult).filter_by(id="result123").first()
        assert retrieved is not None
        assert retrieved.final_capital == 52000
    
    def test_create_trade(self, db_session):
        """Test creating trade record"""
        from datetime import datetime
        trade = Trade(
            id="trade123",
            job_id="job123",
            trade_sequence=1,
            trade_type="BUY",
            symbol="RELIANCE",
            trade_time=datetime(2026, 1, 1, 10, 30, 0),
            price=2500,
            quantity=20,
            capital_after=49999
        )
        db_session.add(trade)
        db_session.commit()
        
        retrieved = db_session.query(Trade).filter_by(id="trade123").first()
        assert retrieved is not None
        assert retrieved.trade_type == "BUY"
