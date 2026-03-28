import { useState, useEffect } from 'react';
import { apiClient } from '../services/api';

export const useStocks = () => {
  const [stocks, setStocks] = useState<string[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchStocks = async () => {
      setLoading(true);
      setError(null);
      try {
        const data = await apiClient.getStocks();
        setStocks(data);
      } catch (err: unknown) {
        const errorMessage = err instanceof Error ? err.message : 'Failed to fetch stocks';
        console.error('Error fetching stocks:', errorMessage);
        setError(errorMessage);
        setStocks([]); // Reset stocks on error
      } finally {
        setLoading(false);
      }
    };

    fetchStocks();
  }, []);

  return {
    stocks,
    loading,
    error,
  };
};
