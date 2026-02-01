// API response types
export interface ApiResponse<T> {
  data: T;
  status: number;
  message?: string;
}

export interface ApiError {
  detail: string | { message: string };
  status: number;
}

// Stock types
export interface Stock {
  symbol: string;
  name: string;
  exchange: string;
  sector: string;
}
