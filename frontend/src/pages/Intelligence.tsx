import React from 'react';
import './Intelligence.css';

const Intelligence: React.FC = () => {
  return (
    <div className="intel-page">
      {/* Header Section */}
      <div className="intel-header-section">
        <div className="intel-header-left">
          <h2 className="intel-main-title">INTELLIGENCE TELEX</h2>
          <p className="intel-subtitle text-teal">SIGNAL INTERCEPT FEED // PRIORITY CHANNEL ALPHA</p>
        </div>
        <div className="intel-header-right">
          <div className="intel-meta">FEED STATUS: <span className="text-teal">ACTIVE</span></div>
          <div className="intel-meta">CLEARANCE: <span className="text-main">LEVEL 4</span></div>
          <div className="intel-timestamp">LAST SYNC: 09:04:22Z</div>
        </div>
      </div>

      {/* Filter Bar */}
      <div className="intel-filter-bar">
        <div className="filter-tabs">
          <button className="filter-tab active">ALL SIGNALS</button>
          <button className="filter-tab">GEOPOLITICAL</button>
          <button className="filter-tab">MARITIME</button>
          <button className="filter-tab">SANCTIONS</button>
          <button className="filter-tab">MARKET</button>
        </div>
        <div className="filter-right">
          <div className="signal-count">
            <span className="count-value text-amber">12</span>
            <span className="count-label">ACTIVE SIGNALS</span>
          </div>
        </div>
      </div>

      {/* Telex Messages */}
      <div className="telex-feed">
        {/* Message 1 - Critical */}
        <div className="telex-msg critical">
          <div className="telex-priority-bar critical-bar"></div>
          <div className="telex-timestamp-col">
            <div className="telex-time">08:42Z</div>
            <div className="telex-date">27-OCT</div>
            <div className="telex-priority-tag critical-tag">CRITICAL</div>
          </div>
          <div className="telex-body">
            <div className="telex-header-row">
              <h4 className="telex-title">HORMUZ STRAIT — KINETIC ACTIVITY DETECTED</h4>
              <div className="telex-source">SRC: SIGINT-KAPPA-09</div>
            </div>
            <div className="telex-classification">
              <span className="class-badge">CLASSIFICATION: OPEN</span>
              <span className="corridor-badge">CORRIDOR: HORMUZ</span>
              <span className="conf-badge">CONFIDENCE: HIGH</span>
            </div>
            <p className="telex-content">
              Multiple fast-attack craft observed conducting interdiction maneuvers near coordinates 26.5°N, 56.2°E. Pattern consistent with IRGCN harassment operations. Commercial tanker MARE ATLANTIS (IMO 9823456) forced course deviation. Recommend advisory upgrade for all eastbound transits through TSS.
            </p>
            <div className="telex-meta-row">
              <div className="telex-metric">
                <span className="tm-label">RISK DELTA</span>
                <span className="tm-value text-red">+18%</span>
              </div>
              <div className="telex-metric">
                <span className="tm-label">IMPACT RADIUS</span>
                <span className="tm-value">REGIONAL</span>
              </div>
              <div className="telex-metric">
                <span className="tm-label">PRECEDENT</span>
                <span className="tm-value text-amber">2024-YEM-ATK</span>
              </div>
              <div className="telex-metric">
                <span className="tm-label">DECAY</span>
                <span className="tm-value">48H</span>
              </div>
            </div>
          </div>
        </div>

        {/* Message 2 - Elevated */}
        <div className="telex-msg elevated">
          <div className="telex-priority-bar elevated-bar"></div>
          <div className="telex-timestamp-col">
            <div className="telex-time">07:15Z</div>
            <div className="telex-date">27-OCT</div>
            <div className="telex-priority-tag elevated-tag">ELEVATED</div>
          </div>
          <div className="telex-body">
            <div className="telex-header-row">
              <h4 className="telex-title">OFAC REGISTRY UPDATE — IRAN SANCTIONS EXPANSION</h4>
              <div className="telex-source">SRC: REGULATORY-FEED</div>
            </div>
            <div className="telex-classification">
              <span className="class-badge">CLASSIFICATION: OPEN</span>
              <span className="corridor-badge">CORRIDOR: IRAN-IND</span>
              <span className="conf-badge">CONFIDENCE: HIGH</span>
            </div>
            <p className="telex-content">
              US Treasury OFAC designates 14 additional entities linked to Iranian petroleum exports. Includes 3 shipping companies previously routing via Fujairah STS transfer. Indian refiners with active term contracts face 90-day compliance window. Estimated supply impact: 180K BBL/DAY.
            </p>
            <div className="telex-meta-row">
              <div className="telex-metric">
                <span className="tm-label">RISK DELTA</span>
                <span className="tm-value text-amber">+8%</span>
              </div>
              <div className="telex-metric">
                <span className="tm-label">IMPACT RADIUS</span>
                <span className="tm-value">BILATERAL</span>
              </div>
              <div className="telex-metric">
                <span className="tm-label">PRECEDENT</span>
                <span className="tm-value text-amber">2022-SANC-03</span>
              </div>
              <div className="telex-metric">
                <span className="tm-label">DECAY</span>
                <span className="tm-value">90D</span>
              </div>
            </div>
          </div>
        </div>

        {/* Message 3 - Routine */}
        <div className="telex-msg routine">
          <div className="telex-priority-bar routine-bar"></div>
          <div className="telex-timestamp-col">
            <div className="telex-time">05:30Z</div>
            <div className="telex-date">27-OCT</div>
            <div className="telex-priority-tag routine-tag">ROUTINE</div>
          </div>
          <div className="telex-body">
            <div className="telex-header-row">
              <h4 className="telex-title">BRENT CRUDE SPOT — INTRADAY VOLATILITY ALERT</h4>
              <div className="telex-source">SRC: MARKET-ENGINE</div>
            </div>
            <div className="telex-classification">
              <span className="class-badge">CLASSIFICATION: OPEN</span>
              <span className="corridor-badge">CORRIDOR: GLOBAL</span>
              <span className="conf-badge">CONFIDENCE: MEDIUM</span>
            </div>
            <p className="telex-content">
              Brent futures (BZ=F) registered 3.2% intraday swing following Hormuz incident reports. Current spot: $84.22/BBL. Options market implied volatility at 6-month high. Algorithmic traders increasing short-term hedge positions. Pattern correlation with Q4-2023 Red Sea disruption cycle.
            </p>
            <div className="telex-meta-row">
              <div className="telex-metric">
                <span className="tm-label">RISK DELTA</span>
                <span className="tm-value text-teal">+3%</span>
              </div>
              <div className="telex-metric">
                <span className="tm-label">IMPACT RADIUS</span>
                <span className="tm-value">GLOBAL</span>
              </div>
              <div className="telex-metric">
                <span className="tm-label">PRECEDENT</span>
                <span className="tm-value text-teal">BASELINE</span>
              </div>
              <div className="telex-metric">
                <span className="tm-label">DECAY</span>
                <span className="tm-value">24H</span>
              </div>
            </div>
          </div>
        </div>

        {/* Message 4 - Watch */}
        <div className="telex-msg routine">
          <div className="telex-priority-bar routine-bar"></div>
          <div className="telex-timestamp-col">
            <div className="telex-time">03:12Z</div>
            <div className="telex-date">27-OCT</div>
            <div className="telex-priority-tag routine-tag">WATCH</div>
          </div>
          <div className="telex-body">
            <div className="telex-header-row">
              <h4 className="telex-title">ARCTIC ROUTE — SEASONAL ICE FORMATION FORECAST</h4>
              <div className="telex-source">SRC: METEO-GRID</div>
            </div>
            <div className="telex-classification">
              <span className="class-badge">CLASSIFICATION: OPEN</span>
              <span className="corridor-badge">CORRIDOR: RUS-IND</span>
              <span className="conf-badge">CONFIDENCE: MEDIUM</span>
            </div>
            <p className="telex-content">
              Northern Sea Route ice coverage advancing 12 days ahead of seasonal average. COR-RUS-IND-01 transit window closing. Recommend pre-positioning vessels for final Q4 Arctic transits. Alternative routing via Suez adds 8-10 days to delivery schedules from Murmansk.
            </p>
            <div className="telex-meta-row">
              <div className="telex-metric">
                <span className="tm-label">RISK DELTA</span>
                <span className="tm-value text-teal">+2%</span>
              </div>
              <div className="telex-metric">
                <span className="tm-label">IMPACT RADIUS</span>
                <span className="tm-value">CORRIDOR</span>
              </div>
              <div className="telex-metric">
                <span className="tm-label">PRECEDENT</span>
                <span className="tm-value text-teal">SEASONAL</span>
              </div>
              <div className="telex-metric">
                <span className="tm-label">DECAY</span>
                <span className="tm-value">30D</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Intelligence;
