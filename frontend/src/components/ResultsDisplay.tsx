import React from 'react';
import {
  Box,
  Card,
  CardContent,
  Grid,
  Typography,
  CircularProgress,
  Alert,
  Chip,
} from '@mui/material';
import { BacktestResults } from '../types/results';

interface ResultsDisplayProps {
  results: BacktestResults | null;
  loading: boolean;
  error?: string;
}

const formatCurrency = (value: number): string => {
  return new Intl.NumberFormat('en-IN', {
    style: 'currency',
    currency: 'INR',
    minimumFractionDigits: 2,
    maximumFractionDigits: 2,
  }).format(value);
};

const formatPercentage = (value: number): string => {
  return `${(value * 100).toFixed(2)}%`;
};

const MetricCard: React.FC<{ label: string; value: string | number; color?: 'success' | 'error' | 'warning' }> = ({
  label,
  value,
  color,
}) => (
  <Card sx={{ height: '100%' }}>
    <CardContent>
      <Typography color="textSecondary" gutterBottom>
        {label}
      </Typography>
      <Typography
        variant="h6"
        sx={{
          color: color === 'success' ? 'green' : color === 'error' ? 'red' : 'inherit',
        }}
      >
        {value}
      </Typography>
    </CardContent>
  </Card>
);

export const ResultsDisplay: React.FC<ResultsDisplayProps> = ({ results, loading, error }) => {
  if (loading) {
    return (
      <Box sx={{ display: 'flex', justifyContent: 'center', py: 4 }}>
        <CircularProgress />
      </Box>
    );
  }

  if (error) {
    return <Alert severity="error">Error loading results: {error}</Alert>;
  }

  if (!results) {
    return (
      <Alert severity="info">No results available. Run a backtest to see results.</Alert>
    );
  }

  return (
    <Box sx={{ width: '100%' }}>
      <Card sx={{ mb: 3 }}>
        <CardContent>
          <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
            <Typography variant="h5">{results.symbol}</Typography>
            <Chip
              label={results.status.toUpperCase()}
              color={results.status === 'completed' ? 'success' : 'warning'}
              variant="outlined"
            />
          </Box>
          <Grid container spacing={2} sx={{ mb: 2 }}>
            <Grid item xs={12} sm={6}>
              <Typography color="textSecondary">Algorithm</Typography>
              <Typography variant="body1">{results.algorithm}</Typography>
            </Grid>
            <Grid item xs={12} sm={6}>
              <Typography color="textSecondary">Period</Typography>
              <Typography variant="body1">
                {results.start_date} to {results.end_date}
              </Typography>
            </Grid>
          </Grid>
        </CardContent>
      </Card>

      <Grid container spacing={2} sx={{ mb: 3 }}>
        <Grid item xs={12} sm={6} md={3}>
          <MetricCard
            label="Initial Capital"
            value={formatCurrency(results.initial_capital)}
          />
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <MetricCard
            label="Final Capital"
            value={formatCurrency(results.final_capital)}
            color={results.final_capital >= results.initial_capital ? 'success' : 'error'}
          />
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <MetricCard
            label="Total Return"
            value={formatCurrency(results.total_return)}
            color={results.total_return >= 0 ? 'success' : 'error'}
          />
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <MetricCard
            label="Return %"
            value={formatPercentage(results.return_percentage / 100)}
            color={results.return_percentage >= 0 ? 'success' : 'error'}
          />
        </Grid>
      </Grid>

      <Grid container spacing={2}>
        <Grid item xs={12} sm={6} md={2.4}>
          <MetricCard label="Total Trades" value={results.total_trades} />
        </Grid>
        <Grid item xs={12} sm={6} md={2.4}>
          <MetricCard label="Winning Trades" value={results.winning_trades} color="success" />
        </Grid>
        <Grid item xs={12} sm={6} md={2.4}>
          <MetricCard label="Losing Trades" value={results.losing_trades} color="error" />
        </Grid>
        <Grid item xs={12} sm={6} md={2.4}>
          <MetricCard label="Win Rate" value={formatPercentage(results.win_rate)} />
        </Grid>
      </Grid>
    </Box>
  );
};

export default ResultsDisplay;
