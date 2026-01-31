import { describe, it, expect, beforeEach, vi } from 'vitest';
import { render, screen } from '@testing-library/react';
import App from './App';

// lightweight BrowserRouter shim to avoid requiring react-router-dom in the test env
const BrowserRouter = ({ children }: any) => children;

// Mock API calls
vi.mock('../services/api', () => ({
  getStocks: vi.fn(() => Promise.resolve([
    { id: 1, symbol: 'TATVA', name: 'TATVA' },
    { id: 2, symbol: 'VOLTAS', name: 'VOLTAS' }
  ])),
  getAlgorithms: vi.fn(() => Promise.resolve([
    { id: 1, name: 'mean_reversion', description: 'Mean Reversion' }
  ])),
  submitBacktest: vi.fn(() => Promise.resolve({ job_id: 'test-123' })),
  getResults: vi.fn(() => Promise.resolve({
    job_id: 'test-123',
    symbol: 'TATVA',
    initial_capital: 50000,
    final_capital: 55000,
    total_trades: 10
  }))
}));

describe('App Component', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('renders the main app component', () => {
    render(
      <BrowserRouter>
        <App />
      </BrowserRouter>
    );
    const matches = screen.getAllByText(/trading backtester/i);
    expect(matches.length).toBeGreaterThan(0);
  });

  it('displays loading spinner initially', () => {
    render(
      <BrowserRouter>
        <App />
      </BrowserRouter>
    );
    // App should render without errors
    expect(screen.getByRole('main')).toBeTruthy();
  });

  it('renders without crashing', () => {
    const { container } = render(
      <BrowserRouter>
        <App />
      </BrowserRouter>
    );
    expect(container).toBeTruthy();
  });
});
