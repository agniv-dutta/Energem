import { useAppStore, type CorridorData } from '../store/useAppStore';
import './Modal.css';

interface Props {
  corridor: CorridorData;
}

export default function CorridorDetailsModal({ corridor }: Props) {
  const setSelectedCorridor = useAppStore((s) => s.setSelectedCorridor);

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
            <div className="detail-row">
              <span className="detail-label">PROBABILITY</span>
              <span className="detail-value text-amber">{corridor.probability}%</span>
            </div>
            <div className="detail-row">
              <span className="detail-label">DAILY FLOW</span>
              <span className="detail-value text-teal">{corridor.dailyFlow}</span>
            </div>
            <div className="detail-row">
              <span className="detail-label">CONFIDENCE</span>
              <span className="detail-value">{corridor.confidence}</span>
            </div>
            <div className="detail-row">
              <span className="detail-label">HISTORICAL BASELINE</span>
              <span className="detail-value">
                <button className="baseline-btn" onClick={() => alert('Historical data: 2022 Hormuz incident scored 78%')}>
                  Click to compare vs. 2022 Hormuz incident ({corridor.historicalBaseline}%)
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
