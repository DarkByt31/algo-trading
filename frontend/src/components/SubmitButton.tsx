import React from 'react';
import { Box, Button, CircularProgress, Alert } from '@mui/material';

interface SubmitButtonProps {
  loading: boolean;
  error?: string;
  disabled?: boolean;
  onClick: () => void;
}

export const SubmitButton: React.FC<SubmitButtonProps> = ({
  loading,
  error,
  disabled = false,
  onClick,
}) => {
  return (
    <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2, width: '100%' }}>
      <Button
        variant="contained"
        color="primary"
        size="large"
        fullWidth
        onClick={onClick}
        disabled={loading || disabled}
        sx={{ py: 1.5, fontSize: '1.1rem' }}
      >
        {loading ? <CircularProgress size={24} sx={{ mr: 1 }} /> : null}
        {loading ? 'Running Backtest...' : 'Run Backtest'}
      </Button>
      {error && <Alert severity="error">{error}</Alert>}
    </Box>
  );
};

export default SubmitButton;
