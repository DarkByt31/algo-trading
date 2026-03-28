from fastapi import APIRouter
from typing import List
from app.api.v1.schemas.stock import StockInfo

router = APIRouter()

# Simple static list for MVP
_STOCKS = [
    {"symbol": "RELIANCE", "name": "Reliance Industries", "exchange": "NSE", "sector": "Energy"},
    {"symbol": "VOLTAS", "name": "Voltas Limited", "exchange": "NSE", "sector": "Electrical Equipment"},
    {"symbol": "TATVA", "name": "Tatva Chintan Pharma", "exchange": "NSE", "sector": "Chemicals"},
]


@router.get("/stocks", response_model=List[StockInfo])
def list_stocks():
    return _STOCKS
