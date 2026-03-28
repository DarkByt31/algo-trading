import { useState, useEffect } from 'react';
import { apiClient } from '../services/api';
import { Trade } from '../types/results';

export const useTrades = (jobId?: string) => {
  const [trades, setTrades] = useState<Trade[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!jobId) return;

    const fetchTrades = async () => {
      setLoading(true);
      setError(null);
      try {
        const data = await apiClient.getTrades(jobId);
        setTrades(data);
      } catch (err: unknown) {
        const errorMessage = err instanceof Error ? err.message : 'Failed to fetch trades';
        setError(errorMessage);
      } finally {
        setLoading(false);
      }
    };

    fetchTrades();
  }, [jobId]);

  return {
    trades,
    loading,
    error,
  };
};
