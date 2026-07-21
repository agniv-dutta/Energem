import React, { useEffect, useRef, useCallback } from 'react';
import { useAppStore, type CorridorData } from '../store/useAppStore';
import { fetchCorridors, type CorridorStatus } from '../services/api';
import CorridorDetailsModal from '../components/CorridorDetailsModal';
import RerouteModal from '../components/RerouteModal';
import './CorridorMap.css';

const POLL_INTERVAL_MS = 30_000;

const CORRIDOR_COLORS: Record<string, string> = {
  'COR-HORMUZ-01': '#B23A2E',
  'COR-RED-SEA-01': '#E2892C',
  'COR-MALACCA-04': '#A67C3D',
  'COR-SUEZ-03': '#74804A',
  'COR-LAND-02': '#4E8C86',
};

const CORRIDOR_NAMES: Record<string, string> = {
  'COR-HORMUZ-01': 'STRAIT OF HORMUZ',
  'COR-RED-SEA-01': 'RED SEA / BAB AL-MANDAB',
  'COR-MALACCA-04': 'STRAIT OF MALACCA',
  'COR-SUEZ-03': 'SUEZ CANAL',
  'COR-LAND-02': 'LAND / RAIL ROUTES',
};

function formatFlow(bbl: number): string {
  if (bbl >= 1_000_000) return `${(bbl / 1_000_000).toFixed(1)}M bbl`;
  if (bbl >= 1_000) return `${(bbl / 1_000).toFixed(0)}K bbl`;
  return `${bbl} bbl`;
}

