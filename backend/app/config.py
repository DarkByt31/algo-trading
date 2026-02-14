import os
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application configuration"""
    
    # Database
    DATABASE_URL: str = "mysql+pymysql://root:password@localhost:3306/algo_trading"
    
    # Kite Connect API
    KITE_API_KEY: str = ""
    KITE_API_SECRET: str = ""
    KITE_ACCESS_TOKEN: str = ""
    
    # App
    DEBUG: bool = True
    LOG_LEVEL: str = "DEBUG"
    APP_NAME: str = "Trading Backtester API"
    API_VERSION: str = "v1"
    
    # Backtest constraints
    MAX_BACKTEST_DAYS: int = 90  # 3 months
    DEFAULT_INTERVAL: str = "5minute"
    # CORS
    # Comma-separated list of allowed origins, e.g. "http://localhost,http://localhost:8000"
    ALLOWED_ORIGINS: str = "http://localhost,http://127.0.0.1,http://localhost:8000"
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
