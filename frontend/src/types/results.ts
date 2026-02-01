// Trade-related types
export interface Trade {
  id: string;
  job_id: string;
  symbol: string;
  entry_date: string;
  entry_price: number;
  exit_date: string;
  exit_price: number;
  quantity: number;
  pnl: number;
  type: 'LONG' | 'SHORT';
}

// Chart data structure
export interface ChartData {
  timestamps: string[];
  prices: number[];
  sma?: number[];
  z_scores?: number[];
  signals?: number[];
}

// Results-related types
export interface BacktestResults {
  job_id: string;
  status: string;
  symbol: string;
  algorithm: string;
  start_date: string;
  end_date: string;
  initial_capital: number;
  final_capital: number;
  total_return: number;
  total_trades: number;
  winning_trades: number;
  losing_trades: number;
  win_rate: number;
  return_percentage: number;
  chart_data: ChartData;
}

export interface ResultsWithTrades {
  results: BacktestResults;
  trades: Trade[];
}
