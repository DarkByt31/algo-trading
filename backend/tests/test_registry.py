import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from app.core.algorithms.registry import AlgorithmRegistry
from app.core.algorithms.mean_reversion import MeanReversionAlgorithm
from app.core.algorithms.base import BaseAlgorithm


class TestAlgorithmRegistry:
    """Test suite for Algorithm Registry"""
    
    def test_registry_get_mean_reversion(self, algorithm_params):
        """Test getting mean reversion algorithm from registry"""
        algo = AlgorithmRegistry.get_algorithm("mean_reversion", algorithm_params)
        
        assert isinstance(algo, MeanReversionAlgorithm)
        assert algo.algorithm_id == "mean_reversion"
    
    def test_registry_get_nonexistent_algorithm(self, algorithm_params):
        """Test getting non-existent algorithm raises error"""
        with pytest.raises(ValueError, match="Algorithm 'nonexistent' not found"):
            AlgorithmRegistry.get_algorithm("nonexistent", algorithm_params)
    
    def test_registry_list_algorithms(self):
        """Test listing all available algorithms"""
        algorithms = AlgorithmRegistry.list_algorithms()
        
        assert isinstance(algorithms, dict)
        assert "mean_reversion" in algorithms
        assert len(algorithms) >= 1
    
    def test_registry_mean_reversion_is_base_algorithm(self, algorithm_params):
        """Test mean reversion is instance of BaseAlgorithm"""
        algo = AlgorithmRegistry.get_algorithm("mean_reversion", algorithm_params)
        assert isinstance(algo, BaseAlgorithm)
    
    def test_registry_register_new_algorithm(self, algorithm_params):
        """Test registering new algorithm"""
        # Create a mock algorithm class
        class DummyAlgorithm(BaseAlgorithm):
            @property
            def algorithm_id(self):
                return "dummy"
            
            @property
            def algorithm_name(self):
                return "Dummy"
            
            def validate_parameters(self):
                pass
            
            def generate_signals(self, df):
                return df
        
        AlgorithmRegistry.register("dummy", DummyAlgorithm)
        
        # Verify it can be retrieved
        algo = AlgorithmRegistry.get_algorithm("dummy", algorithm_params)
        assert algo.algorithm_id == "dummy"
    
    def test_registry_algorithm_parameter_validation(self):
        """Test that invalid parameters raise error on instantiation"""
        invalid_params = {'INVALID': 1}
        
        with pytest.raises(ValueError):
            AlgorithmRegistry.get_algorithm("mean_reversion", invalid_params)
    
    def test_registry_error_message_shows_available(self):
        """Test error message shows available algorithms"""
        try:
            AlgorithmRegistry.get_algorithm("invalid", {})
        except ValueError as e:
            assert "Available:" in str(e) or "not found" in str(e)
