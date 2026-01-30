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

// Results-related types
export interface BacktestResults {
  job_id: string;
  symbol: string;
  algorithm: string;
  start_date: string;
  end_date: string;
  initial_capital: number;
  final_capital: number;
  total_trades: number;
  winning_trades: number;
  losing_trades: number;
  win_rate: number;
  total_pnl: number;
  return_percentage: number;
  max_drawdown: number;
  sharpe_ratio: number;
  created_at: string;
  status: string;
}

export interface ResultsWithTrades {
  results: BacktestResults;
  trades: Trade[];
}
