import React from 'react';
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
  Card,
  CardContent,
} from 'recharts';
import { Box, Typography, Alert } from '@mui/material';
import { Trade } from '../types/results';

interface ChartDataPoint {
  date: string;
  capital: number;
}

interface ChartContainerProps {
  trades: Trade[];
  initialCapital: number;
}

export const ChartContainer: React.FC<ChartContainerProps> = ({ trades, initialCapital }) => {
  // Generate chart data from trades
  const generateChartData = (): ChartDataPoint[] => {
    if (trades.length === 0) {
      return [];
    }

    const data: ChartDataPoint[] = [];
    let runningCapital = initialCapital;

    // Sort trades by exit date
    const sortedTrades = [...trades].sort(
      (a, b) => new Date(a.exit_date).getTime() - new Date(b.exit_date).getTime()
    );

    sortedTrades.forEach((trade) => {
      runningCapital += trade.pnl;
      data.push({
        date: new Date(trade.exit_date).toLocaleDateString('en-IN'),
        capital: parseFloat(runningCapital.toFixed(2)),
      });
    });

    return data;
  };

  const chartData = generateChartData();

  if (chartData.length === 0) {
    return <Alert severity="info">No trades to display on chart.</Alert>;
  }

  return (
    <Box sx={{ width: '100%', height: 400 }}>
      <Typography variant="h6" sx={{ mb: 2 }}>
        Capital Growth
      </Typography>
      <ResponsiveContainer width="100%" height="100%">
        <LineChart data={chartData}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="date" angle={-45} textAnchor="end" height={80} />
          <YAxis />
          <Tooltip
            formatter={(value) =>
              `₹${Number(value).toLocaleString('en-IN', {
                minimumFractionDigits: 2,
                maximumFractionDigits: 2,
              })}`
            }
          />
          <Legend />
          <Line
            type="monotone"
            dataKey="capital"
            stroke="#8884d8"
            dot={{ fill: '#8884d8', r: 4 }}
            activeDot={{ r: 6 }}
            name="Capital"
          />
        </LineChart>
      </ResponsiveContainer>
    </Box>
  );
};

export default ChartContainer;
