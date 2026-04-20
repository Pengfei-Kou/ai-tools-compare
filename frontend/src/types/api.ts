export interface AIModel {
  id: number;
  name: string;
  provider: string;
  description: string | null;
  input_price: number;
  output_price: number;
  context_window: number;
  category: string;
  is_active: boolean;
}

export interface AIModelList {
  models: AIModel[];
  total: number;
}
