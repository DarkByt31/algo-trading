// Backtest-related types
export interface BacktestParameters {
  SMA_WINDOW: number;
  Z_ENTRY: number;
  Z_EXIT_THRESHOLD: number;
}

export interface BacktestRequest {
  symbol: string;
  algorithm_id: string;
  start_date: string;
  end_date: string;
  initial_capital: number;
  parameters: BacktestParameters;
  allow_short?: boolean;
  brokerage_fee?: number;
}

export interface BacktestResponse {
  job_id: string;
  status: string;
  message?: string;
}

export interface BacktestStatus {
  job_id: string;
  status: 'pending' | 'running' | 'completed' | 'failed';
  progress: number;
}

export interface BacktestResults {
  job_id: string;
  final_capital: number;
  total_return: number;
  return_percentage: number;
  total_trades: number;
  winning_trades: number;
  losing_trades: number;
  win_rate: number;
  chart_data: {
    timestamps: string[];
    prices: number[];
    sma: number[];
    z_scores: number[];
    signals: number[];
  };
}
