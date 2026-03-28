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
  const [isCompleted, setIsCompleted] = useState(false);

  const fetchResults = useCallback(async (id: string) => {
    setLoading(true);
    setError(null);
    try {
      const data = await apiClient.getResults(id);
      setResults(data);
      // Stop polling if status is completed or failed
      if (data.status === 'completed' || data.status === 'failed') {
        setIsCompleted(true);
      }
    } catch (err: unknown) {
      const errorMessage = err instanceof Error ? err.message : 'Failed to fetch results';
      setError(errorMessage);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    if (!jobId || isCompleted) return;

    // Initial fetch
    fetchResults(jobId);

    // Set up polling - only if not completed
    const interval = setInterval(() => {
      fetchResults(jobId);
    }, pollInterval);

    return () => clearInterval(interval);
  }, [jobId, pollInterval, fetchResults, isCompleted]);

  return {
    results,
    loading,
    error,
    isCompleted,
    refetch: () => {
      setIsCompleted(false);
      jobId && fetchResults(jobId);
    },
  };
};
