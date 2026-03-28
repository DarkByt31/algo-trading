import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from app.utils.exceptions import (
    BacktestException,
    InvalidParametersException,
    AlgorithmNotFound,
    DataFetchException,
    BacktestExecutionException
)


class TestExceptions:
    """Test suite for custom exceptions"""
    
    def test_backtest_exception_inherits_exception(self):
        """Test BacktestException inherits from Exception"""
        assert issubclass(BacktestException, Exception)
    
    def test_invalid_parameters_exception_inherits_backtest_exception(self):
        """Test InvalidParametersException inherits from BacktestException"""
        assert issubclass(InvalidParametersException, BacktestException)
    
    def test_algorithm_not_found_exception_inherits_backtest_exception(self):
        """Test AlgorithmNotFound inherits from BacktestException"""
        assert issubclass(AlgorithmNotFound, BacktestException)
    
    def test_data_fetch_exception_inherits_backtest_exception(self):
        """Test DataFetchException inherits from BacktestException"""
        assert issubclass(DataFetchException, BacktestException)
    
    def test_backtest_execution_exception_inherits_backtest_exception(self):
        """Test BacktestExecutionException inherits from BacktestException"""
        assert issubclass(BacktestExecutionException, BacktestException)
    
    def test_raise_invalid_parameters_exception(self):
        """Test raising InvalidParametersException"""
        with pytest.raises(InvalidParametersException):
            raise InvalidParametersException("Invalid params")
    
    def test_raise_algorithm_not_found(self):
        """Test raising AlgorithmNotFound"""
        with pytest.raises(AlgorithmNotFound):
            raise AlgorithmNotFound("Algorithm not found")
    
    def test_raise_data_fetch_exception(self):
        """Test raising DataFetchException"""
        with pytest.raises(DataFetchException):
            raise DataFetchException("Data fetch failed")
    
    def test_raise_backtest_execution_exception(self):
        """Test raising BacktestExecutionException"""
        with pytest.raises(BacktestExecutionException):
            raise BacktestExecutionException("Execution failed")
    
    def test_exception_message(self):
        """Test exception carries message"""
        msg = "Test error message"
        try:
            raise BacktestException(msg)
        except BacktestException as e:
            assert str(e) == msg
