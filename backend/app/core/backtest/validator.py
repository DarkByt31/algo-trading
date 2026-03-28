import logging
from typing import Dict, List, Any
from datetime import datetime
import pandas as pd

logger = logging.getLogger(__name__)


class ParameterValidator:
    """Validates backtest parameters"""
    
    @staticmethod
    def validate_date_range(start_date: datetime, end_date: datetime, max_days: int = 90) -> None:
        """Validate date range"""
        if start_date >= end_date:
            raise ValueError("start_date must be before end_date")
        
        days_diff = (end_date - start_date).days
        if days_diff > max_days:
            raise ValueError(f"Date range exceeds maximum of {max_days} days (requested: {days_diff})")
        
        logger.info(f"Date range valid: {days_diff} days")
    
    @staticmethod
    def validate_capital(capital: float) -> None:
        """Validate initial capital"""
        if capital <= 0:
            raise ValueError("Initial capital must be positive")
        
        if capital > 10000000:  # Max 1 crore
            raise ValueError("Initial capital exceeds maximum limit")
        
        logger.info(f"Capital valid: ₹{capital}")
    
    @staticmethod
    def validate_brokerage(brokerage: float) -> None:
        """Validate brokerage fee"""
        if brokerage < 0 or brokerage > 1000:
            raise ValueError("Brokerage fee must be between 0 and 1000")
        
        logger.info(f"Brokerage valid: ₹{brokerage}")
