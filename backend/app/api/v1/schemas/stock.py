from typing import Optional
from pydantic import BaseModel


class StockInfo(BaseModel):
    symbol: str
    name: Optional[str] = None
    exchange: str
    sector: Optional[str] = None

