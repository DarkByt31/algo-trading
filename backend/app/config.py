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
    LOG_LEVEL: str = "INFO"
    APP_NAME: str = "Trading Backtester API"
    API_VERSION: str = "v1"
    
    # Backtest constraints
    MAX_BACKTEST_DAYS: int = 90  # 3 months
    DEFAULT_INTERVAL: str = "5minute"
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
