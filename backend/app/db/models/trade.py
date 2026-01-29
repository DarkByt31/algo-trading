from sqlalchemy import Column, String, Numeric, Float, Integer, Enum, DateTime, ForeignKey, func
from datetime import datetime
import uuid
from app.db.base import Base


class Trade(Base):
    """Individual trade records"""
    __tablename__ = "trades"
    
    id = Column(String(36), primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    job_id = Column(String(36), ForeignKey("backtest_jobs.id", ondelete="CASCADE"), nullable=False, index=True)
    
    trade_sequence = Column(Integer, nullable=False)  # Order of trade
    trade_type = Column(Enum('BUY', 'SELL', 'EXIT'), nullable=False)
    symbol = Column(String(20), nullable=False)
    trade_time = Column(DateTime, nullable=False, index=True)
    price = Column(Numeric(10, 2), nullable=False)
    quantity = Column(Integer, nullable=False)
    brokerage_fee = Column(Numeric(8, 2), default=0)
    capital_after = Column(Numeric(12, 2), nullable=False)
    
    # Exit trade specific
    pnl = Column(Numeric(12, 2), nullable=True)  # Profit/Loss for exit trades
    pnl_percentage = Column(Numeric(8, 4), nullable=True)
    
    # Context data
    z_score = Column(Numeric(8, 4), nullable=True)
    sma = Column(Numeric(10, 2), nullable=True)
    
    created_at = Column(DateTime, default=func.now())
    
    def __repr__(self):
        return f"<Trade {self.id} - {self.trade_type}>"
