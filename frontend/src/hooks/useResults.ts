import { useState, useEffect, useCallback } from 'react';
import { apiClient } from '../services/api';
import { BacktestResults } from '../types/results';

interface UseResultsOptions {
  jobId?: string;
  pollInterval?: number;
}

export const useResults = ({ jobId, pollInterval = 2000 }: UseResultsOptions = {}) => {
  const [results, setResults] = useState<BacktestResults | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const fetchResults = useCallback(async (id: string) => {
    setLoading(true);
    setError(null);
    try {
      const data = await apiClient.getResults(id);
      setResults(data);
    } catch (err: unknown) {
      const errorMessage = err instanceof Error ? err.message : 'Failed to fetch results';
      setError(errorMessage);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    if (!jobId) return;

    // Initial fetch
    fetchResults(jobId);

    // Set up polling
    const interval = setInterval(() => {
      fetchResults(jobId);
    }, pollInterval);

    return () => clearInterval(interval);
  }, [jobId, pollInterval, fetchResults]);

  return {
    results,
    loading,
    error,
    refetch: () => jobId && fetchResults(jobId),
  };
};
