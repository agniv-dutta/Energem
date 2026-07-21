import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import { Settings, Activity, Gauge, Network } from 'lucide-react';
import { fetchLandingData, type LandingData } from '../services/api';
import './Landing.css';

const mockLandingData: LandingData = {
  risk_score: 72,
  trend_delta: 18,
  trend_direction: "up",
  trend_hours: 24,
  top_corridor: "hormuz",
  last_3_signals: [
    { timestamp: "08:42Z", event: "HORMUZ STRAIT / KINETIC ACTIVITY DETECTED", confidence: "HIGH", risk_delta: "+8%" },
    { timestamp: "09:15Z", event: "PARADIP TERMINAL / PRESSURE ANOMALY", confidence: "MEDIUM", risk_delta: "+2%" },
    { timestamp: "09:42Z", event: "MALACCA STRAIT / VESSEL DEVIATION", confidence: "HIGH", risk_delta: "+5%" },
  ],
  feed_status: "ACTIVE",
  last_updated_at: new Date().toISOString()
};

const COMPASS_BEARINGS = [
  { angle: 0, label: 'OVERVIEW', route: '/overview' },
  { angle: 72, label: 'LOGISTICS', route: '/map' },
  { angle: 144, label: 'FORECAST', route: '/simulator' },
  { angle: 216, label: 'PROCUREMENT', route: '/procurement' },
  { angle: 288, label: 'INTELLIGENCE', route: '/intelligence' },
];

