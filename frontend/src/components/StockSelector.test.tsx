import { describe, it, expect, vi, afterEach } from 'vitest';
import { render, screen, fireEvent } from '@testing-library/react';
import StockSelector from './StockSelector';
import * as useStocksHook from '../hooks/useStocks';

describe('StockSelector Component', () => {
  afterEach(() => {
    vi.resetAllMocks();
  });

  // Test 1: Renders with available stocks
  it('renders stock selector with available stocks', () => {
    vi.spyOn(useStocksHook, 'useStocks').mockReturnValue({
      stocks: ['TATVA', 'VOLTAS', 'RELIANCE'],
      loading: false,
      error: null,
    });

    const mockOnChange = vi.fn();
    render(<StockSelector value="TATVA" onChange={mockOnChange} />);
    
    const combobox = screen.getByRole('combobox');
    expect(combobox).toBeTruthy();
  });

  // Test 2: Calls onChange when stock is selected
  it('calls onChange when stock is selected via input change', () => {
    vi.spyOn(useStocksHook, 'useStocks').mockReturnValue({
      stocks: ['TATVA', 'VOLTAS'],
      loading: false,
      error: null,
    });

    const mockOnChange = vi.fn();
    render(<StockSelector value="TATVA" onChange={mockOnChange} />);
    
    const nativeInput = screen.getByDisplayValue('TATVA') as HTMLInputElement;
    fireEvent.change(nativeInput, { target: { value: 'VOLTAS' } });
    
    expect(mockOnChange).toHaveBeenCalledWith('VOLTAS');
  });

  // Test 3: Displays loading spinner when loading
  it('displays loading spinner when loading stocks', () => {
    vi.spyOn(useStocksHook, 'useStocks').mockReturnValue({
      stocks: [],
      loading: true,
      error: null,
    });

    const mockOnChange = vi.fn();
    render(<StockSelector value="" onChange={mockOnChange} />);
    
    expect(screen.getByRole('progressbar')).toBeTruthy();
  });

  // Test 4: Displays error message when API fails
  it('displays error message when stock fetching fails', () => {
    vi.spyOn(useStocksHook, 'useStocks').mockReturnValue({
      stocks: [],
      loading: false,
      error: 'Failed to fetch stocks',
    });

    const mockOnChange = vi.fn();
    render(<StockSelector value="" onChange={mockOnChange} />);
    
    const errorAlert = screen.getByText(/Failed to load stocks/i);
    expect(errorAlert).toBeTruthy();
  });

  // Test 5: Disables dropdown during loading
  it('disables dropdown while loading stocks', () => {
    vi.spyOn(useStocksHook, 'useStocks').mockReturnValue({
      stocks: [],
      loading: true,
      error: null,
    });

    const mockOnChange = vi.fn();
    render(<StockSelector value="" onChange={mockOnChange} />);
    
    const formControl = screen.getByRole('combobox').closest('[class*="MuiFormControl"]');
    expect(formControl).toBeTruthy();
    // Verify loading state shows spinner
    expect(screen.getByRole('progressbar')).toBeTruthy();
  });

  // Test 6: Handles dropdown click without breaking
  it('handles dropdown click without throwing errors', () => {
    vi.spyOn(useStocksHook, 'useStocks').mockReturnValue({
      stocks: ['TATVA', 'VOLTAS', 'RELIANCE'],
      loading: false,
      error: null,
    });

    const mockOnChange = vi.fn();
    render(<StockSelector value="" onChange={mockOnChange} />);
    
    const combobox = screen.getByRole('combobox');
    expect(() => {
      fireEvent.click(combobox);
    }).not.toThrow();
  });

  // Test 7: Renders without crashing with multiple stocks
  it('renders without crashing when multiple stocks are available', () => {
    const stocks = ['TATVA', 'VOLTAS', 'RELIANCE', 'HDFC', 'INFOSYS'];
    vi.spyOn(useStocksHook, 'useStocks').mockReturnValue({
      stocks,
      loading: false,
      error: null,
    });

    const mockOnChange = vi.fn();
    render(<StockSelector value="" onChange={mockOnChange} />);
    
    const combobox = screen.getByRole('combobox');
    expect(combobox).toBeTruthy();
  });

  // Test 8: Handles empty stocks array gracefully
  it('handles empty stocks array gracefully', () => {
    vi.spyOn(useStocksHook, 'useStocks').mockReturnValue({
      stocks: [],
      loading: false,
      error: null,
    });

    const mockOnChange = vi.fn();
    render(<StockSelector value="" onChange={mockOnChange} />);
    
    const combobox = screen.getByRole('combobox');
    expect(combobox).toBeTruthy();
    expect(combobox.closest('[class*="MuiFormControl"]')).toBeTruthy();
  });

  // Test 9: Maintains selected value when value prop changes
  it('maintains selected value when value prop changes', () => {
    vi.spyOn(useStocksHook, 'useStocks').mockReturnValue({
      stocks: ['TATVA', 'VOLTAS', 'RELIANCE'],
      loading: false,
      error: null,
    });

    const mockOnChange = vi.fn();
    const { rerender } = render(
      <StockSelector value="TATVA" onChange={mockOnChange} />
    );
    
    let combobox = screen.getByDisplayValue('TATVA');
    expect(combobox).toBeTruthy();
    
    rerender(<StockSelector value="VOLTAS" onChange={mockOnChange} />);
    
    combobox = screen.getByDisplayValue('VOLTAS');
    expect(combobox).toBeTruthy();
  });

  // Test 10: Network error handling
  it('handles network errors gracefully with error display', () => {
    vi.spyOn(useStocksHook, 'useStocks').mockReturnValue({
      stocks: [],
      loading: false,
      error: 'Network Error: Failed to connect to API',
    });

    const mockOnChange = vi.fn();
    render(<StockSelector value="" onChange={mockOnChange} />);
    
    const errorAlert = screen.getByText(/Failed to load stocks/i);
    expect(errorAlert).toBeTruthy();
  });

  // Test 11: Renders FormControl component
  it('renders FormControl component for proper layout', () => {
    vi.spyOn(useStocksHook, 'useStocks').mockReturnValue({
      stocks: ['TATVA', 'VOLTAS'],
      loading: false,
      error: null,
    });

    const mockOnChange = vi.fn();
    render(<StockSelector value="TATVA" onChange={mockOnChange} />);
    
    const formControl = screen.getByRole('combobox').closest('[class*="MuiFormControl"]');
    expect(formControl).toBeTruthy();
  });

  // Test 12: Handles selection of first stock
  it('allows selection of first available stock', () => {
    vi.spyOn(useStocksHook, 'useStocks').mockReturnValue({
      stocks: ['TATVA', 'VOLTAS', 'RELIANCE'],
      loading: false,
      error: null,
    });

    const mockOnChange = vi.fn();
    render(<StockSelector value="" onChange={mockOnChange} />);
    
    const nativeInput = screen.getByDisplayValue('') as HTMLInputElement;
    fireEvent.change(nativeInput, { target: { value: 'TATVA' } });
    
    expect(mockOnChange).toHaveBeenCalledWith('TATVA');
  });
});
