// Algorithm-related types
export interface AlgorithmParameter {
  name: string;
  type: 'integer' | 'float' | 'string' | 'boolean';
  default: string | number | boolean;
  min?: number;
  max?: number;
  description: string;
}

export interface Algorithm {
  id: string;
  name: string;
  description: string;
  version: string;
  is_active: boolean;
  parameters: AlgorithmParameter[];
}
