import logging
from typing import Optional
from datetime import datetime, timedelta
import pandas as pd
from kiteconnect import KiteConnect
from app.config import settings

logger = logging.getLogger(__name__)


class DataFetcher:
    """Fetches historical data from Kite Connect API"""
    
    def __init__(self, api_key: str = None, api_secret: str = None, access_token: str = None):
        """Initialize Kite Connect client"""
        self.api_key = api_key or settings.KITE_API_KEY
        self.api_secret = api_secret or settings.KITE_API_SECRET
        self.access_token = access_token or settings.KITE_ACCESS_TOKEN
        
        self.kite = KiteConnect(api_key=self.api_key)
        if self.access_token:
            self.kite.set_access_token(self.access_token)
    
    def get_instrument_token(self, symbol: str, exchange: str = "NSE") -> int:
        """Get instrument token for a symbol"""
        try:
            instruments = self.kite.instruments(exchange)
            for instrument in instruments:
                if instrument['tradingsymbol'] == symbol:
                    return instrument['instrument_token']
            raise ValueError(f"Symbol {symbol} not found in {exchange}")
        except Exception as e:
            logger.error(f"Error fetching instrument token for {symbol}: {e}")
            raise
    
    def fetch_historical_data(
        self,
        symbol: str,
        from_date: datetime,
        to_date: datetime,
        interval: str = "5minute",
        exchange: str = "NSE"
    ) -> pd.DataFrame:
        """
        Fetch historical data from Kite API
        
        Args:
            symbol: Stock symbol (e.g., 'RELIANCE')
            from_date: Start date
            to_date: End date
            interval: Candle interval ('5minute', '15minute', etc.)
            exchange: Exchange name ('NSE', 'BSE')
        
        Returns:
            DataFrame with columns: datetime, close, open, high, low, volume
        """
        try:
            token = self.get_instrument_token(symbol, exchange)
            logger.info(f"Fetching data for {symbol} from {from_date} to {to_date}")
            
            data = self.kite.historical_data(token, from_date, to_date, interval)
            
            if not data:
                logger.warning(f"No data returned for {symbol}")
                return pd.DataFrame()
            
            df = pd.DataFrame(data)
            df['datetime'] = pd.to_datetime(df['date'])
            df = df[['datetime', 'close', 'open', 'high', 'low', 'volume']]
            
            # Filter for market hours (9:15 AM - 3:30 PM)
            market_open = datetime.time(9, 15)
            market_close = datetime.time(15, 30)
            df = df[(df['datetime'].dt.time >= market_open) & 
                    (df['datetime'].dt.time <= market_close)]
            
            df = df.sort_values('datetime').reset_index(drop=True)
            logger.info(f"Fetched {len(df)} candles for {symbol}")
            
            return df
        
        except Exception as e:
            logger.error(f"Error fetching historical data: {e}")
            raise


class MockDataFetcher(DataFetcher):
    """Mock data fetcher for testing without API credentials"""
    
    def fetch_historical_data(
        self,
        symbol: str,
        from_date: datetime,
        to_date: datetime,
        interval: str = "5minute",
        exchange: str = "NSE"
    ) -> pd.DataFrame:
        """Generate mock historical data"""
        import numpy as np
        from datetime import time as datetime_time
        
        logger.info(f"Generating mock data for {symbol}")
        
        # Generate dates with 5-minute intervals during market hours
        dates = []
        current = from_date.replace(hour=9, minute=15, second=0, microsecond=0)
        
        while current <= to_date:
            if current.weekday() < 5 and current.time() >= datetime_time(9, 15) and current.time() <= datetime_time(15, 30):
                dates.append(current)
            current += timedelta(minutes=5)
        
        # Generate realistic OHLCV data
        n = len(dates)
        base_price = 2500
        close_prices = base_price + np.cumsum(np.random.randn(n) * 5)
        
        # Generate realistic OHLC relationships
        open_prices = close_prices + np.random.randn(n) * 2
        high_prices = np.maximum.reduce([open_prices, close_prices]) + np.abs(np.random.randn(n) * 2)
        low_prices = np.minimum.reduce([open_prices, close_prices]) - np.abs(np.random.randn(n) * 2)
        
        df = pd.DataFrame({
            'datetime': dates,
            'close': close_prices,
            'open': open_prices,
            'high': high_prices,
            'low': low_prices,
            'volume': np.random.randint(1000, 100000, n)
        })
        
        return df.sort_values('datetime').reset_index(drop=True)
