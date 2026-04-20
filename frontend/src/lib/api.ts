import type { AIModelList } from '../types/api';

const API_URL = import.meta.env.PUBLIC_API_URL;

export async function fetchModels(): Promise<AIModelList> {
  const res = await fetch(`${API_URL}/models/`);
  if (!res.ok) {
    throw new Error(`API error: ${res.status}`);
  }
  return res.json();
}
