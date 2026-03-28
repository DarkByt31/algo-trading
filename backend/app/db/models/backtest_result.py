from sqlalchemy import Column, String, Numeric, Float, Integer, JSON, DateTime, ForeignKey, func
from datetime import datetime
import uuid
from app.db.base import Base


class BacktestResult(Base):
    """Backtest results and performance metrics"""
    __tablename__ = "backtest_results"
    
    id = Column(String(36), primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    job_id = Column(String(36), ForeignKey("backtest_jobs.id", ondelete="CASCADE"), nullable=False, unique=True, index=True)
    
    final_capital = Column(Numeric(12, 2), nullable=False)
    total_return = Column(Numeric(12, 2), nullable=False)
    return_percentage = Column(Numeric(8, 4), nullable=False)
    total_trades = Column(Integer, default=0)
    winning_trades = Column(Integer, default=0)
    losing_trades = Column(Integer, default=0)
    win_rate = Column(Numeric(5, 2), nullable=True)
    max_drawdown = Column(Numeric(8, 4), nullable=True)
    min_capital = Column(Numeric(12, 2), nullable=True)
    sharpe_ratio = Column(Numeric(8, 4), nullable=True)
    profit_factor = Column(Numeric(8, 4), nullable=True)
    avg_trade_duration_minutes = Column(Integer, nullable=True)
    best_trade_pnl = Column(Numeric(12, 2), nullable=True)
    worst_trade_pnl = Column(Numeric(12, 2), nullable=True)
    chart_data = Column(JSON, nullable=True)  # Time series data for charts
    
    created_at = Column(DateTime, default=func.now())
    
    def __repr__(self):
        return f"<BacktestResult {self.job_id}>"
