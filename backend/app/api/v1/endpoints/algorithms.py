from fastapi import APIRouter
from typing import List
from app.api.v1.schemas.algorithm import AlgorithmMetadata, AlgorithmParam

router = APIRouter()

# For MVP provide registry-driven metadata
_ALGORITHMS = [
    {
        "id": "mean_reversion",
        "name": "Mean Reversion",
        "description": "Detects price deviations and trades reversal",
        "version": "1.0",
        "is_active": True,
        "parameters": [
            {"name": "SMA_WINDOW", "type": "integer", "default": 20, "min": 5, "max": 100, "description": "Simple Moving Average window"},
            {"name": "Z_ENTRY", "type": "float", "default": 1.0, "min": 0.5, "max": 3.0, "description": "Z-score entry threshold"},
            {"name": "Z_EXIT_THRESHOLD", "type": "float", "default": 0.3, "min": 0.1, "max": 1.0, "description": "Z-score exit threshold"}
        ]
    }
]


@router.get("/algorithms", response_model=List[AlgorithmMetadata])
def list_algorithms():
    return _ALGORITHMS
