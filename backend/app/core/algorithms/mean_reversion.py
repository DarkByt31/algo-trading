from typing import Dict, Any
import pandas as pd
import logging
from app.core.algorithms.base import BaseAlgorithm

logger = logging.getLogger(__name__)


class MeanReversionAlgorithm(BaseAlgorithm):
    """Mean Reversion Trading Algorithm"""
    
    @property
    def algorithm_id(self) -> str:
        return "mean_reversion"
    
    @property
    def algorithm_name(self) -> str:
        return "Mean Reversion"
    
    def validate_parameters(self) -> None:
        """Validate algorithm parameters"""
        required = ['SMA_WINDOW', 'Z_ENTRY', 'Z_EXIT_THRESHOLD']
        for param in required:
            if param not in self.parameters:
                raise ValueError(f"Missing required parameter: {param}")
        
        sma_window = self.parameters['SMA_WINDOW']
        z_entry = self.parameters['Z_ENTRY']
        z_exit = self.parameters['Z_EXIT_THRESHOLD']
        
        if not isinstance(sma_window, int) or sma_window < 5 or sma_window > 100:
            raise ValueError(f"SMA_WINDOW must be int between 5-100, got {sma_window}")
        
        if not isinstance(z_entry, (int, float)) or z_entry < 0.5 or z_entry > 3.0:
            raise ValueError(f"Z_ENTRY must be float between 0.5-3.0, got {z_entry}")
        
        if not isinstance(z_exit, (int, float)) or z_exit < 0.1 or z_exit > 1.0:
            raise ValueError(f"Z_EXIT_THRESHOLD must be float between 0.1-1.0, got {z_exit}")
        
        logger.info(f"Parameters validated: {self.parameters}")
    
    def generate_signals(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Generate mean reversion signals
        
        Algorithm:
        1. Calculate SMA (Simple Moving Average)
        2. Calculate Z-score: (price - SMA) / std_dev
        3. BUY signal when Z-score crosses below -Z_ENTRY (price too low)
        4. SELL signal when Z-score crosses above +Z_ENTRY (price too high)
        5. EXIT when Z-score reverts toward zero
        """
        df = df.copy()
        
        sma_window = self.parameters['SMA_WINDOW']
        z_entry = self.parameters['Z_ENTRY']
        z_exit = self.parameters['Z_EXIT_THRESHOLD']
        
        # Calculate SMA and Z-score
        df['sma'] = df['close'].rolling(window=sma_window).mean()
        df['std'] = df['close'].rolling(window=sma_window).std()
        df['z_score'] = (df['close'] - df['sma']) / df['std']
        
        # Initialize signals
        df['signal'] = 'HOLD'
        
        # Detect local extrema for signals
        for i in range(2, len(df)):
            z_prev2 = df.loc[i - 2, 'z_score']
            z_prev1 = df.loc[i - 1, 'z_score']
            z_curr = df.loc[i, 'z_score']
            
            # Local maximum (SELL): price extended too high
            if z_prev2 < z_prev1 > z_curr and z_curr > z_entry:
                df.loc[i, 'signal'] = 'SELL'
            
            # Local minimum (BUY): price extended too low
            elif z_prev2 > z_prev1 < z_curr and z_curr < -z_entry:
                df.loc[i, 'signal'] = 'BUY'
        
        # Shift signal to avoid forward bias (execute on next candle)
        df['position'] = df['signal'].shift(1).fillna('HOLD')
        
        logger.info(f"Generated signals for {len(df)} candles")
        
        return df.dropna(subset=['z_score'])
