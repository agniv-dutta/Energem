import axios from 'axios';

const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000',
  timeout: 30000,
  headers: { 'Content-Type': 'application/json' },
});

export async function simulateScenario(params: {
  corridor: string;
  disruption_percent: number;
  duration_days: number;
  affected_nodes: string[];
  scenario_name: string;
  alternatives_activated?: boolean;
}) {
  const { data } = await api.post('/api/scenarios/simulate', params);
  return data;
}

export async function fetchProcurementRecommendations(params?: { scenario_id?: string; status?: string }) {
  const { data } = await api.get('/api/procurement/recommendations', { params });
  return data;
}

export async function authorizeRecommendations(params: {
  recommendation_ids: string[];
  authorized_by: string;
  authorization_level: 'directorate_b' | 'ministry' | 'emergency';
  reason: string;
}) {
  const { data } = await api.post('/api/procurement/authorize', params);
  return data;
}

export async function fetchLatestSignals(category = 'all') {
  const { data } = await api.get('/api/signals/latest', { params: { category } });
  return data;
}

export default api;
