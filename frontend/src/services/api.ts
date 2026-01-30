import axios, { AxiosInstance, AxiosError } from 'axios';
import { Algorithm } from '../types/algorithm';
import { BacktestRequest, BacktestResponse, BacktestStatus } from '../types/backtest';
import { Trade, BacktestResults } from '../types/results';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api/v1';

class ApiClient {
  private axiosInstance: AxiosInstance;

  constructor() {
    this.axiosInstance = axios.create({
      baseURL: API_BASE_URL,
      headers: {
        'Content-Type': 'application/json',
      },
    });

    // Add response interceptor for error handling
    this.axiosInstance.interceptors.response.use(
      (response) => response,
      (error: AxiosError) => {
        console.error('API Error:', error.response?.data || error.message);
        return Promise.reject(error);
      }
    );
  }

  // Stock endpoints
  async getStocks(): Promise<string[]> {
    const response = await this.axiosInstance.get<string[]>('/stocks');
    return response.data;
  }

  // Algorithm endpoints
  async getAlgorithms(): Promise<Algorithm[]> {
    const response = await this.axiosInstance.get<Algorithm[]>('/algorithms');
    return response.data;
  }

  // Backtest endpoints
  async submitBacktest(request: BacktestRequest): Promise<BacktestResponse> {
    const response = await this.axiosInstance.post<BacktestResponse>(
      '/backtest',
      request
    );
    return response.data;
  }

  async getBacktestStatus(jobId: string): Promise<BacktestStatus> {
    const response = await this.axiosInstance.get<BacktestStatus>(
      `/backtest/${jobId}/status`
    );
    return response.data;
  }

  // Results endpoints
  async getResults(jobId: string): Promise<BacktestResults> {
    const response = await this.axiosInstance.get<BacktestResults>(
      `/results/${jobId}`
    );
    return response.data;
  }

  // Trades endpoints
  async getTrades(jobId: string): Promise<Trade[]> {
    const response = await this.axiosInstance.get<Trade[]>(
      `/trades/${jobId}`
    );
    return response.data;
  }
}

export const apiClient = new ApiClient();
export default ApiClient;
