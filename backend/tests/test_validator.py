import pytest
import sys
from pathlib import Path
from datetime import datetime, timedelta

sys.path.insert(0, str(Path(__file__).parent.parent))

from app.core.backtest.validator import ParameterValidator


class TestParameterValidator:
    """Test suite for parameter validation"""
    
    def test_validate_date_range_valid(self):
        """Test valid date range passes"""
        start = datetime(2026, 1, 1)
        end = datetime(2026, 1, 15)
        # Should not raise
        ParameterValidator.validate_date_range(start, end)
    
    def test_validate_date_range_start_after_end(self):
        """Test start_date after end_date raises error"""
        start = datetime(2026, 1, 15)
        end = datetime(2026, 1, 1)
        
        with pytest.raises(ValueError, match="start_date must be before end_date"):
            ParameterValidator.validate_date_range(start, end)
    
    def test_validate_date_range_same_dates(self):
        """Test same start and end dates raises error"""
        start = datetime(2026, 1, 1)
        end = datetime(2026, 1, 1)
        
        with pytest.raises(ValueError, match="start_date must be before end_date"):
            ParameterValidator.validate_date_range(start, end)
    
    def test_validate_date_range_exceeds_max_days(self):
        """Test date range exceeding max days raises error"""
        start = datetime(2026, 1, 1)
        end = datetime(2026, 5, 1)  # 120 days, exceeds 90 day limit
        
        with pytest.raises(ValueError, match="Date range exceeds maximum"):
            ParameterValidator.validate_date_range(start, end, max_days=90)
    
    def test_validate_date_range_at_max_boundary(self):
        """Test date range exactly at max days passes"""
        start = datetime(2026, 1, 1)
        end = datetime(2026, 3, 31)  # Exactly 90 days
        # Should not raise
        ParameterValidator.validate_date_range(start, end, max_days=90)
    
    def test_validate_capital_valid(self):
        """Test valid capital passes"""
        # Should not raise
        ParameterValidator.validate_capital(50000)
    
    def test_validate_capital_zero(self):
        """Test zero capital raises error"""
        with pytest.raises(ValueError, match="Initial capital must be positive"):
            ParameterValidator.validate_capital(0)
    
    def test_validate_capital_negative(self):
        """Test negative capital raises error"""
        with pytest.raises(ValueError, match="Initial capital must be positive"):
            ParameterValidator.validate_capital(-1000)
    
    def test_validate_capital_exceeds_max(self):
        """Test capital exceeding max raises error"""
        with pytest.raises(ValueError, match="exceeds maximum limit"):
            ParameterValidator.validate_capital(11000000)
    
    def test_validate_capital_at_max_boundary(self):
        """Test capital at max boundary passes"""
        # Should not raise
        ParameterValidator.validate_capital(10000000)
    
    def test_validate_brokerage_valid(self):
        """Test valid brokerage passes"""
        # Should not raise
        ParameterValidator.validate_brokerage(20)
    
    def test_validate_brokerage_zero(self):
        """Test zero brokerage passes"""
        # Should not raise
        ParameterValidator.validate_brokerage(0)
    
    def test_validate_brokerage_negative(self):
        """Test negative brokerage raises error"""
        with pytest.raises(ValueError, match="between 0 and 1000"):
            ParameterValidator.validate_brokerage(-10)
    
    def test_validate_brokerage_exceeds_max(self):
        """Test brokerage exceeding max raises error"""
        with pytest.raises(ValueError, match="between 0 and 1000"):
            ParameterValidator.validate_brokerage(2000)
    
    def test_validate_brokerage_at_max_boundary(self):
        """Test brokerage at max boundary passes"""
        # Should not raise
        ParameterValidator.validate_brokerage(1000)
    
    def test_validate_all_parameters_together(self):
        """Test validating all parameters together"""
        start = datetime(2026, 1, 1)
        end = datetime(2026, 1, 15)
        capital = 50000
        brokerage = 20
        
        # All should pass without raising
        ParameterValidator.validate_date_range(start, end)
        ParameterValidator.validate_capital(capital)
        ParameterValidator.validate_brokerage(brokerage)
