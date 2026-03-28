from fastapi import APIRouter, HTTPException
from app.db.session import SessionLocal
from app.db.models.backtest_result import BacktestResult
from app.db.models.backtest_job import BacktestJob

router = APIRouter()


@router.get("/results/{job_id}")
def get_results(job_id: str):
    db = SessionLocal()
    try:
        # Query both job and result to get all data
        job = db.query(BacktestJob).filter_by(id=job_id).first()
        res = db.query(BacktestResult).filter_by(job_id=job_id).first()
        
        if not res or not job:
            raise HTTPException(status_code=404, detail="Result not found")
        
        # Return flattened top-level fields for compatibility with existing clients,
        # while keeping a nested `backtest_result` object for richer data.
        payload = {
            'job_id': job_id,
            'status': 'completed',
            'symbol': job.symbol,
            'algorithm_id': job.algorithm_id,
            'start_date': job.start_date.isoformat() if job.start_date else None,
            'end_date': job.end_date.isoformat() if job.end_date else None,
            'initial_capital': float(job.initial_capital),
            'final_capital': float(res.final_capital),
            'total_return': float(res.total_return),
            'return_percentage': float(res.return_percentage),
            'total_trades': int(res.total_trades),
            'winning_trades': int(res.winning_trades),
            'losing_trades': int(res.losing_trades),
            'win_rate': float(res.win_rate) if res.win_rate else 0,
            'max_drawdown': float(res.max_drawdown) if res.max_drawdown else 0,
            'sharpe_ratio': float(res.sharpe_ratio) if res.sharpe_ratio else 0,
            'chart_data': res.chart_data,
        }

        # keep nested structure for clients that expect it
        payload['backtest_result'] = {
            'final_capital': payload['final_capital'],
            'total_return': payload['total_return'],
            'return_percentage': payload['return_percentage'],
            'total_trades': payload['total_trades'],
            'winning_trades': payload['winning_trades'],
            'losing_trades': payload['losing_trades'],
            'win_rate': payload['win_rate'],
            'max_drawdown': payload['max_drawdown'],
            'sharpe_ratio': payload['sharpe_ratio'],
            'chart_data': payload['chart_data'],
        }

        return payload
    finally:
        db.close()
