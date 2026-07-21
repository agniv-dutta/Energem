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

  const timelineDays = simulationResult?.timeline ?? [];

  return (
    <div className="simulator-page">
      <div className="sim-body">
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
                <div className="timeline-grid">
                  {timelineDays.map((t) => (
                    <div key={t.day} className="timeline-day-col">
                      <div className="timeline-day-label">DAY {String(t.day).padStart(2, '0')}</div>

                      <div className="timeline-metric">
                        <div className="metric-val text-red">-{t.supply_loss_bbl.toLocaleString()}</div>
                        <div className="metric-unit">BBL/D</div>
                      </div>

                      <div className="timeline-metric">
                        <div className="metric-val text-amber">${t.brent_price}/BBL</div>
                        <div className="metric-trend">({t.brent_price > 90 ? '+' : ''}{((t.brent_price - 90) / 90 * 100).toFixed(0)}%)</div>
                      </div>

                      <div className="timeline-metric">
                        <div className="metric-val text-teal">SPR: {t.spr_remaining_days}d</div>
                        <div className="metric-trend">({t.spr_remaining_days < 9.3 ? '' : '+'}{(t.spr_remaining_days - 9.3).toFixed(1)}d)</div>
                      </div>
                    </div>
                  ))}
                </div>

                <div className="timeline-divider"></div>

                <div className="timeline-summary-row">
                  <div className="summary-item">
                    <span className="summary-label">TOTAL DEFICIT</span>
                    <span className="summary-val text-red">{simulationResult.summary.total_deficit_display}</span>
                  </div>
                  <div className="summary-item">
                    <span className="summary-label">PRICE CEILING</span>
                    <span className="summary-val text-amber">{simulationResult.summary.peak_price_display}</span>
                  </div>
                  <div className="summary-item">
                    <span className="summary-label">SPR CRITICAL DAY</span>
                    <span className="summary-val text-teal">{simulationResult.summary.spr_critical_day}</span>
                  </div>
                  <div className="summary-item">
                    <span className="summary-label">RECOVERY ESTIMATE</span>
                    <span className="summary-val text-main">{simulationResult.summary.recovery_estimate}</span>
                  </div>
                </div>

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
              <>
                <div className="timeline-grid placeholder-grid">
                  {['01', '05', '10', '30'].map((day) => (
                    <div key={day} className="timeline-day-col placeholder-col">
                      <div className="timeline-day-label">DAY {day}</div>
                      <div className="timeline-metric">
                        <div className="metric-val text-muted">—</div>
                        <div className="metric-unit">BBL/D</div>
                      </div>
                      <div className="timeline-metric">
                        <div className="metric-val text-muted">—</div>
                        <div className="metric-unit">$/BBL</div>
                      </div>
                      <div className="timeline-metric">
                        <div className="metric-val text-muted">SPR: —</div>
                        <div className="metric-unit">REMAINING</div>
                      </div>
                    </div>
                  ))}
                </div>

                <div className="timeline-divider"></div>

                <div className="timeline-summary-row">
                  <div className="summary-item">
                    <span className="summary-label">TOTAL DEFICIT</span>
                    <span className="summary-val text-muted">—</span>
                  </div>
                  <div className="summary-item">
                    <span className="summary-label">PRICE CEILING</span>
                    <span className="summary-val text-muted">—</span>
                  </div>
                  <div className="summary-item">
                    <span className="summary-label">SPR CRITICAL DAY</span>
                    <span className="summary-val text-muted">—</span>
                  </div>
                  <div className="summary-item">
                    <span className="summary-label">RECOVERY ESTIMATE</span>
                    <span className="summary-val text-muted">—</span>
                  </div>
                </div>
              </>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default Simulator;