const Landing: React.FC = () => {
  const navigate = useNavigate();
  const [data, setData] = useState<LandingData | null>(null);
  const [loading, setLoading] = useState(true);
  const [tickerIndex, setTickerIndex] = useState(0);

  const fetchData = async () => {
    try {
      const landingData = await fetchLandingData();
      setData(landingData);
      setLoading(false);
    } catch {
      setData(mockLandingData);
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
    const interval = setInterval(fetchData, 60000);
    return () => clearInterval(interval);
  }, []);

  useEffect(() => {
    if (!data || data.last_3_signals.length === 0) return;
    const tickerInterval = setInterval(() => {
      setTickerIndex(prev => (prev + 1) % data.last_3_signals.length);
    }, 5000);
    return () => clearInterval(tickerInterval);
  }, [data]);

  if (loading || !data) {
    return <div className="landing-page font-data" style={{ justifyContent: 'center' }}>INITIALIZING SYSTEM...</div>;
  }

  const needleRotation = (data.risk_score / 100) * 180 - 90;

  return (
    <div className="landing-page">
      <div className="landing-container">
        <header className="landing-masthead">
          <div className="masthead-logo">ENERGEM</div>
          <div className="masthead-center">
            <div className="gauge-container">
              <svg className="gauge-svg" viewBox="0 0 120 60">
                <path d="M 10 50 A 50 50 0 0 1 110 50" fill="none" stroke="#333" strokeWidth="6" strokeLinecap="round" />
                <path d="M 10 50 A 50 50 0 0 1 30 18" fill="none" stroke="#75c4b8" strokeWidth="6" strokeLinecap="round" />
                <path d="M 30 18 A 50 50 0 0 1 90 18" fill="none" stroke="#d09c5a" strokeWidth="6" strokeLinecap="round" />
                <path d="M 90 18 A 50 50 0 0 1 110 50" fill="none" stroke="#d85252" strokeWidth="6" strokeLinecap="round" />
                <motion.g
                  initial={{ rotate: -90 }}
                  animate={{ rotate: needleRotation }}
                  transition={{ duration: 1.2, ease: "easeOut" }}
                  style={{ transformOrigin: '60px 50px' }}
                >
                  <polygon points="58,50 62,50 60,10" fill="#E2892C" />
                  <circle cx="60" cy="50" r="4" fill="#E2892C" />
                </motion.g>
              </svg>
              <div className="gauge-label font-data">SYSTEM PRESSURE: {data.risk_score} PSI</div>
            </div>
          </div>
          <div className="masthead-actions">
            <button className="icon-btn" style={{ color: 'var(--cyanotype)' }}><Settings size={20} /></button>
          </div>
        </header>

        <div className="landing-ticker font-data">
          <div className="ticker-content fade-in" key={tickerIndex}>
            <div className="ticker-item">
              {data.last_3_signals[tickerIndex].timestamp} — {data.last_3_signals[tickerIndex].event} / CONFIDENCE: {data.last_3_signals[tickerIndex].confidence} ▶
            </div>
            {data.last_3_signals.length > 1 && (
              <div className="ticker-item" style={{ opacity: 0.5 }}>
                {data.last_3_signals[(tickerIndex + 1) % data.last_3_signals.length].timestamp} — {data.last_3_signals[(tickerIndex + 1) % data.last_3_signals.length].event}
              </div>
            )}
          </div>
        </div>

        <section className="landing-hero">
          <div className="hero-status font-data">OPERATIONAL STATUS: CRITICAL</div>

          <div className="compass-rose-container">
            <svg viewBox="0 0 400 400" className="compass-rose-svg">
              <circle cx="200" cy="200" r="190" stroke="#A67C3D" strokeWidth="0.5" fill="none" opacity="0.2" />
              <circle cx="200" cy="200" r="150" stroke="#4E8C86" strokeWidth="2" fill="none" />
              <circle cx="200" cy="200" r="60" stroke="#A67C3D" strokeWidth="0.5" fill="none" opacity="0.3" />

              {COMPASS_BEARINGS.map((bearing) => {
                const rad = (bearing.angle - 90) * (Math.PI / 180);
                const outerX = 200 + 140 * Math.cos(rad);
                const outerY = 200 + 140 * Math.sin(rad);
                const innerX = 200 + 65 * Math.cos(rad);
                const innerY = 200 + 65 * Math.sin(rad);
                const labelX = 200 + 172 * Math.cos(rad);
                const labelY = 200 + 172 * Math.sin(rad);

                return (
                  <g key={bearing.angle}
                     onClick={() => navigate(bearing.route)}
                     style={{ cursor: 'pointer' }}
                     className="compass-bearing">
                    <line x1={innerX} y1={innerY} x2={outerX} y2={outerY}
                          stroke="#A67C3D" strokeWidth="1.5" />
                    <circle cx={outerX} cy={outerY} r="30"
                            fill="transparent" />
                    <text x={labelX} y={labelY - 8}
                          textAnchor="middle" fill="#4E8C86"
                          fontSize="14" fontWeight="bold"
                          fontFamily="'IBM Plex Mono', monospace"
                          className="bearing-angle-label">
                      {bearing.angle.toString().padStart(3, '0')}°
                    </text>
                    <text x={labelX} y={labelY + 10}
                          textAnchor="middle" fill="#C9C2AE"
                          fontSize="10"
                          fontFamily="'IBM Plex Mono', monospace"
                          className="bearing-name-label">
                      {bearing.label}
                    </text>
                  </g>
                );
              })}

              <circle cx="200" cy="200" r="42"
                      stroke="#A67C3D" strokeWidth="2" fill="none"
                      onClick={() => navigate('/overview')}
                      style={{ cursor: 'pointer' }} />
              <text x="200" y="194" textAnchor="middle"
                    fill="#E2892C" fontSize="11" fontWeight="bold"
                    fontFamily="'Rajdhani', sans-serif"
                    onClick={() => navigate('/overview')}
                    style={{ cursor: 'pointer' }}>
                ENTER
              </text>
              <text x="200" y="210" textAnchor="middle"
                    fill="#E2892C" fontSize="10" fontWeight="bold"
                    fontFamily="'Rajdhani', sans-serif"
                    onClick={() => navigate('/overview')}
                    style={{ cursor: 'pointer' }}>
                DASHBOARD
              </text>
            </svg>
          </div>

          <h1 className="hero-title font-display">
            SUPPLY RESILIENCE WHEN<br />
            <span className="highlight">EVERY HOUR COUNTS</span>
          </h1>
          <p className="hero-subtitle">
            Real-time disruption signals. Impact forecasts. Procurement intelligence.<br />
            Engineered for India's critical energy infrastructure.
          </p>
          <div className="cta-container">
            <button className="cta-button font-display" onClick={() => navigate('/overview')}>
              ENTER DASHBOARD
            </button>
          </div>
        </section>

        <section className="landing-value-prop">
          <div className="value-col">
            <div className="value-col-header font-data">
              <Activity className="value-icon" />
              <span className="value-title">DETECT</span>
            </div>
            <p className="value-desc">
              Sub-millisecond signal capture from global maritime transponders and pipeline telemetry. We isolate the noise to deliver 100% verified disruption alerts.
            </p>
          </div>
          <div className="value-col">
            <div className="value-col-header font-data">
              <Gauge className="value-icon" />
              <span className="value-title">FORECAST</span>
            </div>
            <p className="value-desc">
              AI-driven simulation modeling identifying supply chain vulnerabilities 47 hours before market impact. From kinetic events to weather-driven outages.
            </p>
          </div>
          <div className="value-col">
            <div className="value-col-header font-data">
              <Network className="value-icon" />
              <span className="value-title">EXECUTE</span>
            </div>
            <p className="value-desc">
              Automated procurement intelligence and re-routing. Shorten response windows from 47 days to 47 minutes with integrated logistical protocol execution.
            </p>
          </div>
        </section>

        <div className="landing-info-bar font-data">
          <span>©2024 ENERGYGUARD INDUSTRIAL SYSTEMS | TERMINAL 07-B | SYSTEM STATS: NOMINAL PRESSURE: {data.risk_score} PSI RISK: ELEVATED LAT: 29.7604° N LON: 95.3698° W</span>
        </div>

        <section className="landing-stats font-data">
          <div className="stat-col">
            <div className="stat-label">LATENCY</div>
            <div className="stat-value">0.004 <span className="stat-unit">MS</span></div>
          </div>
          <div className="stat-col">
            <div className="stat-label">MODEL ACCURACY</div>
            <div className="stat-value">99.2<span className="stat-unit">%</span></div>
          </div>
          <div className="stat-col">
            <div className="stat-label">EXECUTION WINDOW</div>
            <div className="stat-value">47 <span className="stat-unit">MIN</span></div>
          </div>
        </section>

        <section className="landing-visualizer">
          <div className="visualizer-box">
            <div className="visualizer-title font-data">SUPPLY CHAIN SCHEMATIC</div>
            <svg viewBox="0 0 800 300" className="node-viz-svg">
              <g className="origin-nodes">
                <rect x="10" y="20" width="100" height="36" fill="#14171A" stroke="#4E8C86" strokeWidth="1.5" />
                <text x="60" y="43" textAnchor="middle" fontSize="9" fill="#4E8C86" fontWeight="bold" fontFamily="'IBM Plex Mono', monospace">SAUDI ARABIA</text>
                <rect x="10" y="70" width="100" height="36" fill="#14171A" stroke="#4E8C86" strokeWidth="1.5" />
                <text x="60" y="93" textAnchor="middle" fontSize="9" fill="#4E8C86" fontWeight="bold" fontFamily="'IBM Plex Mono', monospace">IRAQ</text>
                <rect x="10" y="120" width="100" height="36" fill="#14171A" stroke="#4E8C86" strokeWidth="1.5" />
                <text x="60" y="143" textAnchor="middle" fontSize="9" fill="#4E8C86" fontWeight="bold" fontFamily="'IBM Plex Mono', monospace">IRAN</text>
                <rect x="10" y="180" width="100" height="36" fill="#14171A" stroke="#E2892C" strokeWidth="1.5" />
                <text x="60" y="203" textAnchor="middle" fontSize="9" fill="#E2892C" fontWeight="bold" fontFamily="'IBM Plex Mono', monospace">AFRICA/ME</text>
                <rect x="10" y="240" width="100" height="36" fill="#14171A" stroke="#A67C3D" strokeWidth="1.5" />
                <text x="60" y="263" textAnchor="middle" fontSize="9" fill="#A67C3D" fontWeight="bold" fontFamily="'IBM Plex Mono', monospace">RUSSIA</text>
              </g>

              <g className="chokepoint-nodes">
                <circle cx="380" cy="55" r="32" fill="none" stroke="#B23A2E" strokeWidth="2" />
                <line x1="368" y1="55" x2="392" y2="55" stroke="#B23A2E" strokeWidth="1.5" />
                <text x="380" y="52" textAnchor="middle" fontSize="8" fill="#B23A2E" fontWeight="bold" fontFamily="'IBM Plex Mono', monospace">HORMUZ</text>
                <text x="380" y="62" textAnchor="middle" fontSize="7" fill="#B23A2E" fontFamily="'IBM Plex Mono', monospace">97.5%</text>

                <circle cx="380" cy="130" r="32" fill="none" stroke="#E2892C" strokeWidth="2" />
                <line x1="368" y1="130" x2="392" y2="130" stroke="#E2892C" strokeWidth="1.5" />
                <text x="380" y="127" textAnchor="middle" fontSize="8" fill="#E2892C" fontWeight="bold" fontFamily="'IBM Plex Mono', monospace">RED SEA</text>
                <text x="380" y="137" textAnchor="middle" fontSize="7" fill="#E2892C" fontFamily="'IBM Plex Mono', monospace">86.4%</text>

                <circle cx="380" cy="205" r="32" fill="none" stroke="#A67C3D" strokeWidth="2" />
                <line x1="368" y1="205" x2="392" y2="205" stroke="#A67C3D" strokeWidth="1.5" />
                <text x="380" y="202" textAnchor="middle" fontSize="8" fill="#A67C3D" fontWeight="bold" fontFamily="'IBM Plex Mono', monospace">MALACCA</text>
                <text x="380" y="212" textAnchor="middle" fontSize="7" fill="#A67C3D" fontFamily="'IBM Plex Mono', monospace">42.2%</text>

                <circle cx="380" cy="270" r="28" fill="none" stroke="#74804A" strokeWidth="1.5" />
                <line x1="370" y1="270" x2="390" y2="270" stroke="#74804A" strokeWidth="1" />
                <text x="380" y="268" textAnchor="middle" fontSize="8" fill="#74804A" fontWeight="bold" fontFamily="'IBM Plex Mono', monospace">SUEZ</text>
                <text x="380" y="277" textAnchor="middle" fontSize="7" fill="#74804A" fontFamily="'IBM Plex Mono', monospace">35.8%</text>
              </g>

              <g className="routing-lines" opacity="0.8">
                <line x1="110" y1="38" x2="348" y2="55" stroke="#B23A2E" strokeWidth="1.5" />
                <line x1="110" y1="88" x2="348" y2="55" stroke="#B23A2E" strokeWidth="1.5" />
                <line x1="110" y1="138" x2="348" y2="55" stroke="#B23A2E" strokeWidth="1.5" />
                <line x1="110" y1="198" x2="348" y2="130" stroke="#E2892C" strokeWidth="1.5" />
                <line x1="110" y1="258" x2="348" y2="205" stroke="#A67C3D" strokeWidth="1.5" />

                <line x1="412" y1="55" x2="640" y2="150" stroke="#4E8C86" strokeWidth="1.5" />
                <line x1="412" y1="130" x2="640" y2="150" stroke="#4E8C86" strokeWidth="1.5" />
                <line x1="412" y1="205" x2="640" y2="150" stroke="#4E8C86" strokeWidth="1.5" />
                <line x1="408" y1="270" x2="640" y2="150" stroke="#4E8C86" strokeWidth="1" opacity="0.5" />
              </g>

              <g className="destination-node">
                <rect x="640" y="120" width="120" height="60" fill="#14171A" stroke="#4E8C86" strokeWidth="2" />
                <text x="700" y="148" textAnchor="middle" fontSize="12" fill="#4E8C86" fontWeight="bold" fontFamily="'IBM Plex Mono', monospace">INDIA</text>
                <text x="700" y="165" textAnchor="middle" fontSize="9" fill="#A67C3D" fontFamily="'IBM Plex Mono', monospace">REFINERY</text>
              </g>
            </svg>
            <div className="visualizer-footer font-data">
              <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                <div style={{ width: '8px', height: '8px', backgroundColor: 'var(--cyanotype)' }}></div>
                <span>LIVE FEED: TERMINAL-07</span>
              </div>
              <div>LAT: 29.7604° N | LON: 95.3698° W</div>
            </div>
          </div>
          <div className="visualizer-text">
            <h2 className="visualizer-heading font-display">
              MECHANICAL<br />PRECISION DATA
            </h2>
            <div className="visualizer-item">
              <div className="visualizer-item-title font-data">DIRECT ASSET TELEMETRY</div>
              <div className="visualizer-item-desc">Hard-wired connection to physical infrastructure sensors bypassing public internet protocols.</div>
            </div>
            <div className="visualizer-item">
              <div className="visualizer-item-title font-data">STRATEGIC RESERVE ANALYSIS</div>
              <div className="visualizer-item-desc">Real-time balancing of regional storage capacities against predicted demand surges.</div>
            </div>
            <div className="visualizer-item">
              <div className="visualizer-item-title font-data">GEOPOLITICAL RISK ENGINE</div>
              <div className="visualizer-item-desc">Machine-learned impact scoring of kinetic and diplomatic shifts in energy corridors.</div>
            </div>
          </div>
        </section>
      </div>
    </div>
  );
};

export default Landing;
