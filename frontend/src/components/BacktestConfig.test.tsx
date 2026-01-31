import { describe, it, expect, vi } from 'vitest';
import { render, screen, fireEvent } from '@testing-library/react';
import BacktestConfig from './BacktestConfig';

describe('BacktestConfig Component', () => {
  it('renders backtest configuration form and inputs', () => {
    const mockStart = vi.fn();
    const mockEnd = vi.fn();
    const mockCapital = vi.fn();

    render(
      <BacktestConfig
        startDate=""
        endDate=""
        capital={50000}
        onStartDateChange={mockStart}
        onEndDateChange={mockEnd}
        onCapitalChange={mockCapital}
      />
    );

    expect(screen.getByText(/backtest configuration/i)).toBeTruthy();
    expect(screen.getByLabelText(/start date/i)).toBeTruthy();
    expect(screen.getByLabelText(/end date/i)).toBeTruthy();
    expect(screen.getByLabelText(/initial capital/i)).toBeTruthy();
  });

  it('calls change handlers when inputs change', () => {
    const mockStart = vi.fn();
    const mockEnd = vi.fn();
    const mockCapital = vi.fn();

    render(
      <BacktestConfig
        startDate=""
        endDate=""
        capital={50000}
        onStartDateChange={mockStart}
        onEndDateChange={mockEnd}
        onCapitalChange={mockCapital}
      />
    );

    const start = screen.getByLabelText(/start date/i) as HTMLInputElement;
    const end = screen.getByLabelText(/end date/i) as HTMLInputElement;
    const capital = screen.getByLabelText(/initial capital/i) as HTMLInputElement;

    fireEvent.change(start, { target: { value: '2024-01-01' } });
    fireEvent.change(end, { target: { value: '2024-01-10' } });
    fireEvent.change(capital, { target: { value: '60000' } });

    expect(mockStart).toHaveBeenCalledWith('2024-01-01');
    expect(mockEnd).toHaveBeenCalledWith('2024-01-10');
    expect(mockCapital).toHaveBeenCalledWith(60000);
  });
});
