from fastapi import APIRouter, HTTPException
from app.api.v1.schemas.backtest import BacktestRequest, BacktestResponse, BacktestResultSchema, ChartData
from app.core.data.fetcher import MockDataFetcher
from fastapi import APIRouter, HTTPException
from app.api.v1.schemas.backtest import BacktestRequest, BacktestResponse
from app.core.data.fetcher import MockDataFetcher
from app.core.backtest.executor import TradeExecutor
from app.core.backtest.engine import BacktestEngine
from app.db.models.backtest_job import BacktestJob
from app.db.models.backtest_result import BacktestResult
from app.db.models.trade import Trade
from app.db.session import SessionLocal
from datetime import datetime, time
import uuid
import logging

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/backtest", response_model=BacktestResponse, status_code=202)
def submit_backtest(req: BacktestRequest):
    job_id = str(uuid.uuid4())
    logger.info(f"New backtest request - Job ID: {job_id}, Symbol: {req.symbol}, Algorithm: {req.algorithm_id}")
    db = SessionLocal()
    try:
        job = BacktestJob(
            id=job_id,
            symbol=req.symbol,
            algorithm_id=req.algorithm_id,
            parameters=req.parameters.model_dump(),
            start_date=req.start_date,
            end_date=req.end_date,
            initial_capital=req.initial_capital,
            allow_short=req.allow_short,
            brokerage_fee=req.brokerage_fee,
            status="processing",
        )
        db.add(job)
        db.commit()
        logger.debug(f"Job {job_id} created in database")

        fetcher = MockDataFetcher()
        logger.debug(f"Fetching data for {req.symbol} from {req.start_date} to {req.end_date}")
        df = fetcher.fetch_historical_data(
            req.symbol,
            datetime.combine(req.start_date, time.min),
            datetime.combine(req.end_date, time.max),
        )
        logger.debug(f"Data fetched - {len(df)} candles received")

        executor = TradeExecutor(brokerage_fee=req.brokerage_fee)
        engine = BacktestEngine(executor)
        logger.debug(f"Running backtest engine for {req.symbol}")
        result = engine.run(
            req.symbol, req.algorithm_id, req.parameters.model_dump(), df, req.initial_capital, req.allow_short
        )

        chart = {
            "timestamps": [ts.isoformat() for ts in df["datetime"].tolist()],
            "prices": df["close"].tolist(),
            "sma": df["sma"].tolist() if "sma" in df.columns else [],
            "z_scores": df["z_score"].tolist() if "z_score" in df.columns else [],
            "signals": df["signal"].tolist() if "signal" in df.columns else [],
        }

        res = BacktestResult(
            job_id=job_id,
            final_capital=result["final_capital"],
            total_return=round(result["final_capital"] - req.initial_capital, 2),
            return_percentage=round((result["final_capital"] - req.initial_capital) / req.initial_capital * 100, 4),
            total_trades=sum(1 for t in result["trades"] if t["type"] == "EXIT"),
            winning_trades=sum(1 for t in result["trades"] if t.get("type") == "EXIT" and t.get("pnl", 0) and t.get("pnl") > 0),
            losing_trades=sum(1 for t in result["trades"] if t.get("type") == "EXIT" and t.get("pnl", 0) and t.get("pnl") <= 0),
            win_rate=0.0,
            chart_data=chart,
        )
        db.add(res)
        db.commit()
        logger.info(f"Backtest result saved - Job ID: {job_id}, Final Capital: {result['final_capital']}, Total Trades: {res.total_trades}")

        seq = 0
        for t in result["trades"]:
            seq += 1
            trade = Trade(
                id=str(uuid.uuid4()),
                job_id=job_id,
                trade_sequence=t.get("trade_sequence", seq),
                trade_type=t["type"],
                symbol=req.symbol,
                trade_time=t["time"],
                price=t["price"],
                quantity=t["qty"],
                brokerage_fee=req.brokerage_fee,
                capital_after=t["capital"],
                pnl=t.get("pnl"),
                pnl_percentage=None,
                z_score=t.get("z_score"),
                sma=t.get("sma"),
            )
            db.add(trade)
        db.commit()
        logger.debug(f"All trades saved to database - Total: {len(result['trades'])}")

        job.status = "completed"
        db.add(job)
        db.commit()
        logger.info(f"Job {job_id} completed successfully")

        return BacktestResponse(job_id=job_id, status="completed", message="Backtest completed")
    except Exception as e:
        logger.error(f"Backtest failed for job {job_id} - Error: {str(e)}", exc_info=True)
        db.rollback()
        if "job" in locals():
            job.status = "failed"
            job.error_message = str(e)
            db.add(job)
            db.commit()
            logger.error(f"Job {job_id} marked as failed")
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()
