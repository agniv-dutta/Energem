import React, { useState } from 'react';
import { useAppStore } from '../store/useAppStore';
import { simulateScenario } from '../services/api';
import './Simulator.css';

const DURATION_MAP: Record<string, number> = {
  short: 5,
  medium: 15,
  long: 30,
  extreme: 90,
};

const Simulator: React.FC = () => {
  const simulationRunning = useAppStore((s) => s.simulationRunning);
  const simulationResult = useAppStore((s) => s.simulationResult);
  const setSimulationRunning = useAppStore((s) => s.setSimulationRunning);
  const setSimulationResult = useAppStore((s) => s.setSimulationResult);
  const showToast = useAppStore((s) => s.showToast);

  const [severity, setSeverity] = useState(65);
  const [selectedDuration, setSelectedDuration] = useState('medium');
  const [selectedNodes, setSelectedNodes] = useState<Record<string, boolean>>({
    GULF_STREAM_PIPE_01: true,
    KEYSTONE_EXT_B: false,
    PORT_ARTHUR_REFINERY: true,
  });

  const nodeNames = Object.keys(selectedNodes);

  const handleRunSimulation = async () => {
    setSimulationRunning(true);
    setSimulationResult(null);
    try {
      const result = await simulateScenario({
        corridor: 'hormuz',
        disruption_percent: severity,
        duration_days: DURATION_MAP[selectedDuration] || 15,
        affected_nodes: nodeNames.filter((n) => selectedNodes[n]),
        scenario_name: `Hormuz ${severity}% closure, ${DURATION_MAP[selectedDuration] || 15} days`,
        alternatives_activated: true,
      });
      setSimulationResult(result);
    } catch {
      showToast('SIMULATION FAILED — CHECK BACKEND CONNECTION', 'error');
    } finally {
      setSimulationRunning(false);
    }
  };

  const toggleNode = (name: string) => {
    setSelectedNodes((prev) => ({ ...prev, [name]: !prev[name] }));
  };

  return (
    <div className="simulator-page">
      <div className="sim-body">
        {/* Left Panel - Parameters */}
        <div className="sim-params-panel">
          <div className="sim-params-header">
            <h3>SET PARAMETERS</h3>
            <span className="config-mode">[CONFIG_MODE: MANUAL]</span>
          </div>

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

          <div className="param-section">
            <h4 className="param-section-title text-amber">DURATION (DAYS)</h4>
            <div className="duration-grid">
              {['short', 'medium', 'long', 'extreme'].map((key) => (
                <button
                  key={key}
                  className={`duration-btn ${selectedDuration === key ? 'active' : ''}`}
                  onClick={() => setSelectedDuration(key)}
                >
                  <span className="dur-label">{key.toUpperCase()}</span>
                  <span className="dur-value">{DURATION_MAP[key]} DAYS</span>
                </button>
              ))}
            </div>
          </div>

          <div className="param-section">
            <h4 className="param-section-title text-amber">AFFECTED NODES</h4>
            <div className="nodes-list panel">
              {nodeNames.map((name) => (
                <div key={name} className="node-item" onClick={() => toggleNode(name)} style={{ cursor: 'pointer' }}>
                  <div className={`node-checkbox ${selectedNodes[name] ? 'checked' : ''}`}></div>
                  <span>{name}</span>
                </div>
              ))}
            </div>
          </div>

          <button className="run-sim-btn" onClick={handleRunSimulation} disabled={simulationRunning}>
            {simulationRunning ? 'SIMULATION RUNNING...' : 'RUN SIMULATION'}
          </button>
          {simulationRunning && <div className="sim-spinner" />}
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
            {simulationResult ? (
              <>
                <div className="osc-grid">
                  {simulationResult.timeline.map((t) => (
                    <div key={t.day} className="osc-col">
                      <div className="osc-col-label">DAY {String(t.day).padStart(2, '0')}</div>
                    </div>
                  ))}
                </div>

                <svg className="osc-svg" viewBox="0 0 600 280" preserveAspectRatio="none">
                  {simulationResult.timeline.length > 1 && (() => {
                    const maxLoss = Math.max(...simulationResult.timeline.map((t) => t.supply_loss_bbl));
                    const w = 600 / (simulationResult.timeline.length - 1);
                    const supplyPoints = simulationResult.timeline.map((t, i) => {
                      const x = i * w;
                      const y = 260 - (t.supply_loss_bbl / maxLoss) * 200;
                      return `${x},${y}`;
                    });
                    const pricePoints = simulationResult.timeline.map((t, i) => {
                      const x = i * w;
                      const y = 260 - ((t.brent_price - 90) / 60) * 200;
                      return `${x},${y}`;
                    });
                    return (
                      <>
                        <polyline points={supplyPoints.join(' ')} fill="none" stroke="#75c4b8" strokeWidth="2" strokeDasharray="6 3" opacity="0.9" />
                        <polyline points={pricePoints.join(' ')} fill="none" stroke="#d09c5a" strokeWidth="2" strokeDasharray="6 3" opacity="0.9" />
                        {/* Sharp markers at each data point */}
                        {simulationResult.timeline.map((t, i) => {
                          const sx = i * w;
                          const sy = 260 - (t.supply_loss_bbl / maxLoss) * 200;
                          const py = 260 - ((t.brent_price - 90) / 60) * 200;
                          return (
                            <g key={i}>
                              <circle cx={sx} cy={sy} r="4" fill="#75c4b8" stroke="#1a1a1a" strokeWidth="1" />
                              <circle cx={sx} cy={py} r="4" fill="#d09c5a" stroke="#1a1a1a" strokeWidth="1" />
                            </g>
                          );
                        })}
                      </>
                    );
                  })()}
                </svg>

                {/* Tooltips at each day marker */}
                <div className="osc-tooltip-row">
                  {simulationResult.timeline.map((t) => (
                    <div key={t.day} className="osc-tooltip-item">
                      <div className="tooltip-header">DAY {t.day}</div>
                      <div className="tooltip-val">-{t.supply_loss_bbl.toLocaleString()}</div>
                      <div className="tooltip-unit">BBL/D</div>
                      <div className="tooltip-price">${t.brent_price}/BBL</div>
                      <div className="tooltip-spr">SPR: {t.spr_remaining_days}d</div>
                    </div>
                  ))}
                </div>

                {/* Bottom Results Metrics */}
                <div className="sim-results-row">
                  <div className="sim-result panel">
                    <div className="result-label">TOTAL DEFICIT</div>
                    <div className="result-value text-teal">{simulationResult.summary.total_deficit_display}</div>
                  </div>
                  <div className="sim-result panel">
                    <div className="result-label">PRICE CEILING</div>
                    <div className="result-value text-amber">{simulationResult.summary.peak_price_display}</div>
                  </div>
                  <div className="sim-result panel">
                    <div className="result-label">RECOVERY_EST</div>
                    <div className="result-value text-red">{simulationResult.summary.recovery_estimate}</div>
                  </div>
                </div>

                {/* Flags */}
                {simulationResult.flags.length > 0 && (
                  <div className="sim-flags">
                    {simulationResult.flags.map((f, i) => (
                      <div key={i} className={`sim-flag ${f.severity === 'CRITICAL' ? 'flag-critical' : 'flag-warning'}`}>
                        [{f.severity}] {f.message}
                      </div>
                    ))}
                  </div>
                )}
              </>
            ) : (
              <div className="osc-placeholder">
                <div className="osc-grid">
                  <div className="osc-col"><div className="osc-col-label">DAY 01</div></div>
                  <div className="osc-col"><div className="osc-col-label">DAY 05</div></div>
                  <div className="osc-col"><div className="osc-col-label">DAY 10</div></div>
                  <div className="osc-col"><div className="osc-col-label">DAY 30</div></div>
                </div>
                <svg className="osc-svg" viewBox="0 0 600 280" preserveAspectRatio="none">
                  <polyline points="0,260 60,250 150,200 250,120 350,80 450,90 550,100 600,105" fill="none" stroke="#75c4b8" strokeWidth="1.5" strokeDasharray="6 3" opacity="0.4" />
                  <polyline points="0,260 60,255 150,230 250,180 350,140 450,150 550,155 600,158" fill="none" stroke="#d09c5a" strokeWidth="1.5" strokeDasharray="6 3" opacity="0.4" />
                </svg>
                <div className="osc-tooltip">
                  <div className="tooltip-header">DAY 15</div>
                  <div className="tooltip-val">-420K</div>
                  <div className="tooltip-unit">BBL/D</div>
                  <div className="tooltip-price">+$12.40/BBL</div>
                </div>
                <div className="sim-results-row">
                  <div className="sim-result panel">
                    <div className="result-label">TOTAL DEFICIT</div>
                    <div className="result-value text-teal">—</div>
                  </div>
                  <div className="sim-result panel">
                    <div className="result-label">PRICE CEILING</div>
                    <div className="result-value text-amber">—</div>
                  </div>
                  <div className="sim-result panel">
                    <div className="result-label">RECOVERY_EST</div>
                    <div className="result-value text-red">—</div>
                  </div>
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default Simulator;
