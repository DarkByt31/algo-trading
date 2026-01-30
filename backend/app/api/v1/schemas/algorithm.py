from pydantic import BaseModel
from typing import List, Dict, Any


class AlgorithmParam(BaseModel):
    name: str
    type: str
    default: Any
    min: Any = None
    max: Any = None
    description: str = ""


class AlgorithmMetadata(BaseModel):
    id: str
    name: str
    description: str
    version: str
    is_active: bool
    parameters: List[AlgorithmParam]
