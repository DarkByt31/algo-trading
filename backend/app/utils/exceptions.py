class BacktestException(Exception):
    """Base exception for backtest operations"""
    pass


class InvalidParametersException(BacktestException):
    """Raised when algorithm parameters are invalid"""
    pass


class AlgorithmNotFound(BacktestException):
    """Raised when algorithm is not found"""
    pass


class DataFetchException(BacktestException):
    """Raised when data fetching fails"""
    pass


class BacktestExecutionException(BacktestException):
    """Raised when backtest execution fails"""
    pass
