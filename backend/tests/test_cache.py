import pytest
import sys
from pathlib import Path
from datetime import datetime, timedelta
import time

sys.path.insert(0, str(Path(__file__).parent.parent))

from app.core.data.cache import DataCache
from tests.conftest import sample_dataframe


class TestDataCache:
    """Test suite for in-memory data cache"""
    
    def test_cache_initialization(self):
        """Test cache initializes empty"""
        cache = DataCache()
        assert len(cache.cache) == 0
    
    def test_cache_set_and_get(self, sample_dataframe):
        """Test setting and getting data from cache"""
        cache = DataCache(max_age_hours=24)
        
        from_date = datetime(2026, 1, 1)
        to_date = datetime(2026, 1, 2)
        
        cache.set("RELIANCE", from_date, to_date, sample_dataframe)
        result = cache.get("RELIANCE", from_date, to_date)
        
        assert result is not None
        assert len(result) == len(sample_dataframe)
    
    def test_cache_miss_returns_none(self, sample_dataframe):
        """Test cache returns None on miss"""
        cache = DataCache()
        from_date = datetime(2026, 1, 1)
        to_date = datetime(2026, 1, 2)
        
        result = cache.get("NONEXISTENT", from_date, to_date)
        assert result is None
    
    def test_cache_key_generation(self):
        """Test cache key is generated correctly"""
        cache = DataCache()
        key = cache._generate_key("RELIANCE", datetime(2026, 1, 1), datetime(2026, 1, 2), "5minute")
        
        assert "RELIANCE" in key
        assert "5minute" in key
        assert "2026-01-01" in key
        assert "2026-01-02" in key
    
    def test_cache_different_symbols_separate(self, sample_dataframe):
        """Test different symbols are cached separately"""
        cache = DataCache()
        from_date = datetime(2026, 1, 1)
        to_date = datetime(2026, 1, 2)
        
        cache.set("RELIANCE", from_date, to_date, sample_dataframe)
        cache.set("VOLTAS", from_date, to_date, sample_dataframe)
        
        assert cache.get("RELIANCE", from_date, to_date) is not None
        assert cache.get("VOLTAS", from_date, to_date) is not None
        assert len(cache.cache) == 2
    
    def test_cache_different_dates_separate(self, sample_dataframe):
        """Test different date ranges are cached separately"""
        cache = DataCache()
        from_date1 = datetime(2026, 1, 1)
        to_date1 = datetime(2026, 1, 2)
        from_date2 = datetime(2026, 1, 3)
        to_date2 = datetime(2026, 1, 4)
        
        cache.set("RELIANCE", from_date1, to_date1, sample_dataframe)
        cache.set("RELIANCE", from_date2, to_date2, sample_dataframe)
        
        assert len(cache.cache) == 2
    
    def test_cache_expiry(self, sample_dataframe):
        """Test cache expiry"""
        cache = DataCache(max_age_hours=0)  # Expire immediately
        from_date = datetime(2026, 1, 1)
        to_date = datetime(2026, 1, 2)
        
        cache.set("RELIANCE", from_date, to_date, sample_dataframe)
        time.sleep(0.1)  # Small delay
        
        result = cache.get("RELIANCE", from_date, to_date)
        assert result is None
    
    def test_cache_clear(self, sample_dataframe):
        """Test cache clear"""
        cache = DataCache()
        from_date = datetime(2026, 1, 1)
        to_date = datetime(2026, 1, 2)
        
        cache.set("RELIANCE", from_date, to_date, sample_dataframe)
        assert len(cache.cache) > 0
        
        cache.clear()
        assert len(cache.cache) == 0
    
    def test_cache_stats(self, sample_dataframe):
        """Test cache statistics"""
        cache = DataCache()
        from_date = datetime(2026, 1, 1)
        to_date = datetime(2026, 1, 2)
        
        cache.set("RELIANCE", from_date, to_date, sample_dataframe)
        stats = cache.get_cache_stats()
        
        assert stats['entries'] == 1
        assert stats['total_rows'] == len(sample_dataframe)
        assert len(stats['keys']) == 1
    
    def test_cache_get_returns_copy(self, sample_dataframe):
        """Test cache returns copy, not reference"""
        cache = DataCache()
        from_date = datetime(2026, 1, 1)
        to_date = datetime(2026, 1, 2)
        
        cache.set("RELIANCE", from_date, to_date, sample_dataframe)
        result1 = cache.get("RELIANCE", from_date, to_date)
        result2 = cache.get("RELIANCE", from_date, to_date)
        
        # Modify result1
        result1['close'].iloc[0] = 9999
        
        # result2 should not be modified
        assert result2['close'].iloc[0] != 9999
