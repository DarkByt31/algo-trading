from fastapi import APIRouter, HTTPException
from app.db.session import SessionLocal
from app.db.models.backtest_result import BacktestResult

router = APIRouter()


@router.get("/results/{job_id}")
def get_results(job_id: str):
    db = SessionLocal()
    try:
        res = db.query(BacktestResult).filter_by(job_id=job_id).first()
        if not res:
            raise HTTPException(status_code=404, detail="Result not found")
        return {
            'job_id': job_id,
            'status': 'completed',
            'backtest_result': {
                'final_capital': float(res.final_capital),
                'total_return': float(res.total_return),
                'return_percentage': float(res.return_percentage),
                'total_trades': int(res.total_trades),
                'chart_data': res.chart_data
            }
        }
    finally:
        db.close()
