import { describe, it, expect, vi, afterEach } from 'vitest';
import { render, screen } from '@testing-library/react';
import TradeLog from './TradeLog';
import * as useTradesHook from '../hooks/useTrades';

describe('TradeLog Component', () => {
  afterEach(() => {
    vi.resetAllMocks();
  });

  const mockTrades = [
    {
      id: '1',
      trade_sequence: 1,
      type: 'LONG' as const,
      symbol: 'TATVA',
      entry_date: '2024-01-02',
      entry_price: 100,
      exit_date: '2024-01-03',
      exit_price: 105,
      quantity: 100,
      pnl: 500,
      job_id: 'job-1',
    },
    {
      id: '2',
      trade_sequence: 2,
      type: 'SHORT' as const,
      symbol: 'TATVA',
      entry_date: '2024-01-04',
      entry_price: 105,
      exit_date: '2024-01-05',
      exit_price: 103,
      quantity: 100,
      pnl: -200,
      job_id: 'job-1',
    }
  ];

  it('renders trade log header when jobId provided', () => {
    vi.spyOn(useTradesHook, 'useTrades').mockReturnValue({ trades: mockTrades, loading: false, error: null });
    render(<TradeLog jobId="job-1" />);
    expect(screen.getByText(/trade log/i)).toBeTruthy();
  });

  it('displays all trades and types', () => {
    vi.spyOn(useTradesHook, 'useTrades').mockReturnValue({ trades: mockTrades, loading: false, error: null });
    render(<TradeLog jobId="job-1" />);
    expect(screen.getByText(/BUY/)).toBeTruthy();
    expect(screen.getByText(/SELL/)).toBeTruthy();
  });

  it('shows trade details formatted', () => {
    vi.spyOn(useTradesHook, 'useTrades').mockReturnValue({ trades: mockTrades, loading: false, error: null });
    render(<TradeLog jobId="job-1" />);
    // prices are formatted as currency
    expect(screen.getByText(/₹100.00/)).toBeTruthy();
    expect(screen.getByText(/₹500.00/)).toBeTruthy();
  });

  it('handles empty trades list', () => {
    vi.spyOn(useTradesHook, 'useTrades').mockReturnValue({ trades: [], loading: false, error: null });
    render(<TradeLog jobId="job-1" />);
    expect(screen.getByText(/no trades executed/i)).toBeTruthy();
  });

  it('displays loading state', () => {
    vi.spyOn(useTradesHook, 'useTrades').mockReturnValue({ trades: [], loading: true, error: null });
    render(<TradeLog jobId="job-1" />);
    expect(screen.getByRole('progressbar')).toBeTruthy();
  });
});
