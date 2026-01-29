from sqlalchemy import Column, String, Date, Numeric, Boolean, Enum, DateTime, JSON, Integer, Text, func
from datetime import datetime
import uuid
from app.db.base import Base


class BacktestJob(Base):
    """Backtest execution requests"""
    __tablename__ = "backtest_jobs"
    
    id = Column(String(36), primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    symbol = Column(String(20), nullable=False, index=True)
    algorithm_id = Column(String(50), nullable=False, index=True)
    parameters = Column(JSON, nullable=False)  # Algorithm-specific parameters
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    initial_capital = Column(Numeric(12, 2), nullable=False)
    allow_short = Column(Boolean, default=True)
    brokerage_fee = Column(Numeric(8, 2), default=20)
    status = Column(Enum('queued', 'processing', 'completed', 'failed'), default='queued', index=True)
    error_message = Column(Text, nullable=True)
    execution_time_ms = Column(Integer, nullable=True)
    created_at = Column(DateTime, default=func.now(), index=True)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    def __repr__(self):
        return f"<BacktestJob {self.id} - {self.symbol}>"
