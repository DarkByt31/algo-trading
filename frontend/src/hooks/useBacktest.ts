import { useState } from 'react';
import { apiClient } from '../services/api';
import { BacktestRequest, BacktestResponse } from '../types/backtest';

export const useBacktest = () => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [jobId, setJobId] = useState<string | null>(null);

  const submitBacktest = async (request: BacktestRequest): Promise<BacktestResponse> => {
    setLoading(true);
    setError(null);
    try {
      const response = await apiClient.submitBacktest(request);
      setJobId(response.job_id);
      return response;
    } catch (err: unknown) {
      const errorMessage = err instanceof Error ? err.message : 'Failed to submit backtest';
      setError(errorMessage);
      throw err;
    } finally {
      setLoading(false);
    }
  };

  return {
    loading,
    error,
    jobId,
    submitBacktest,
  };
};
