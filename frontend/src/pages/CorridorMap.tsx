import React, { useEffect, useRef, useCallback } from 'react';
import { useAppStore, type CorridorData } from '../store/useAppStore';
import { fetchCorridors, type CorridorStatus } from '../services/api';
import CorridorDetailsModal from '../components/CorridorDetailsModal';
import RerouteModal from '../components/RerouteModal';
import './CorridorMap.css';

const POLL_INTERVAL_MS = 30_000;

function formatFlow(bbl: number): string {
  if (bbl >= 1_000_000) return `${(bbl / 1_000_000).toFixed(1)}M bbl`;
  if (bbl >= 1_000) return `${(bbl / 1_000).toFixed(0)}K bbl`;
  return `${bbl} bbl`;
}

function heatmapClass(score: number): string {
  if (score >= 70) return 'heatmap-high';
  if (score >= 40) return 'heatmap-mid';
  return 'heatmap-low';
}

function confidenceColor(c: string): string {
  if (c === 'high') return 'text-red';
  if (c === 'medium') return 'text-amber';
  return 'text-teal';
}

function corridorToCorridorData(c: CorridorStatus): CorridorData {
  return {
    name: c.name,
    riskScore: c.risk_score,
    probability: c.active_threats > 0 ? Math.min(100, c.risk_score * 0.85) : 0,
    dailyFlow: formatFlow(c.daily_flow_bbl),
    confidence: c.confidence.charAt(0).toUpperCase() + c.confidence.slice(1),
    historicalBaseline: c.historical_baseline_risk,
    trend: c.trend,
    activeThreats: c.active_threats,
    lastSignal: c.last_signal,
    alternativeRoutes: c.alternative_routes,
  };
}

