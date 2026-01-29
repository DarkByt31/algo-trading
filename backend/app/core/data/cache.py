import logging
from typing import Dict, Optional
from datetime import datetime
import pandas as pd

logger = logging.getLogger(__name__)


class DataCache:
    """In-memory cache for historical data"""
    
    def __init__(self, max_age_hours: int = 24):
        """
        Initialize cache
        
        Args:
            max_age_hours: Maximum age of cached data in hours
        """
        self.cache: Dict[str, dict] = {}
        self.max_age_hours = max_age_hours
    
    def _generate_key(self, symbol: str, from_date: datetime, to_date: datetime, interval: str) -> str:
        """Generate cache key"""
        return f"{symbol}_{interval}_{from_date.date()}_{to_date.date()}"
    
    def get(self, symbol: str, from_date: datetime, to_date: datetime, interval: str = "5minute") -> Optional[pd.DataFrame]:
        """Get data from cache if available and not expired"""
        key = self._generate_key(symbol, from_date, to_date, interval)
        
        if key not in self.cache:
            logger.debug(f"Cache miss for {key}")
            return None
        
        cached_data = self.cache[key]
        age_hours = (datetime.now() - cached_data['timestamp']).total_seconds() / 3600
        
        if age_hours > self.max_age_hours:
            logger.info(f"Cache expired for {key}")
            del self.cache[key]
            return None
        
        logger.info(f"Cache hit for {key}")
        return cached_data['data'].copy()
    
    def set(self, symbol: str, from_date: datetime, to_date: datetime, data: pd.DataFrame, interval: str = "5minute") -> None:
        """Store data in cache"""
        key = self._generate_key(symbol, from_date, to_date, interval)
        self.cache[key] = {
            'data': data.copy(),
            'timestamp': datetime.now()
        }
        logger.info(f"Cached {len(data)} rows for {key}")
    
    def clear(self) -> None:
        """Clear all cache"""
        self.cache.clear()
        logger.info("Cache cleared")
    
    def get_cache_stats(self) -> dict:
        """Get cache statistics"""
        total_rows = sum(len(item['data']) for item in self.cache.values())
        return {
            'entries': len(self.cache),
            'total_rows': total_rows,
            'keys': list(self.cache.keys())
        }


# Global cache instance
_cache = DataCache()


def get_cache() -> DataCache:
    """Get global cache instance"""
    return _cache
