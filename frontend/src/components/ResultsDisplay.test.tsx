import { describe, it, expect } from 'vitest';
import { render, screen } from '@testing-library/react';
import ResultsDisplay from './ResultsDisplay';

describe('ResultsDisplay Component', () => {
  const mockResults = {
    job_id: 'test-123',
    symbol: 'TATVA',
    status: 'completed',
    algorithm: 'mean_reversion',
    start_date: '2024-01-01',
    end_date: '2024-01-10',
    initial_capital: 50000,
    final_capital: 55000,
    total_pnl: 5000,
    total_trades: 10,
    winning_trades: 6,
    losing_trades: 4,
    win_rate: 0.6,
    return_percentage: 10.0,
    max_drawdown: 0.05,
    total_return: 10.0,
    chart_data: {
      timestamps: ['2024-01-01', '2024-01-10'],
      prices: [50000, 55000]
    }
  };

  it('renders results display with symbol and metrics', () => {
    render(<ResultsDisplay results={mockResults} loading={false} />);
    expect(screen.getByText('TATVA')).toBeTruthy();
    expect(screen.getByText(/₹55,000.00/)).toBeTruthy();
    expect(screen.getByText(/10.00%/)).toBeTruthy();
  });

  it('shows winning and losing trades', () => {
    render(<ResultsDisplay results={mockResults} loading={false} />);
    const six = screen.getAllByText((content) => content.trim() === '6');
    const four = screen.getAllByText((content) => content.trim() === '4');
    expect(six.length).toBeGreaterThan(0);
    expect(four.length).toBeGreaterThan(0);
  });

  it('displays loading indicator when loading', () => {
    render(<ResultsDisplay results={null} loading={true} />);
    expect(screen.getByRole('progressbar')).toBeTruthy();
  });

  it('displays empty state when no results', () => {
    render(<ResultsDisplay results={null} loading={false} />);
    expect(screen.getByText(/no results available/i)).toBeTruthy();
  });

  it('displays negative returns correctly', () => {
    const negativeResults = { ...mockResults, final_capital: 45000, return_percentage: -10.0, total_return: -10.0, chart_data: { timestamps: ['2024-01-01', '2024-01-10'], prices: [50000, 45000] } };
    render(<ResultsDisplay results={negativeResults} loading={false} />);
    expect(screen.getByText(/-10.00%/)).toBeTruthy();
  });
});