const CorridorMap: React.FC = () => {
  const selectedCorridor = useAppStore((s) => s.selectedCorridor);
  const modalType = useAppStore((s) => s.modalType);
  const setSelectedCorridor = useAppStore((s) => s.setSelectedCorridor);
  const corridors = useAppStore((s) => s.corridors);
  const corridorsUpdatedAt = useAppStore((s) => s.corridorsUpdatedAt);
  const corridorsLoading = useAppStore((s) => s.corridorsLoading);
  const setCorridors = useAppStore((s) => s.setCorridors);
  const setCorridorsLoading = useAppStore((s) => s.setCorridorsLoading);

  const timerRef = useRef<ReturnType<typeof setInterval> | null>(null);

  const loadCorridors = useCallback(async () => {
    setCorridorsLoading(true);
    try {
      const data = await fetchCorridors();
      setCorridors(data.corridors, data.updated_at);
    } catch {
      // keep stale data on error
    } finally {
      setCorridorsLoading(false);
    }
  }, [setCorridors, setCorridorsLoading]);

  useEffect(() => {
    loadCorridors();
    timerRef.current = setInterval(loadCorridors, POLL_INTERVAL_MS);
    return () => {
      if (timerRef.current) clearInterval(timerRef.current);
    };
  }, [loadCorridors]);

  const topCorridor = corridors[0] ?? null;
  const topScore = topCorridor?.risk_score ?? 0;
  const topFlow = topCorridor ? formatFlow(topCorridor.daily_flow_bbl) : '--';
  const topKey = topCorridor?.name?.toUpperCase() ?? 'HORMUZ';
  const topThreat = topCorridor?.active_threats ?? 0;

  const updatedTime = corridorsUpdatedAt
    ? new Date(corridorsUpdatedAt).toISOString().replace('T', ' ').slice(0, 19) + ' ZULU'
    : new Date().toISOString().replace('T', ' ').slice(0, 19) + ' ZULU';

  return (
    <div className="corridor-page">
      <div className="ticker-bar">
        <div className="ticker-content">
          <span>SYSTEM STATUS: NOMINAL</span>
          <span className="ticker-sep">//</span>
          <span>DATA LATENCY: {corridorsLoading ? 'FETCHING...' : '40MS'}</span>
          <span className="ticker-sep">//</span>
          <span className="text-amber">TOP THREAT: {topKey} @ {topScore.toFixed(0)}%</span>
          <span className="ticker-sep">//</span>
          <span>ACTIVE THREATS: {corridors.reduce((a, c) => a + c.active_threats, 0)}</span>
          <span className="ticker-sep">//</span>
          <span>GLOBAL FLOW RATE: 78.4M BBL/DAY</span>
          <span className="ticker-sep">//</span>
          <span>SYSTEM STATUS: NOMINAL</span>
          <span className="ticker-sep">//</span>
          <span>DATA LATENCY: {corridorsLoading ? 'FETCHING...' : '40MS'}</span>
          <span className="ticker-sep">//</span>
          <span className="text-amber">TOP THREAT: {topKey} @ {topScore.toFixed(0)}%</span>
          <span className="ticker-sep">//</span>
          <span>ACTIVE THREATS: {corridors.reduce((a, c) => a + c.active_threats, 0)}</span>
          <span className="ticker-sep">//</span>
          <span>GLOBAL FLOW RATE: 78.4M BBL/DAY</span>
        </div>
      </div>

      <div className="corridor-title-section">
        <div className="corridor-title-left">
          <h2 className="corridor-title">SUPPLY CORRIDOR ALPHA-7</h2>
          <p className="corridor-subtitle">P&amp;ID SCHEMATIC // REAL-TIME TRANSIT VECTORING</p>
        </div>
        <div className="corridor-title-right">
          <div className={`latency-badge ${corridorsLoading ? 'text-amber' : 'text-teal'}`}>
            {corridorsLoading ? 'UPDATING...' : 'LIVE: 30S POLL'}
          </div>
          <div className="timestamp">{updatedTime}</div>
        </div>
      </div>

      <div className="map-schematic panel">
        <svg viewBox="0 0 900 420" className="schematic-svg" xmlns="http://www.w3.org/2000/svg">
          <rect x="60" y="80" width="60" height="30" fill="#2a2a2a" stroke="#555" strokeWidth="1"/>
          <text x="90" y="115" fill="#888" fontSize="10" textAnchor="middle" fontFamily="'Share Tech Mono', monospace">RUSSIA</text>
          <line x1="120" y1="95" x2="300" y2="95" stroke="#75c4b8" strokeWidth="1" strokeDasharray="4 4" opacity="0.7"/>
          <line x1="300" y1="95" x2="420" y2="200" stroke="#75c4b8" strokeWidth="1" strokeDasharray="4 4" opacity="0.7"/>
          <line x1="420" y1="200" x2="420" y2="260" stroke="#75c4b8" strokeWidth="1" strokeDasharray="4 4" opacity="0.7"/>
          <line x1="0" y1="230" x2="380" y2="230" stroke="#d85252" strokeWidth="1.5" strokeDasharray="6 4" opacity="0.8"/>
          <line x1="520" y1="230" x2="900" y2="230" stroke="#d85252" strokeWidth="1.5" strokeDasharray="6 4" opacity="0.8"/>
          <line x1="0" y1="340" x2="350" y2="340" stroke="#d85252" strokeWidth="1.5" strokeDasharray="6 4" opacity="0.5"/>
          <line x1="420" y1="290" x2="350" y2="340" stroke="#75c4b8" strokeWidth="1" strokeDasharray="4 4" opacity="0.5"/>
          <rect x="380" y="220" width="180" height="80" fill="#1a1a1a" stroke="#555" strokeWidth="1"/>
          <text x="395" y="242" fill="#e0e0e0" fontSize="10" fontFamily="'Share Tech Mono', monospace" letterSpacing="1">
            CHOKEPOINT: {topKey}
          </text>
          <polygon points="565,228 572,234 565,240" fill="#d09c5a"/>
          <line x1="390" y1="250" x2="550" y2="250" stroke="#333" strokeWidth="0.5"/>
          <text x="395" y="268" fill="#888" fontSize="9" fontFamily="'Share Tech Mono', monospace">RISK INDEX</text>
          <text x="540" y="268" fill="#d85252" fontSize="11" fontFamily="'Share Tech Mono', monospace" textAnchor="end" fontWeight="bold">
            {topScore.toFixed(0)}%
          </text>
          <text x="395" y="286" fill="#888" fontSize="9" fontFamily="'Share Tech Mono', monospace">THREATS</text>
          <text x="540" y="286" fill="#d09c5a" fontSize="11" fontFamily="'Share Tech Mono', monospace" textAnchor="end" fontWeight="bold">
            {topThreat}
          </text>
          <rect x="395" y="292" width="145" height="3" fill="#d85252"/>
        </svg>

        <div className="map-legend panel">
          <div className="legend-item">
            <div className="legend-swatch" style={{backgroundColor: '#75c4b8'}}></div>
            <span>OPTIMAL FLOW</span>
          </div>
          <div className="legend-item">
            <div className="legend-swatch" style={{backgroundColor: '#d09c5a'}}></div>
            <span>THROTTLED / RISK</span>
          </div>
          <div className="legend-item">
            <div className="legend-swatch" style={{backgroundColor: '#d85252'}}></div>
            <span>CRITICAL BLOCKADE</span>
          </div>
        </div>
      </div>

      <div className="globe-section">
        <div className="globe-label">GGN° OVERVIEW</div>
      </div>

      <div className="manifest-section">
        <div className="manifest-header">
          <span className="manifest-title">RISK MANIFEST LOG // SEGMENT DATA</span>
          <span className="auto-refresh">
            {corridorsLoading ? 'REFRESHING...' : `AUTO-REFRESH: 30S`}
          </span>
        </div>
        <table className="manifest-table">
          <thead>
            <tr>
              <th>CORRIDOR ID</th>
              <th>THREAT VECTOR</th>
              <th>RISK SCORE</th>
              <th>TREND</th>
              <th>HEATMAP</th>
              <th>ACTION</th>
            </tr>
          </thead>
          <tbody>
            {corridors.length === 0 && (
              <tr>
                <td colSpan={6} style={{ textAlign: 'center', color: '#666', padding: '20px' }}>
                  {corridorsLoading ? 'LOADING CORRIDORS...' : 'NO CORRIDOR DATA — RUN /api/signals/refresh'}
                </td>
              </tr>
            )}
            {corridors.map((c) => {
              const data = corridorToCorridorData(c);
              return (
                <tr key={c.id}>
                  <td>{c.id}</td>
                  <td className={confidenceColor(c.confidence)}>
                    {c.name.toUpperCase()}
                    {c.active_threats > 0 && (
                      <span style={{ marginLeft: 6, fontSize: 9, color: '#d85252' }}>
                        [{c.active_threats} THREAT{c.active_threats > 1 ? 'S' : ''}]
                      </span>
                    )}
                  </td>
                  <td>{c.risk_score.toFixed(1)}%</td>
                  <td style={{ fontSize: 10, color: c.trend?.startsWith('+') ? '#d85252' : c.trend?.startsWith('-') ? '#75c4b8' : '#888' }}>
                    {c.trend || '--'}
                  </td>
                  <td>
                    <div className="heatmap-bar">
                      <div
                        className={`heatmap-fill ${heatmapClass(c.risk_score)}`}
                        style={{ width: `${Math.min(100, c.risk_score)}%` }}
                      ></div>
                    </div>
                  </td>
                  <td>
                    <button className="table-btn" onClick={() => setSelectedCorridor(data, 'details')}>
                      DETAILS
                    </button>
                    {c.risk_score >= 60 && (
                      <button
                        className="table-btn table-btn-danger"
                        onClick={() => setSelectedCorridor(data, 'reroute')}
                        style={{ marginLeft: 8 }}
                      >
                        REROUTE
                      </button>
                    )}
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>

      {selectedCorridor && modalType === 'details' && <CorridorDetailsModal corridor={selectedCorridor} />}
      {selectedCorridor && modalType === 'reroute' && <RerouteModal corridor={selectedCorridor} />}
    </div>
  );
};

export default CorridorMap;
