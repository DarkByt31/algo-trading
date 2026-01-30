// Backtest-related types
export interface BacktestRequest {
  symbol: string;
  algorithm: string;
  start_date: string;
  end_date: string;
  capital: number;
  parameters: Record<string, string | number>;
}

export interface BacktestResponse {
  job_id: string;
  status: string;
  created_at: string;
}

export interface BacktestStatus {
  job_id: string;
  status: 'pending' | 'running' | 'completed' | 'failed';
  progress: number;
}
