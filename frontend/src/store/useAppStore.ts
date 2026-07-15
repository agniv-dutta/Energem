import { create } from 'zustand';
import type { CorridorStatus } from '../services/api';

export type ModalType = 'details' | 'reroute' | null;

export interface CorridorData {
  name: string;
  riskScore: number;
  probability: number;
  dailyFlow: string;
  confidence: string;
  historicalBaseline: number;
  trend?: string;
  activeThreats?: number;
  lastSignal?: string;
  alternativeRoutes?: CorridorStatus['alternative_routes'];
}

export interface SimulationResult {
  scenario: string;
  parameters: Record<string, unknown>;
  timeline: Array<{
    day: number;
    supply_loss_bbl: number;
    spr_remaining_days: number;
    brent_price: number;
    brent_price_range: [number, number];
    refinery_utilization_pct: number;
    cumulative_deficit_bbl: number;
    flags: string[];
  }>;
  summary: {
    total_deficit_display: string;
    peak_price_display: string;
    spr_critical_day: number;
    gdp_impact_annualized_pct: number;
    recovery_estimate: string;
    recommended_actions: string[];
  };
  flags: Array<{ day: number; severity: string; message: string }>;
}

export interface Recommendation {
  id: number;
  title: string;
  volume: string;
  arrival: string;
  status: 'PENDING_EXECUTION' | 'PENDING_APPROVAL' | 'AUTHORIZED';
}

interface AppState {
  currentPage: string;
  simulationRunning: boolean;
  simulationResult: SimulationResult | null;
  selectedCorridor: CorridorData | null;
  modalType: ModalType;
  activeIntelligenceTab: string;
  authorizationStatus: Record<number, string>;
  recommendations: Recommendation[];
  toast: { message: string; type: 'success' | 'error' } | null;
  corridors: CorridorStatus[];
  corridorsUpdatedAt: string | null;
  corridorsLoading: boolean;

  setCurrentPage: (page: string) => void;
  setSimulationRunning: (v: boolean) => void;
  setSimulationResult: (r: SimulationResult | null) => void;
  setSelectedCorridor: (c: CorridorData | null, modal?: ModalType) => void;
  setActiveIntelligenceTab: (t: string) => void;
  setAuthorizationStatus: (s: Record<number, string>) => void;
  setRecommendations: (r: Recommendation[]) => void;
  showToast: (message: string, type: 'success' | 'error') => void;
  clearToast: () => void;
  setCorridors: (corridors: CorridorStatus[], updatedAt: string) => void;
  setCorridorsLoading: (v: boolean) => void;
}

export const useAppStore = create<AppState>((set) => ({
  currentPage: 'overview',
  simulationRunning: false,
  simulationResult: null,
  selectedCorridor: null,
  modalType: null,
  activeIntelligenceTab: 'all',
  authorizationStatus: {},
  recommendations: [],
  toast: null,
  corridors: [],
  corridorsUpdatedAt: null,
  corridorsLoading: false,

  setCurrentPage: (page) => set({ currentPage: page }),
  setSimulationRunning: (v) => set({ simulationRunning: v }),
  setSimulationResult: (r) => set({ simulationResult: r }),
  setSelectedCorridor: (c, modal) => set({ selectedCorridor: c, modalType: c ? modal ?? 'details' : null }),
  setActiveIntelligenceTab: (t) => set({ activeIntelligenceTab: t }),
  setAuthorizationStatus: (s) => set({ authorizationStatus: s }),
  setRecommendations: (r) => set({ recommendations: r }),
  showToast: (message, type) => set({ toast: { message, type } }),
  clearToast: () => set({ toast: null }),
  setCorridors: (corridors, updatedAt) => set({ corridors, corridorsUpdatedAt: updatedAt }),
  setCorridorsLoading: (v) => set({ corridorsLoading: v }),
}));
