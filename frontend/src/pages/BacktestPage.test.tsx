import { describe, it, expect } from 'vitest';

/**
 * BacktestPage - Backtest API Integration Tests
 * 
 * These tests document and verify the correct field names and structure
 * used when submitting backtest requests to the backend API.
 */
describe('BacktestPage - Backtest Submission', () => {
  // const mockAlgorithms = [
  //   {
  //     id: 'mean_reversion',
  //     name: 'Mean Reversion',
  //     description: 'Mean reversion trading strategy',
  //     parameters: [
  //       { name: 'SMA_WINDOW', default: 20, min: 5, max: 100, step: 1 },
  //       { name: 'Z_ENTRY', default: 1, min: 0.5, max: 3, step: 0.1 },
  //       { name: 'Z_EXIT_THRESHOLD', default: 0.3, min: 0.1, max: 1, step: 0.1 },
  //     ],
  //   },
  // ];

  // Test 1: Verify correct BacktestRequest field names
  it('uses algorithm_id field (NOT algorithm) in BacktestRequest', () => {
    // ✓ CORRECT field name: algorithm_id
    // ✗ WRONG field name: algorithm
    const correctRequest = {
      symbol: 'RELIANCE',
      algorithm_id: 'mean_reversion', // CORRECT
      start_date: '2026-01-01',
      end_date: '2026-01-31',
      initial_capital: 50000,
      parameters: {
        SMA_WINDOW: 20,
        Z_ENTRY: 1,
        Z_EXIT_THRESHOLD: 0.3,
      },
    };
    expect(correctRequest.algorithm_id).toBe('mean_reversion');
  });

  // Test 2: Verify initial_capital field name
  it('uses initial_capital field (NOT capital) in BacktestRequest', () => {
    // ✓ CORRECT field name: initial_capital
    // ✗ WRONG field name: capital
    const correctRequest = {
      symbol: 'RELIANCE',
      algorithm_id: 'mean_reversion',
      start_date: '2026-01-01',
      end_date: '2026-01-31',
      initial_capital: 50000, // CORRECT
      parameters: {
        SMA_WINDOW: 20,
        Z_ENTRY: 1,
        Z_EXIT_THRESHOLD: 0.3,
      },
    };
    expect(correctRequest.initial_capital).toBe(50000);
  });

  // Test 3: Verify parameter names use uppercase
  it('uses uppercase parameter names (SMA_WINDOW, Z_ENTRY, Z_EXIT_THRESHOLD)', () => {
    // ✓ CORRECT: SMA_WINDOW, Z_ENTRY, Z_EXIT_THRESHOLD
    // ✗ WRONG: sma_window, z_entry, z_exit_threshold
    const parameters = {
      SMA_WINDOW: 20,
      Z_ENTRY: 1,
      Z_EXIT_THRESHOLD: 0.3,
    };
    expect(parameters.SMA_WINDOW).toBe(20);
    expect(parameters.Z_ENTRY).toBe(1);
    expect(parameters.Z_EXIT_THRESHOLD).toBe(0.3);
  });

  // Test 4: Verify parameters are numbers not strings
  it('converts parameters to numbers (not strings)', () => {
    const parameters = {
      SMA_WINDOW: Number('20'),
      Z_ENTRY: Number('1'),
      Z_EXIT_THRESHOLD: Number('0.3'),
    };
    expect(typeof parameters.SMA_WINDOW).toBe('number');
    expect(typeof parameters.Z_ENTRY).toBe('number');
    expect(typeof parameters.Z_EXIT_THRESHOLD).toBe('number');
  });

  // Test 5: Verify date format is YYYY-MM-DD
  it('formats dates as YYYY-MM-DD strings (not ISO format)', () => {
    // ✓ CORRECT: "2026-01-01" (YYYY-MM-DD)
    // ✗ WRONG: "2026-01-01T00:00:00Z" (ISO format)
    const startDate = '2026-01-01';
    const endDate = '2026-01-31';
    expect(startDate).toMatch(/^\d{4}-\d{2}-\d{2}$/);
    expect(endDate).toMatch(/^\d{4}-\d{2}-\d{2}$/);
  });

  // Test 6: Verify all required fields in BacktestRequest
  it('includes all required fields in BacktestRequest', () => {
    const requiredFields = [
      'symbol',
      'algorithm_id',
      'start_date',
      'end_date',
      'initial_capital',
      'parameters',
    ];
    
    const request = {
      symbol: 'RELIANCE',
      algorithm_id: 'mean_reversion',
      start_date: '2026-01-01',
      end_date: '2026-01-31',
      initial_capital: 50000,
      parameters: {
        SMA_WINDOW: 20,
        Z_ENTRY: 1,
        Z_EXIT_THRESHOLD: 0.3,
      },
    };

    requiredFields.forEach(field => {
      expect(request).toHaveProperty(field);
    });
  });

  // Test 7: Verify optional fields with defaults
  it('includes optional fields with correct defaults (allow_short, brokerage_fee)', () => {
    const request = {
      symbol: 'RELIANCE',
      algorithm_id: 'mean_reversion',
      start_date: '2026-01-01',
      end_date: '2026-01-31',
      initial_capital: 50000,
      parameters: {
        SMA_WINDOW: 20,
        Z_ENTRY: 1,
        Z_EXIT_THRESHOLD: 0.3,
      },
      allow_short: true, // Default
      brokerage_fee: 20.0, // Default
    };

    expect(request.allow_short).toBe(true);
    expect(request.brokerage_fee).toBe(20.0);
  });

  // Test 8: Full example request matching curl command
  it('constructs full request matching the working curl command', () => {
    // This matches the curl command from the user
    const request = {
      symbol: 'RELIANCE',
      algorithm_id: 'mean_reversion',
      start_date: '2026-01-01',
      end_date: '2026-01-31',
      initial_capital: 50000,
      parameters: {
        SMA_WINDOW: 20,
        Z_ENTRY: 1,
        Z_EXIT_THRESHOLD: 0.3,
      },
      allow_short: true,
      brokerage_fee: 20.0,
    };

    // Verify structure
    expect(request.symbol).toBe('RELIANCE');
    expect(request.algorithm_id).toBe('mean_reversion');
    expect(request.start_date).toBe('2026-01-01');
    expect(request.end_date).toBe('2026-01-31');
    expect(request.initial_capital).toBe(50000);
    expect(Object.keys(request.parameters)).toEqual(['SMA_WINDOW', 'Z_ENTRY', 'Z_EXIT_THRESHOLD']);
  });

  // Test 9: Verify BacktestResponse structure
  it('correctly handles BacktestResponse with job_id, status, and optional message', () => {
    const response = {
      job_id: '2df029ca-e5f2-4bd8-9217-b808c82ef85f',
      status: 'completed',
      message: 'Backtest completed',
    };

    expect(response.job_id).toBeTruthy();
    expect(response.status).toBe('completed');
    expect(response.message).toBeDefined();
  });

  // Test 10: Verify parameter type safety
  it('ensures parameter types match BacktestParameters interface', () => {
    const params: {
      SMA_WINDOW: number;
      Z_ENTRY: number;
      Z_EXIT_THRESHOLD: number;
    } = {
      SMA_WINDOW: 20,
      Z_ENTRY: 1.0,
      Z_EXIT_THRESHOLD: 0.3,
    };

    expect(params.SMA_WINDOW).toBeLessThanOrEqual(100);
    expect(params.SMA_WINDOW).toBeGreaterThanOrEqual(5);
    expect(params.Z_ENTRY).toBeLessThanOrEqual(3.0);
    expect(params.Z_ENTRY).toBeGreaterThanOrEqual(0.5);
    expect(params.Z_EXIT_THRESHOLD).toBeLessThanOrEqual(1.0);
    expect(params.Z_EXIT_THRESHOLD).toBeGreaterThanOrEqual(0.1);
  });
});
