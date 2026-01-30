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
