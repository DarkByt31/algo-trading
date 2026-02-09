import axios, { AxiosInstance, AxiosError } from 'axios';
import { Algorithm } from '../types/algorithm';
import { BacktestRequest, BacktestResponse, BacktestStatus } from '../types/backtest';
import { Trade, BacktestResults } from '../types/results';
import { Stock } from '../types/api';

// Use relative `/api` by default so browser requests use the same origin
// and are handled by the Vite dev server proxy. If you need an explicit
// base URL override, set `VITE_API_BASE_URL` in the environment.
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || '/api';

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
    try {
      const response = await this.axiosInstance.get<Stock[]>('/stocks');
      // Extract just the symbols from the stock objects
      return response.data.map((stock: Stock) => stock.symbol);
    } catch (error) {
      console.error('Failed to fetch stocks:', error);
      throw error;
    }
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
    const response = await this.axiosInstance.get<any>(
      `/results/${jobId}`
    );
    // Backend returns nested structure with backtest_result
    const data = response.data;
    if (data.backtest_result) {
      // Flatten the nested structure and include job metadata
      return {
        job_id: data.job_id,
        status: data.status,
        symbol: data.symbol,
        algorithm: data.algorithm_id,
        start_date: data.start_date,
        end_date: data.end_date,
        initial_capital: data.initial_capital,
        final_capital: data.backtest_result.final_capital,
        total_return: data.backtest_result.total_return,
        return_percentage: data.backtest_result.return_percentage,
        total_trades: data.backtest_result.total_trades,
        winning_trades: data.backtest_result.winning_trades || 0,
        losing_trades: data.backtest_result.losing_trades || 0,
        win_rate: data.backtest_result.win_rate || 0,
        chart_data: data.backtest_result.chart_data,
      };
    }
    return data;
  }

  // Trades endpoints
  async getTrades(jobId: string): Promise<Trade[]> {
    const response = await this.axiosInstance.get<any>(
      `/trades/${jobId}`
    );
    // Backend returns sequential trades (entry and exit as separate records)
    // We need to pair them together into complete trades
    if (response.data.trades && Array.isArray(response.data.trades)) {
      const trades: Trade[] = [];
      const backendTrades = response.data.trades;
      
      // Track open positions to pair with exits
      let entryTrade: any = null;
      
      for (const trade of backendTrades) {
        // Opening trade (BUY or SELL)
        if (trade.type === 'BUY' || trade.type === 'SELL') {
          entryTrade = trade;
        }
        // Closing trade (EXIT)
        else if (trade.type === 'EXIT' && entryTrade) {
          trades.push({
            id: entryTrade.id,
            job_id: jobId,
            symbol: entryTrade.symbol,
            entry_date: entryTrade.time,
            entry_price: entryTrade.price,
            exit_date: trade.time,
            exit_price: trade.price,
            quantity: trade.quantity,
            pnl: trade.pnl || 0,
            type: entryTrade.type,
          });
          entryTrade = null;
        }
      }
      
      return trades;
    }
    return response.data;
  }
}

export const apiClient = new ApiClient();
export default ApiClient;
