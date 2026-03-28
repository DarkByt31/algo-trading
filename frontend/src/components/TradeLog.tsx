import React from 'react';
import {
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
  Typography,
  Box,
  CircularProgress,
  Alert,
} from '@mui/material';
import { useTrades } from '../hooks/useTrades';

interface TradeLogProps {
  jobId?: string;
}

const formatCurrency = (value: number): string => {
  return new Intl.NumberFormat('en-IN', {
    style: 'currency',
    currency: 'INR',
    minimumFractionDigits: 2,
  }).format(value);
};

const formatDate = (date: string): string => {
  return new Date(date).toLocaleString('en-IN');
};

export const TradeLog: React.FC<TradeLogProps> = ({ jobId }) => {
  const { trades, loading, error } = useTrades(jobId);

  if (!jobId) {
    return <Alert severity="info">No job selected. Submit a backtest first.</Alert>;
  }

  if (loading) {
    return (
      <Box sx={{ display: 'flex', justifyContent: 'center', py: 4 }}>
        <CircularProgress />
      </Box>
    );
  }

  if (error) {
    return <Alert severity="error">Error loading trades: {error}</Alert>;
  }

  if (trades.length === 0) {
    return <Alert severity="info">No trades executed in this backtest.</Alert>;
  }

  return (
    <Box sx={{ width: '100%' }}>
      <Typography variant="h6" sx={{ mb: 2 }}>
        Trade Log ({trades.length} trades)
      </Typography>
      <TableContainer component={Paper}>
        <Table size="small">
          <TableHead sx={{ backgroundColor: '#f5f5f5' }}>
            <TableRow>
              <TableCell>Entry Date</TableCell>
              <TableCell align="right">Entry Price</TableCell>
              <TableCell>Exit Date</TableCell>
              <TableCell align="right">Exit Price</TableCell>
              <TableCell align="right">Qty</TableCell>
              <TableCell align="right">PnL</TableCell>
              <TableCell>Type</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {trades.map((trade) => (
              <TableRow key={trade.id}>
                <TableCell>{formatDate(trade.entry_date)}</TableCell>
                <TableCell align="right">{formatCurrency(trade.entry_price)}</TableCell>
                <TableCell>{formatDate(trade.exit_date)}</TableCell>
                <TableCell align="right">{formatCurrency(trade.exit_price)}</TableCell>
                <TableCell align="right">{trade.quantity}</TableCell>
                <TableCell
                  align="right"
                  sx={{
                    color: trade.pnl >= 0 ? 'green' : 'red',
                    fontWeight: 'bold',
                  }}
                >
                  {formatCurrency(trade.pnl)}
                </TableCell>
                <TableCell>{trade.type}</TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>
    </Box>
  );
};

export default TradeLog;
