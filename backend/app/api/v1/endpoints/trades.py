from fastapi import APIRouter, HTTPException
from app.db.session import SessionLocal
from app.db.models.trade import Trade

router = APIRouter()


@router.get("/trades/{job_id}")
def get_trades(job_id: str):
    db = SessionLocal()
    try:
        q = db.query(Trade).filter_by(job_id=job_id).order_by(Trade.trade_sequence.asc())
        items = q.all()
        # Build raw trade records list
        raw = []
        for t in items:
            raw.append({
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

        # Pair entry (BUY/SELL) with subsequent EXIT records to produce complete trades
        paired = []
        open_entry = None
        for r in raw:
            if r['type'] in ('BUY', 'SELL'):
                open_entry = {
                    'entry_date': r['time'],
                    'entry_price': r['price'],
                    'quantity': r['quantity'],
                    'type': 'LONG' if r['type'] == 'BUY' else 'SHORT',
                }
            elif r['type'] == 'EXIT' and open_entry:
                trade = {
                    'entry_date': open_entry['entry_date'],
                    'entry_price': open_entry['entry_price'],
                    'exit_date': r['time'],
                    'exit_price': r['price'],
                    'quantity': open_entry['quantity'],
                    'pnl': r['pnl'],
                    'type': open_entry['type'],
                }
                paired.append(trade)
                open_entry = None

        return paired
    finally:
        db.close()
