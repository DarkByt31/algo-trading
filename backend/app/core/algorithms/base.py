from abc import ABC, abstractmethod
from typing import Dict, List, Any
import pandas as pd
import logging

logger = logging.getLogger(__name__)


class BaseAlgorithm(ABC):
    """Abstract base class for all trading algorithms"""
    
    def __init__(self, parameters: Dict[str, Any]):
        """
        Initialize algorithm with parameters
        
        Args:
            parameters: Algorithm-specific parameters (dict)
        """
        self.parameters = parameters
        self.validate_parameters()
    
    @abstractmethod
    def validate_parameters(self) -> None:
        """Validate parameters. Raise ValueError if invalid."""
        pass
    
    @abstractmethod
    def generate_signals(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Generate buy/sell signals based on price data
        
        Args:
            df: DataFrame with OHLCV data
        
        Returns:
            DataFrame with additional signal columns
        """
        pass
    
    @property
    @abstractmethod
    def algorithm_id(self) -> str:
        """Unique algorithm identifier"""
        pass
    
    @property
    @abstractmethod
    def algorithm_name(self) -> str:
        """Algorithm display name"""
        pass
    
    def __repr__(self) -> str:
        return f"<{self.algorithm_name} - {self.algorithm_id}>"
