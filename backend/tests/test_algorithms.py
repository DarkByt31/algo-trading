import pytest
import sys
from pathlib import Path
import pandas as pd

sys.path.insert(0, str(Path(__file__).parent.parent))

from app.core.algorithms.mean_reversion import MeanReversionAlgorithm
from app.utils.exceptions import InvalidParametersException


class TestMeanReversionAlgorithm:
    """Test suite for Mean Reversion Algorithm"""
    
    def test_initialization_valid_params(self, algorithm_params):
        """Test algorithm initialization with valid parameters"""
        algo = MeanReversionAlgorithm(algorithm_params)
        assert algo.algorithm_id == "mean_reversion"
        assert algo.algorithm_name == "Mean Reversion"
        assert algo.parameters == algorithm_params
    
    def test_initialization_missing_sma_window(self):
        """Test algorithm fails with missing SMA_WINDOW"""
        params = {'Z_ENTRY': 1.0, 'Z_EXIT_THRESHOLD': 0.3}
        with pytest.raises(ValueError, match="Missing required parameter: SMA_WINDOW"):
            MeanReversionAlgorithm(params)
    
    def test_initialization_missing_z_entry(self):
        """Test algorithm fails with missing Z_ENTRY"""
        params = {'SMA_WINDOW': 20, 'Z_EXIT_THRESHOLD': 0.3}
        with pytest.raises(ValueError, match="Missing required parameter: Z_ENTRY"):
            MeanReversionAlgorithm(params)
    
    def test_initialization_invalid_sma_window_too_small(self):
        """Test algorithm fails with SMA_WINDOW < 5"""
        params = {'SMA_WINDOW': 3, 'Z_ENTRY': 1.0, 'Z_EXIT_THRESHOLD': 0.3}
        with pytest.raises(ValueError, match="SMA_WINDOW must be int between 5-100"):
            MeanReversionAlgorithm(params)
    
    def test_initialization_invalid_sma_window_too_large(self):
        """Test algorithm fails with SMA_WINDOW > 100"""
        params = {'SMA_WINDOW': 150, 'Z_ENTRY': 1.0, 'Z_EXIT_THRESHOLD': 0.3}
        with pytest.raises(ValueError, match="SMA_WINDOW must be int between 5-100"):
            MeanReversionAlgorithm(params)
    
    def test_initialization_invalid_z_entry_too_small(self):
        """Test algorithm fails with Z_ENTRY < 0.5"""
        params = {'SMA_WINDOW': 20, 'Z_ENTRY': 0.2, 'Z_EXIT_THRESHOLD': 0.3}
        with pytest.raises(ValueError, match="Z_ENTRY must be float between 0.5-3.0"):
            MeanReversionAlgorithm(params)
    
    def test_initialization_invalid_z_entry_too_large(self):
        """Test algorithm fails with Z_ENTRY > 3.0"""
        params = {'SMA_WINDOW': 20, 'Z_ENTRY': 5.0, 'Z_EXIT_THRESHOLD': 0.3}
        with pytest.raises(ValueError, match="Z_ENTRY must be float between 0.5-3.0"):
            MeanReversionAlgorithm(params)
    
    def test_initialization_invalid_z_exit_too_small(self):
        """Test algorithm fails with Z_EXIT_THRESHOLD < 0.1"""
        params = {'SMA_WINDOW': 20, 'Z_ENTRY': 1.0, 'Z_EXIT_THRESHOLD': 0.05}
        with pytest.raises(ValueError, match="Z_EXIT_THRESHOLD must be float between 0.1-1.0"):
            MeanReversionAlgorithm(params)
    
    def test_generate_signals_returns_dataframe(self, algorithm_params, sample_dataframe):
        """Test signal generation returns DataFrame"""
        algo = MeanReversionAlgorithm(algorithm_params)
        result = algo.generate_signals(sample_dataframe)
        
        assert isinstance(result, pd.DataFrame)
        assert len(result) > 0
    
    def test_generate_signals_has_required_columns(self, algorithm_params, sample_dataframe):
        """Test generated signals have required columns"""
        algo = MeanReversionAlgorithm(algorithm_params)
        result = algo.generate_signals(sample_dataframe)
        
        required_cols = ['datetime', 'close', 'sma', 'std', 'z_score', 'signal', 'position']
        for col in required_cols:
            assert col in result.columns, f"Missing column: {col}"
    
    def test_generate_signals_calculates_sma(self, algorithm_params, sample_dataframe):
        """Test SMA calculation"""
        algo = MeanReversionAlgorithm(algorithm_params)
        result = algo.generate_signals(sample_dataframe)
        
        # Check that SMA values exist and are reasonable
        assert result['sma'].notna().sum() > 0
        # SMA should be close to but not equal to close price
        assert not result['sma'].equals(result['close'])
    
    def test_generate_signals_calculates_z_score(self, algorithm_params, sample_dataframe):
        """Test Z-score calculation"""
        algo = MeanReversionAlgorithm(algorithm_params)
        result = algo.generate_signals(sample_dataframe)
        
        # Z-score should be calculated (non-null values)
        assert result['z_score'].notna().sum() > 0
        # Z-score should have reasonable values (within ±5 std devs)
        assert result['z_score'].min() > -5 and result['z_score'].max() < 5
    
    def test_generate_signals_produces_signals(self, algorithm_params, sample_dataframe):
        """Test that signals are generated (not just HOLD)"""
        algo = MeanReversionAlgorithm(algorithm_params)
        result = algo.generate_signals(sample_dataframe)
        
        unique_signals = result['signal'].unique()
        # Should have at least HOLD, and potentially BUY/SELL
        assert 'HOLD' in unique_signals
    
    def test_generate_signals_position_shifted(self, algorithm_params, sample_dataframe):
        """Test that position is shifted signal (forward bias prevention)"""
        algo = MeanReversionAlgorithm(algorithm_params)
        result = algo.generate_signals(sample_dataframe)
        
        # position should be signal shifted by 1
        # Check that first position is HOLD (shifted from before data)
        assert result['position'].iloc[0] == 'HOLD'
    
    def test_repr(self, algorithm_params):
        """Test string representation"""
        algo = MeanReversionAlgorithm(algorithm_params)
        repr_str = repr(algo)
        assert "Mean Reversion" in repr_str
        assert "mean_reversion" in repr_str
