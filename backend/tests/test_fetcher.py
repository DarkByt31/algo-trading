import pytest
import sys
from pathlib import Path
from datetime import datetime, timedelta
import pandas as pd

sys.path.insert(0, str(Path(__file__).parent.parent))

from app.core.data.fetcher import MockDataFetcher


class TestMockDataFetcher:
    """Test suite for Mock Data Fetcher"""
    
    def test_mock_fetcher_initialization(self):
        """Test mock fetcher initializes"""
        fetcher = MockDataFetcher()
        assert fetcher is not None
    
    def test_mock_fetcher_generates_data(self):
        """Test mock fetcher generates data"""
        fetcher = MockDataFetcher()
        from_date = datetime(2026, 1, 1)
        to_date = datetime(2026, 1, 5)
        
        df = fetcher.fetch_historical_data(
            symbol="RELIANCE",
            from_date=from_date,
            to_date=to_date
        )
        
        assert isinstance(df, pd.DataFrame)
        assert len(df) > 0
    
    def test_mock_fetcher_returns_required_columns(self):
        """Test mock fetcher returns required columns"""
        fetcher = MockDataFetcher()
        from_date = datetime(2026, 1, 1)
        to_date = datetime(2026, 1, 5)
        
        df = fetcher.fetch_historical_data(
            symbol="RELIANCE",
            from_date=from_date,
            to_date=to_date
        )
        
        required_cols = ['datetime', 'close', 'open', 'high', 'low', 'volume']
        for col in required_cols:
            assert col in df.columns, f"Missing column: {col}"
    
    def test_mock_fetcher_datetime_format(self):
        """Test mock fetcher returns correct datetime format"""
        fetcher = MockDataFetcher()
        from_date = datetime(2026, 1, 1)
        to_date = datetime(2026, 1, 5)
        
        df = fetcher.fetch_historical_data(
            symbol="RELIANCE",
            from_date=from_date,
            to_date=to_date
        )
        
        assert pd.api.types.is_datetime64_any_dtype(df['datetime'])
    
    def test_mock_fetcher_respects_date_range(self):
        """Test mock fetcher respects date range"""
        fetcher = MockDataFetcher()
        from_date = datetime(2026, 1, 1, 9, 15)
        to_date = datetime(2026, 1, 5, 15, 30)
        
        df = fetcher.fetch_historical_data(
            symbol="RELIANCE",
            from_date=from_date,
            to_date=to_date
        )
        
        min_date = df['datetime'].min()
        max_date = df['datetime'].max()
        
        assert min_date >= from_date
        assert max_date <= to_date
    
    def test_mock_fetcher_market_hours_filter(self):
        """Test mock fetcher filters market hours (9:15 - 15:30)"""
        from datetime import time as datetime_time
        fetcher = MockDataFetcher()
        from_date = datetime(2026, 1, 1)
        to_date = datetime(2026, 1, 5)
        
        df = fetcher.fetch_historical_data(
            symbol="RELIANCE",
            from_date=from_date,
            to_date=to_date
        )
        
        # All times should be between 9:15 and 15:30
        times = df['datetime'].dt.time
        assert all(t >= datetime_time(9, 15) for t in times)
        assert all(t <= datetime_time(15, 30) for t in times)
    
    def test_mock_fetcher_weekdays_only(self):
        """Test mock fetcher filters weekends"""
        fetcher = MockDataFetcher()
        from_date = datetime(2026, 1, 1)
        to_date = datetime(2026, 1, 10)  # Includes weekend
        
        df = fetcher.fetch_historical_data(
            symbol="RELIANCE",
            from_date=from_date,
            to_date=to_date
        )
        
        # Check only weekdays (0-4, Monday-Friday)
        weekdays = df['datetime'].dt.weekday
        assert all(wd < 5 for wd in weekdays)
    
    def test_mock_fetcher_data_is_sorted(self):
        """Test mock fetcher returns sorted data"""
        fetcher = MockDataFetcher()
        from_date = datetime(2026, 1, 1)
        to_date = datetime(2026, 1, 5)
        
        df = fetcher.fetch_historical_data(
            symbol="RELIANCE",
            from_date=from_date,
            to_date=to_date
        )
        
        # Check data is sorted by datetime
        assert df['datetime'].is_monotonic_increasing
    
    def test_mock_fetcher_price_relationships(self):
        """Test mock fetcher generates realistic price relationships"""
        fetcher = MockDataFetcher()
        from_date = datetime(2026, 1, 1)
        to_date = datetime(2026, 1, 5)
        
        df = fetcher.fetch_historical_data(
            symbol="RELIANCE",
            from_date=from_date,
            to_date=to_date
        )
        
        # High should be >= close and >= open
        assert (df['high'] >= df['close']).all()
        assert (df['high'] >= df['open']).all()
        
        # Low should be <= close and <= open
        assert (df['low'] <= df['close']).all()
        assert (df['low'] <= df['open']).all()
    
    def test_mock_fetcher_volume_positive(self):
        """Test mock fetcher generates positive volume"""
        fetcher = MockDataFetcher()
        from_date = datetime(2026, 1, 1)
        to_date = datetime(2026, 1, 5)
        
        df = fetcher.fetch_historical_data(
            symbol="RELIANCE",
            from_date=from_date,
            to_date=to_date
        )
        
        assert (df['volume'] > 0).all()
    
    def test_mock_fetcher_different_symbols(self):
        """Test mock fetcher works with different symbols"""
        fetcher = MockDataFetcher()
        from_date = datetime(2026, 1, 1)
        to_date = datetime(2026, 1, 5)
        
        df1 = fetcher.fetch_historical_data("RELIANCE", from_date, to_date)
        df2 = fetcher.fetch_historical_data("VOLTAS", from_date, to_date)
        
        assert len(df1) > 0
        assert len(df2) > 0
        # Different symbols should generate different prices
        assert not df1['close'].equals(df2['close'])
