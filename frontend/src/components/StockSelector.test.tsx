import { describe, it, expect, vi } from 'vitest';
import { render, screen, fireEvent } from '@testing-library/react';
import StockSelector from './StockSelector';
import * as useStocksHook from '../hooks/useStocks';

describe('StockSelector Component', () => {
  afterEach(() => {
    vi.resetAllMocks();
  });

  it('renders stock selector with available stocks', () => {
    vi.spyOn(useStocksHook, 'useStocks').mockReturnValue({ stocks: ['TATVA', 'VOLTAS', 'RELIANCE'], loading: false, error: null });
    const mockOnChange = vi.fn();
    render(<StockSelector value="TATVA" onChange={mockOnChange} />);
    const combobox = screen.getByRole('combobox');
    expect(combobox).toBeTruthy();
    expect(combobox.textContent).toContain('TATVA');
  });

  it('calls onChange when stock is selected', () => {
    vi.spyOn(useStocksHook, 'useStocks').mockReturnValue({ stocks: ['TATVA', 'VOLTAS'], loading: false, error: null });
    const mockOnChange = vi.fn();
    render(<StockSelector value="TATVA" onChange={mockOnChange} />);
    const nativeInput = screen.getByDisplayValue('TATVA') as HTMLInputElement;
    fireEvent.change(nativeInput, { target: { value: 'VOLTAS' } });
    expect(mockOnChange).toHaveBeenCalledWith('VOLTAS');
  });

  it('displays loading spinner when loading', () => {
    vi.spyOn(useStocksHook, 'useStocks').mockReturnValue({ stocks: [], loading: true, error: null });
    const mockOnChange = vi.fn();
    render(<StockSelector value="" onChange={mockOnChange} />);
    expect(screen.getByRole('progressbar')).toBeTruthy();
  });
});
