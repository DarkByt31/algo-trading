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
import { useAlgorithms } from '../hooks/useAlgorithms';

interface AlgorithmSelectorProps {
  value: string;
  onChange: (algoId: string) => void;
}

export const AlgorithmSelector: React.FC<AlgorithmSelectorProps> = ({ value, onChange }) => {
  const { algorithms, loading, error } = useAlgorithms();

  if (error) {
    return <Alert severity="error">Failed to load algorithms: {error}</Alert>;
  }

  return (
    <Box sx={{ minWidth: '100%' }}>
      <FormControl fullWidth disabled={loading}>
        <InputLabel>Select Algorithm</InputLabel>
        <Select
          value={value}
          label="Select Algorithm"
          onChange={(e) => onChange(e.target.value)}
        >
          <MenuItem value="">
            <em>Choose an algorithm...</em>
          </MenuItem>
          {algorithms.map((algo) => (
            <MenuItem key={algo.id} value={algo.id}>
              {algo.name} (v{algo.version})
            </MenuItem>
          ))}
        </Select>
      </FormControl>
      {loading && <CircularProgress size={24} sx={{ mt: 2 }} />}
    </Box>
  );
};

export default AlgorithmSelector;
