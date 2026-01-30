from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.utils import setup_logging
from app.db.base import Base
from app.db.session import engine
from app.api.v1.endpoints import stocks, algorithms, backtest, results, trades

# Setup logging
setup_logging()

# Initialize FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    description="Trading Backtesting Platform API",
    version=settings.API_VERSION,
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def startup_event():
    Base.metadata.create_all(bind=engine)


@app.get("/health")
def health_check():
    return {"status": "healthy", "version": settings.API_VERSION}


@app.get("/")
def root():
    return {"message": f"Welcome to {settings.APP_NAME}", "version": settings.API_VERSION}


# Include API routers
app.include_router(stocks.router, prefix="/api/v1")
app.include_router(algorithms.router, prefix="/api/v1")
app.include_router(backtest.router, prefix="/api/v1")
app.include_router(results.router, prefix="/api/v1")
app.include_router(trades.router, prefix="/api/v1")