function getRiskColor(score: number): string {
  if (score >= 80) return '#B23A2E';
  if (score >= 60) return '#E2892C';
  if (score >= 40) return '#A67C3D';
  return '#74804A';
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

  const corridorLookup = corridors.reduce((acc, c) => {
    acc[c.id] = c;
    return acc;
  }, {} as Record<string, CorridorStatus>);

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
          <defs>
            <marker id="arrow-teal" markerWidth="6" markerHeight="4" refX="5" refY="2" orient="auto">
              <polygon points="0 0, 6 2, 0 4" fill="#4E8C86" />
            </marker>
          </defs>

          {/* Origin Nodes - Left Side */}
          <g className="origin-nodes">
            <rect x="20" y="30" width="90" height="32" fill="#1a1a1a" stroke="#4E8C86" strokeWidth="1" />
            <text x="65" y="50" fill="#4E8C86" fontSize="8" textAnchor="middle" fontFamily="'Share Tech Mono', monospace" fontWeight="bold">SAUDI ARABIA</text>

            <rect x="20" y="80" width="90" height="32" fill="#1a1a1a" stroke="#4E8C86" strokeWidth="1" />
            <text x="65" y="100" fill="#4E8C86" fontSize="8" textAnchor="middle" fontFamily="'Share Tech Mono', monospace" fontWeight="bold">IRAQ</text>

            <rect x="20" y="130" width="90" height="32" fill="#1a1a1a" stroke="#4E8C86" strokeWidth="1" />
            <text x="65" y="150" fill="#4E8C86" fontSize="8" textAnchor="middle" fontFamily="'Share Tech Mono', monospace" fontWeight="bold">IRAN</text>

            <rect x="20" y="220" width="90" height="32" fill="#1a1a1a" stroke="#E2892C" strokeWidth="1" />
            <text x="65" y="240" fill="#E2892C" fontSize="8" textAnchor="middle" fontFamily="'Share Tech Mono', monospace" fontWeight="bold">AFRICA / ME</text>

            <rect x="20" y="310" width="90" height="32" fill="#1a1a1a" stroke="#A67C3D" strokeWidth="1" />
            <text x="65" y="330" fill="#A67C3D" fontSize="8" textAnchor="middle" fontFamily="'Share Tech Mono', monospace" fontWeight="bold">RUSSIA</text>

            <rect x="20" y="370" width="90" height="32" fill="#1a1a1a" stroke="#74804A" strokeWidth="1" />
            <text x="65" y="390" fill="#74804A" fontSize="8" textAnchor="middle" fontFamily="'Share Tech Mono', monospace" fontWeight="bold">EU / AFRICA</text>
          </g>

          {/* Chokepoint Nodes - Middle */}
          <g className="chokepoint-nodes">
            {/* Hormuz - Critical */}
            <circle cx="380" cy="60" r="30" fill="none" stroke="#B23A2E" strokeWidth="2" />
            <line x1="370" y1="60" x2="390" y2="60" stroke="#B23A2E" strokeWidth="1.5" />
            <text x="380" y="57" fill="#B23A2E" fontSize="7" textAnchor="middle" fontFamily="'Share Tech Mono', monospace" fontWeight="bold">HORMUZ</text>
            <text x="380" y="66" fill="#B23A2E" fontSize="6" textAnchor="middle" fontFamily="'Share Tech Mono', monospace">
              {corridorLookup['COR-HORMUZ-01']?.risk_score.toFixed(1) ?? '97.5'}%
            </text>

            {/* Red Sea - High */}
            <circle cx="380" cy="160" r="30" fill="none" stroke="#E2892C" strokeWidth="2" />
            <line x1="370" y1="160" x2="390" y2="160" stroke="#E2892C" strokeWidth="1.5" />
            <text x="380" y="157" fill="#E2892C" fontSize="7" textAnchor="middle" fontFamily="'Share Tech Mono', monospace" fontWeight="bold">RED SEA</text>
            <text x="380" y="166" fill="#E2892C" fontSize="6" textAnchor="middle" fontFamily="'Share Tech Mono', monospace">
              {corridorLookup['COR-RED-SEA-01']?.risk_score.toFixed(1) ?? '86.4'}%
            </text>

            {/* Malacca - Moderate */}
            <circle cx="380" cy="260" r="30" fill="none" stroke="#A67C3D" strokeWidth="2" />
            <line x1="370" y1="260" x2="390" y2="260" stroke="#A67C3D" strokeWidth="1.5" />
            <text x="380" y="257" fill="#A67C3D" fontSize="7" textAnchor="middle" fontFamily="'Share Tech Mono', monospace" fontWeight="bold">MALACCA</text>
            <text x="380" y="266" fill="#A67C3D" fontSize="6" textAnchor="middle" fontFamily="'Share Tech Mono', monospace">
              {corridorLookup['COR-MALACCA-04']?.risk_score.toFixed(1) ?? '42.2'}%
            </text>

            {/* Suez - Low */}
            <circle cx="380" cy="340" r="25" fill="none" stroke="#74804A" strokeWidth="1.5" />
            <line x1="372" y1="340" x2="388" y2="340" stroke="#74804A" strokeWidth="1" />
            <text x="380" y="338" fill="#74804A" fontSize="7" textAnchor="middle" fontFamily="'Share Tech Mono', monospace" fontWeight="bold">SUEZ</text>
            <text x="380" y="346" fill="#74804A" fontSize="6" textAnchor="middle" fontFamily="'Share Tech Mono', monospace">
              {corridorLookup['COR-SUEZ-03']?.risk_score.toFixed(1) ?? '35.8'}%
            </text>
          </g>

          {/* Destination Node - Right */}
          <g className="destination-node">
            <rect x="680" y="170" width="100" height="50" fill="#1a1a1a" stroke="#4E8C86" strokeWidth="2" />
            <text x="730" y="193" fill="#4E8C86" fontSize="12" textAnchor="middle" fontFamily="'Share Tech Mono', monospace" fontWeight="bold">INDIA</text>
            <text x="730" y="208" fill="#A67C3D" fontSize="8" textAnchor="middle" fontFamily="'Share Tech Mono', monospace">REFINERY</text>
          </g>

          {/* Routing Lines: Origin → Chokepoint (color-coded by corridor) */}
          <g className="routing-lines" opacity="0.85">
            {/* Saudi Arabia → Hormuz */}
            <line x1="110" y1="46" x2="350" y2="60" stroke="#B23A2E" strokeWidth="1.5" strokeDasharray="4 2" />
            {/* Iraq → Hormuz */}
            <line x1="110" y1="96" x2="350" y2="60" stroke="#B23A2E" strokeWidth="1.5" strokeDasharray="4 2" />
            {/* Iran → Hormuz */}
            <line x1="110" y1="146" x2="350" y2="60" stroke="#B23A2E" strokeWidth="1.5" strokeDasharray="4 2" />

            {/* Africa/ME → Red Sea */}
            <line x1="110" y1="236" x2="350" y2="160" stroke="#E2892C" strokeWidth="1.5" strokeDasharray="4 2" />

            {/* Russia → Malacca */}
            <line x1="110" y1="326" x2="350" y2="260" stroke="#A67C3D" strokeWidth="1.5" strokeDasharray="4 2" />

            {/* EU/Africa → Suez */}
            <line x1="110" y1="386" x2="355" y2="340" stroke="#74804A" strokeWidth="1" strokeDasharray="4 2" />
          </g>

          {/* Routing Lines: Chokepoint → India (teal) */}
          <g className="convergence-lines" opacity="0.7">
            <line x1="410" y1="60" x2="680" y2="195" stroke="#4E8C86" strokeWidth="1.5" markerEnd="url(#arrow-teal)" />
            <line x1="410" y1="160" x2="680" y2="195" stroke="#4E8C86" strokeWidth="1.5" markerEnd="url(#arrow-teal)" />
            <line x1="410" y1="260" x2="680" y2="195" stroke="#4E8C86" strokeWidth="1.5" markerEnd="url(#arrow-teal)" />
            <line x1="405" y1="340" x2="680" y2="195" stroke="#4E8C86" strokeWidth="1" opacity="0.5" markerEnd="url(#arrow-teal)" />
          </g>

          {/* Risk Scale Legend (Bottom Left) */}
          <g className="risk-legend" transform="translate(20, 430)">
            <text x="0" y="-8" fill="#888" fontSize="8" fontFamily="'Share Tech Mono', monospace" letterSpacing="1">RISK SCALE:</text>
            <rect x="0" y="0" width="40" height="6" fill="#B23A2E" />
            <text x="44" y="6" fill="#B23A2E" fontSize="7" fontFamily="'Share Tech Mono', monospace">CRITICAL</text>
            <rect x="100" y="0" width="40" height="6" fill="#E2892C" />
            <text x="144" y="6" fill="#E2892C" fontSize="7" fontFamily="'Share Tech Mono', monospace">HIGH</text>
            <rect x="190" y="0" width="40" height="6" fill="#A67C3D" />
            <text x="234" y="6" fill="#A67C3D" fontSize="7" fontFamily="'Share Tech Mono', monospace">MODERATE</text>
            <rect x="310" y="0" width="40" height="6" fill="#74804A" />
            <text x="354" y="6" fill="#74804A" fontSize="7" fontFamily="'Share Tech Mono', monospace">LOW</text>
          </g>
        </svg>

        <div className="map-legend panel">
          <div className="legend-item">
            <div className="legend-swatch" style={{backgroundColor: '#B23A2E'}}></div>
            <span>CRITICAL (80%+)</span>
          </div>
          <div className="legend-item">
            <div className="legend-swatch" style={{backgroundColor: '#E2892C'}}></div>
            <span>HIGH (60-80%)</span>
          </div>
          <div className="legend-item">
            <div className="legend-swatch" style={{backgroundColor: '#A67C3D'}}></div>
            <span>MODERATE (40-60%)</span>
          </div>
          <div className="legend-item">
            <div className="legend-swatch" style={{backgroundColor: '#74804A'}}></div>
            <span>LOW (&lt;40%)</span>
          </div>
        </div>
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
              <th>ROUTE NAME</th>
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
              const corridorColor = CORRIDOR_COLORS[c.id] || getRiskColor(c.risk_score);
              return (
                <tr key={c.id}>
                  <td style={{ color: corridorColor, fontWeight: 500 }}>{c.id}</td>
                  <td className={confidenceColor(c.confidence)}>
                    {CORRIDOR_NAMES[c.id] || c.name.toUpperCase()}
                    {c.active_threats > 0 && (
                      <span style={{ marginLeft: 6, fontSize: 9, color: '#d85252' }}>
                        [{c.active_threats} THREAT{c.active_threats > 1 ? 'S' : ''}]
                      </span>
                    )}
                  </td>
                  <td style={{ color: corridorColor, fontWeight: 500 }}>{c.risk_score.toFixed(1)}%</td>
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
