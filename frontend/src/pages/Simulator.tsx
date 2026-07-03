import React, { useState } from 'react';
import './Simulator.css';

const Simulator: React.FC = () => {
  const [severity, setSeverity] = useState(65);
  const [selectedDuration, setSelectedDuration] = useState('medium');

  return (
    <div className="simulator-page">
      <div className="sim-body">
        {/* Left Panel - Parameters */}
        <div className="sim-params-panel">
          <div className="sim-params-header">
            <h3>SET PARAMETERS</h3>
            <span className="config-mode">[CONFIG_MODE: MANUAL]</span>
          </div>

          {/* Disruption Severity */}
          <div className="param-section">
            <div className="param-label-row">
              <span className="param-label text-amber">DISRUPTION SEVERITY</span>
              <span className="param-value text-amber">{severity}%</span>
            </div>
            <div className="slider-container">
              <input
                type="range"
                min="0"
                max="100"
                value={severity}
                onChange={(e) => setSeverity(Number(e.target.value))}
                className="severity-slider"
              />
              <div className="slider-labels">
                <span>NOMINAL</span>
                <span>MODERATE</span>
                <span>CRITICAL</span>
              </div>
            </div>
          </div>

          {/* Duration */}
          <div className="param-section">
            <h4 className="param-section-title text-amber">DURATION (DAYS)</h4>
            <div className="duration-grid">
              <button
                className={`duration-btn ${selectedDuration === 'short' ? 'active' : ''}`}
                onClick={() => setSelectedDuration('short')}
              >
                <span className="dur-label">SHORT</span>
                <span className="dur-value">05 DAYS</span>
              </button>
              <button
                className={`duration-btn ${selectedDuration === 'medium' ? 'active' : ''}`}
                onClick={() => setSelectedDuration('medium')}
              >
                <span className="dur-label">MEDIUM</span>
                <span className="dur-value">15 DAYS</span>
              </button>
              <button
                className={`duration-btn ${selectedDuration === 'long' ? 'active' : ''}`}
                onClick={() => setSelectedDuration('long')}
              >
                <span className="dur-label">LONG</span>
                <span className="dur-value">30 DAYS</span>
              </button>
              <button
                className={`duration-btn ${selectedDuration === 'extreme' ? 'active' : ''}`}
                onClick={() => setSelectedDuration('extreme')}
              >
                <span className="dur-label">EXTREME</span>
                <span className="dur-value">90+ DAYS</span>
              </button>
            </div>
          </div>

          {/* Affected Nodes */}
          <div className="param-section">
            <h4 className="param-section-title text-amber">AFFECTED NODES</h4>
            <div className="nodes-list panel">
              <div className="node-item">
                <div className="node-checkbox checked"></div>
                <span>GULF_STREAM_PIPE_01</span>
              </div>
              <div className="node-item">
                <div className="node-checkbox"></div>
                <span>KEYSTONE_EXT_B</span>
              </div>
              <div className="node-item">
                <div className="node-checkbox checked"></div>
                <span>PORT_ARTHUR_REFINERY</span>
              </div>
            </div>
          </div>

          {/* Run Simulation Button */}
          <button className="run-sim-btn">RUN SIMULATION</button>
        </div>

        {/* Right Panel - Oscilloscope Output */}
        <div className="sim-output-panel">
          <div className="output-header">
            <h3>PROJECTED TIMELINE // OSCILLOSCOPE OUTPUT</h3>
            <div className="output-legend">
              <span className="legend-line supply">— SUPPLY LOSS</span>
              <span className="legend-line price">— PRICE SURGE</span>
            </div>
          </div>

          <div className="oscilloscope panel">
            {/* Grid */}
            <div className="osc-grid">
              <div className="osc-col">
                <div className="osc-col-label">DAY 01</div>
              </div>
              <div className="osc-col">
                <div className="osc-col-label">DAY 05</div>
              </div>
              <div className="osc-col">
                <div className="osc-col-label">DAY 10</div>
              </div>
              <div className="osc-col">
                <div className="osc-col-label">DAY 30</div>
              </div>
            </div>

            {/* SVG Lines */}
            <svg className="osc-svg" viewBox="0 0 600 280" preserveAspectRatio="none">
              {/* Supply loss line - dashed */}
              <polyline
                points="0,260 60,250 150,200 250,120 350,80 450,90 550,100 600,105"
                fill="none"
                stroke="#75c4b8"
                strokeWidth="1.5"
                strokeDasharray="6 3"
                opacity="0.8"
              />
              {/* Price surge line */}
              <polyline
                points="0,260 60,255 150,230 250,180 350,140 450,150 550,155 600,158"
                fill="none"
                stroke="#d09c5a"
                strokeWidth="1.5"
                strokeDasharray="6 3"
                opacity="0.8"
              />
            </svg>

            {/* Tooltip */}
            <div className="osc-tooltip">
              <div className="tooltip-header">DAY 15</div>
              <div className="tooltip-val">-420K</div>
              <div className="tooltip-unit">BBL/D</div>
              <div className="tooltip-price">+$12.40/BBL</div>
            </div>
          </div>

          {/* Bottom Results Metrics */}
          <div className="sim-results-row">
            <div className="sim-result panel">
              <div className="result-label">TOTAL DEFICIT</div>
              <div className="result-value text-teal">12.4M BBL</div>
            </div>
            <div className="sim-result panel">
              <div className="result-label">PRICE CEILING</div>
              <div className="result-value text-amber">$104.22</div>
            </div>
            <div className="sim-result panel">
              <div className="result-label">RECOVERY_EST</div>
              <div className="result-value text-red">42 DAYS</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Simulator;
