from fastapi import APIRouter, HTTPException
from app.db.session import SessionLocal
from app.db.models.trade import Trade

router = APIRouter()


@router.get("/trades/{job_id}")
def get_trades(job_id: str, limit: int = 50, offset: int = 0):
    db = SessionLocal()
    try:
        q = db.query(Trade).filter_by(job_id=job_id).order_by(Trade.trade_sequence.asc()).limit(limit).offset(offset)
        items = q.all()
        trades = []
        for t in items:
            trades.append({
                'id': t.id,
                'sequence': t.trade_sequence,
                'type': t.trade_type,
                'symbol': t.symbol,
                'time': t.trade_time.isoformat() if t.trade_time else None,
                'price': float(t.price),
                'quantity': int(t.quantity),
                'brokerage_fee': float(t.brokerage_fee),
                'capital_after': float(t.capital_after),
                'pnl': float(t.pnl) if t.pnl is not None else None,
                'z_score': float(t.z_score) if t.z_score is not None else None,
                'sma': float(t.sma) if t.sma is not None else None,
            })
        total = db.query(Trade).filter_by(job_id=job_id).count()
        return {'trades': trades, 'total_count': total, 'page': int(offset/limit)+1}
    finally:
        db.close()
