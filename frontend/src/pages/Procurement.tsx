import React from 'react';
import './Procurement.css';

const Procurement: React.FC = () => {
  return (
    <div className="procurement-page">
      {/* Page Header */}
      <div className="proc-header-section">
        <div className="proc-header-left">
          <h2 className="proc-main-title">PROCUREMENT<br/>RECOMMENDATIONS</h2>
          <p className="proc-subtitle text-teal">STRATEGIC ACQUISITION MANIFEST // SECTOR 7G-12</p>
        </div>
        <div className="proc-header-right">
          <div className="proc-meta-line">LAST UPDATED: 04:22:10Z</div>
          <div className="proc-authority">AUTHORITY LEVEL:</div>
          <div className="proc-authority-value">OMEGA</div>
        </div>
      </div>

      {/* Priority Cards */}
      <div className="proc-cards">
        {/* Priority 01 */}
        <div className="proc-card panel">
          <div className="proc-card-accent"></div>
          <div className="proc-card-number">01</div>
          <div className="proc-card-body">
            <h3 className="proc-card-title">PRIORITY 01 — INCREASE RUSSIAN IMPORTS</h3>
            <div className="proc-card-metrics">
              <div className="proc-metric">
                <div className="proc-metric-label">VOLUME</div>
                <div className="proc-metric-value text-teal">300K BBL/DAY</div>
              </div>
              <div className="proc-metric">
                <div className="proc-metric-label">EST. ARRIVAL</div>
                <div className="proc-metric-value text-teal">12 DAYS</div>
              </div>
              <div className="proc-metric">
                <div className="proc-metric-label">LOGISTICS STATUS</div>
                <div className="proc-metric-value text-teal">CLEAR</div>
              </div>
              <div className="proc-metric">
                <div className="proc-metric-label">SENSITIVITY</div>
                <div className="proc-metric-value text-amber">CRITICAL</div>
              </div>
            </div>
            <div className="proc-card-footer">
              <div className="proc-badge approved">APPROVED BY DIRECTORATE B</div>
              <span className="proc-footer-text">Manifest verified against refinery intake schedules for terminal K-92.</span>
            </div>
          </div>
          <div className="proc-card-confidence">
            <div className="confidence-label">CONFIDENCE METRIC</div>
            <div className="confidence-bars">
              <div className="conf-bar filled"></div>
              <div className="conf-bar filled"></div>
              <div className="conf-bar filled"></div>
              <div className="conf-bar filled"></div>
              <div className="conf-bar filled"></div>
              <div className="conf-bar filled"></div>
              <div className="conf-bar filled"></div>
              <div className="conf-bar filled dark"></div>
              <div className="conf-bar filled dark"></div>
              <div className="conf-bar"></div>
            </div>
            <div className="confidence-footer">
              <span>90% PROB</span>
              <span>RATING: A+</span>
            </div>
          </div>
        </div>

        {/* Priority 02 */}
        <div className="proc-card panel">
          <div className="proc-card-accent"></div>
          <div className="proc-card-number">02</div>
          <div className="proc-card-body">
            <h3 className="proc-card-title">PRIORITY 02 — SPOT MARKET DIESEL ARBITRAGE</h3>
            <div className="proc-card-metrics">
              <div className="proc-metric">
                <div className="proc-metric-label">VOLUME</div>
                <div className="proc-metric-value text-teal">150K BBL/DAY</div>
              </div>
              <div className="proc-metric">
                <div className="proc-metric-label">EST. ARRIVAL</div>
                <div className="proc-metric-value text-teal">4 DAYS</div>
              </div>
              <div className="proc-metric">
                <div className="proc-metric-label">LOGISTICS STATUS</div>
                <div className="proc-metric-value text-amber">DELAY RISK</div>
              </div>
              <div className="proc-metric">
                <div className="proc-metric-label">COST INDEX</div>
                <div className="proc-metric-value text-teal">LOW</div>
              </div>
            </div>
            <div className="proc-card-footer">
              <div className="proc-badge pending">PENDING EXECUTION</div>
              <span className="proc-footer-text">Awaiting clearance from maritime security corridor 4.</span>
            </div>
          </div>
          <div className="proc-card-confidence">
            <div className="confidence-label">CONFIDENCE METRIC</div>
            <div className="confidence-bars">
              <div className="conf-bar filled"></div>
              <div className="conf-bar filled"></div>
              <div className="conf-bar filled"></div>
              <div className="conf-bar filled"></div>
              <div className="conf-bar filled"></div>
              <div className="conf-bar filled dark"></div>
              <div className="conf-bar filled dark"></div>
              <div className="conf-bar"></div>
              <div className="conf-bar"></div>
              <div className="conf-bar"></div>
            </div>
            <div className="confidence-footer">
              <span>65% PROB</span>
              <span>RATING: B</span>
            </div>
          </div>
        </div>

        {/* Priority 03 - Locked */}
        <div className="proc-card panel locked">
          <div className="proc-card-accent locked-accent"></div>
          <div className="proc-card-number dimmed">03</div>
          <div className="proc-card-body">
            <h3 className="proc-card-title dimmed">STRATEGIC RESERVE RELEASE: SECTOR 9</h3>
            <div className="proc-denied">
              <span className="text-red">PERMISSION DENIED — INSUFFICIENT AUTHORIZATION</span>
            </div>
          </div>
        </div>
      </div>

      {/* Authorize Button */}
      <div className="proc-authorize-section">
        <button className="authorize-btn">AUTHORIZE ALL PRIMARY RECOMMENDATIONS</button>
      </div>
    </div>
  );
};

export default Procurement;
