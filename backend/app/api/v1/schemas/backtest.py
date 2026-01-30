from pydantic import BaseModel, Field
from typing import Dict, Any, Optional
from datetime import date


class BacktestParameters(BaseModel):
    SMA_WINDOW: int = Field(20, ge=5, le=100)
    Z_ENTRY: float = Field(1.0, ge=0.5, le=3.0)
    Z_EXIT_THRESHOLD: float = Field(0.3, ge=0.1, le=1.0)


class BacktestRequest(BaseModel):
    symbol: str
    algorithm_id: str
    parameters: BacktestParameters
    start_date: date
    end_date: date
    initial_capital: float = Field(..., gt=0)
    allow_short: bool = True
    brokerage_fee: float = 20.0


class BacktestResponse(BaseModel):
    job_id: str
    status: str
    message: Optional[str] = None


class ChartData(BaseModel):
    timestamps: list
    prices: list
    sma: list
    z_scores: list
    signals: list


class BacktestResultSchema(BaseModel):
    job_id: str
    symbol: str
    algorithm_id: str
    initial_capital: float
    final_capital: float
    total_trades: int
    winning_trades: int
    losing_trades: int
    win_rate: float
    chart_data: ChartData

