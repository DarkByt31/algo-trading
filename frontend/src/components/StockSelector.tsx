import React from 'react';
import {
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  CircularProgress,
  Alert,
  Box,
} from '@mui/material';
import { useStocks } from '../hooks/useStocks';

interface StockSelectorProps {
  value: string;
  onChange: (symbol: string) => void;
}

export const StockSelector: React.FC<StockSelectorProps> = ({ value, onChange }) => {
  const { stocks, loading, error } = useStocks();

  if (error) {
    return <Alert severity="error">Failed to load stocks: {error}</Alert>;
  }

  return (
    <Box sx={{ minWidth: '100%' }}>
      <FormControl fullWidth disabled={loading}>
        <InputLabel>Select Stock</InputLabel>
        <Select value={value} label="Select Stock" onChange={(e) => onChange(e.target.value)}>
          <MenuItem value="">
            <em>Choose a stock...</em>
          </MenuItem>
          {stocks.map((stock) => (
            <MenuItem key={stock} value={stock}>
              {stock}
            </MenuItem>
          ))}
        </Select>
      </FormControl>
      {loading && <CircularProgress size={24} sx={{ mt: 2 }} />}
    </Box>
  );
};

export default StockSelector;
