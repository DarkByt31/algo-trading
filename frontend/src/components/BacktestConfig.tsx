import React from 'react';
import {
  Box,
  TextField,
  Grid,
  Card,
  CardContent,
  Typography,
  InputAdornment,
} from '@mui/material';

interface BacktestConfigProps {
  startDate: string;
  endDate: string;
  capital: number;
  onStartDateChange: (date: string) => void;
  onEndDateChange: (date: string) => void;
  onCapitalChange: (capital: number) => void;
}

export const BacktestConfig: React.FC<BacktestConfigProps> = ({
  startDate,
  endDate,
  capital,
  onStartDateChange,
  onEndDateChange,
  onCapitalChange,
}) => {
  return (
    <Card sx={{ width: '100%' }}>
      <CardContent>
        <Typography variant="h6" sx={{ mb: 2 }}>
          Backtest Configuration
        </Typography>
        <Grid container spacing={2}>
          <Grid item xs={12} sm={6}>
            <TextField
              fullWidth
              label="Start Date"
              type="date"
              value={startDate}
              onChange={(e) => onStartDateChange(e.target.value)}
              InputLabelProps={{ shrink: true }}
            />
          </Grid>
          <Grid item xs={12} sm={6}>
            <TextField
              fullWidth
              label="End Date"
              type="date"
              value={endDate}
              onChange={(e) => onEndDateChange(e.target.value)}
              InputLabelProps={{ shrink: true }}
            />
          </Grid>
          <Grid item xs={12} sm={6}>
            <TextField
              fullWidth
              label="Initial Capital"
              type="number"
              value={capital}
              onChange={(e) => onCapitalChange(parseFloat(e.target.value))}
              InputProps={{
                startAdornment: <InputAdornment position="start">₹</InputAdornment>,
              }}
              inputProps={{ min: 1000, step: 1000 }}
            />
          </Grid>
        </Grid>
      </CardContent>
    </Card>
  );
};

export default BacktestConfig;
