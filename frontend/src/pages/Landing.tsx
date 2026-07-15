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
            <nav className="compass-nav font-data">
              <a href="#" className="compass-link active">000° LOGISTICS</a>
              <a href="#" className="compass-link">090° REFINERY</a>
              <a href="#" className="compass-link">180° PIPELINE</a>
              <a href="#" className="compass-link">270° STORAGE</a>
            </nav>
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
            <div className="visualizer-title font-data">NODE_VISUALIZATION_V4</div>
            <div style={{ height: '300px', backgroundColor: '#1a1a1a', display: 'flex', alignItems: 'center', justifyContent: 'center', border: '1px solid #333' }}>
              <Network size={64} style={{ opacity: 0.2, color: 'var(--cyanotype)' }} />
            </div>
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
