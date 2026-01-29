import logging
from typing import Dict, Type
from app.core.algorithms.base import BaseAlgorithm
from app.core.algorithms.mean_reversion import MeanReversionAlgorithm

logger = logging.getLogger(__name__)


class AlgorithmRegistry:
    """Registry for all available algorithms"""
    
    _algorithms: Dict[str, Type[BaseAlgorithm]] = {
        'mean_reversion': MeanReversionAlgorithm,
    }
    
    @classmethod
    def get_algorithm(cls, algorithm_id: str, parameters: Dict) -> BaseAlgorithm:
        """
        Get algorithm instance by ID
        
        Args:
            algorithm_id: Algorithm identifier
            parameters: Algorithm parameters
        
        Returns:
            Algorithm instance
        
        Raises:
            ValueError: If algorithm not found
        """
        if algorithm_id not in cls._algorithms:
            available = list(cls._algorithms.keys())
            raise ValueError(f"Algorithm '{algorithm_id}' not found. Available: {available}")
        
        AlgorithmClass = cls._algorithms[algorithm_id]
        logger.info(f"Instantiating algorithm: {algorithm_id}")
        return AlgorithmClass(parameters)
    
    @classmethod
    def list_algorithms(cls) -> Dict[str, Type[BaseAlgorithm]]:
        """List all registered algorithms"""
        return cls._algorithms.copy()
    
    @classmethod
    def register(cls, algorithm_id: str, algorithm_class: Type[BaseAlgorithm]) -> None:
        """Register a new algorithm"""
        if algorithm_id in cls._algorithms:
            logger.warning(f"Overwriting existing algorithm: {algorithm_id}")
        cls._algorithms[algorithm_id] = algorithm_class
        logger.info(f"Registered algorithm: {algorithm_id}")
