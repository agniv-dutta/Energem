import { useAppStore, type CorridorData } from '../store/useAppStore';
import './Modal.css';

interface Props {
  corridor: CorridorData;
}

export default function CorridorDetailsModal({ corridor }: Props) {
  const setSelectedCorridor = useAppStore((s) => s.setSelectedCorridor);

  const lastSignalTime = corridor.lastSignal
    ? new Date(corridor.lastSignal).toISOString().replace('T', ' ').slice(0, 19) + ' ZULU'
    : 'No recent signals';

  return (
    <div className="modal-backdrop" onClick={() => setSelectedCorridor(null)}>
      <div className="modal-panel" onClick={(e) => e.stopPropagation()}>
        <div className="modal-header">
          <h3>CORRIDOR DETAILS // {corridor.name.toUpperCase()}</h3>
          <button className="modal-close" onClick={() => setSelectedCorridor(null)}>✕</button>
        </div>
        <div className="modal-body">
          <div className="detail-grid">
            <div className="detail-row">
              <span className="detail-label">CORRIDOR</span>
              <span className="detail-value">{corridor.name}</span>
            </div>
            <div className="detail-row">
              <span className="detail-label">RISK SCORE</span>
              <span className="detail-value text-red">{corridor.riskScore}%</span>
            </div>
            {corridor.trend && (
              <div className="detail-row">
                <span className="detail-label">TREND</span>
                <span className="detail-value" style={{ color: corridor.trend.startsWith('+') ? '#d85252' : corridor.trend.startsWith('-') ? '#75c4b8' : '#888' }}>
                  {corridor.trend}
                </span>
              </div>
            )}
            <div className="detail-row">
              <span className="detail-label">DAILY FLOW</span>
              <span className="detail-value text-teal">{corridor.dailyFlow}</span>
            </div>
            <div className="detail-row">
              <span className="detail-label">CONFIDENCE</span>
              <span className="detail-value">{corridor.confidence}</span>
            </div>
            {corridor.activeThreats !== undefined && (
              <div className="detail-row">
                <span className="detail-label">ACTIVE THREATS</span>
                <span className="detail-value" style={{ color: corridor.activeThreats > 0 ? '#d85252' : '#75c4b8' }}>
                  {corridor.activeThreats}
                </span>
              </div>
            )}
            <div className="detail-row">
              <span className="detail-label">LAST SIGNAL</span>
              <span className="detail-value" style={{ fontSize: 10 }}>{lastSignalTime}</span>
            </div>
            <div className="detail-row">
              <span className="detail-label">HISTORICAL BASELINE</span>
              <span className="detail-value">
                <button className="baseline-btn" onClick={() => alert(`Historical comparison: Current ${corridor.riskScore}% vs baseline ${corridor.historicalBaseline}%`)}>
                  Click to compare vs. baseline ({corridor.historicalBaseline}%)
                </button>
              </span>
            </div>
          </div>
        </div>
        <div className="modal-footer">
          <button className="btn-amber-full" onClick={() => setSelectedCorridor(null)}>ACKNOWLEDGE</button>
        </div>
      </div>
    </div>
  );
}
