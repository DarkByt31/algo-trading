import { useState, useEffect } from 'react';
import { apiClient } from '../services/api';
import { Algorithm } from '../types/algorithm';

export const useAlgorithms = () => {
  const [algorithms, setAlgorithms] = useState<Algorithm[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchAlgorithms = async () => {
      setLoading(true);
      setError(null);
      try {
        const data = await apiClient.getAlgorithms();
        setAlgorithms(data);
      } catch (err: unknown) {
        const errorMessage = err instanceof Error ? err.message : 'Failed to fetch algorithms';
        setError(errorMessage);
      } finally {
        setLoading(false);
      }
    };

    fetchAlgorithms();
  }, []);

  return {
    algorithms,
    loading,
    error,
  };
};
