import { useAppStore, type CorridorData } from '../store/useAppStore';
import './Modal.css';

interface Props {
  corridor: CorridorData;
}

export default function RerouteModal({ corridor }: Props) {
  const setSelectedCorridor = useAppStore((s) => s.setSelectedCorridor);

  return (
    <div className="modal-backdrop" onClick={() => setSelectedCorridor(null)}>
      <div className="modal-panel" onClick={(e) => e.stopPropagation()}>
        <div className="modal-header">
          <h3>REROUTE ANALYSIS // {corridor.name.toUpperCase()}</h3>
          <button className="modal-close" onClick={() => setSelectedCorridor(null)}>✕</button>
        </div>
        <div className="modal-body">
          <div className="detail-grid">
            <div className="detail-row">
              <span className="detail-label">CURRENT ROUTE</span>
              <span className="detail-value">{corridor.name} Strait (distance 2,400 nm)</span>
            </div>
          </div>

          <h4 className="mt-4 text-amber">ALTERNATIVE ROUTES</h4>
          <div className="alt-route">
            <div className="alt-route-name">ALTERNATIVE 1: Malacca Strait</div>
            <div className="alt-route-detail">Distance: 3,100 nm &nbsp;|&nbsp; +5 days transit &nbsp;|&nbsp; <span className="text-teal">VIABLE</span></div>
          </div>
          <div className="alt-route">
            <div className="alt-route-name">ALTERNATIVE 2: Suez Canal</div>
            <div className="alt-route-detail">Distance: 4,800 nm &nbsp;|&nbsp; +8 days transit &nbsp;|&nbsp; <span className="text-amber">MODERATE RISK</span></div>
          </div>

          <h4 className="mt-4 text-amber">COST IMPACT</h4>
          <div className="detail-row">
            <span className="detail-label">INSURANCE PREMIUM</span>
            <span className="detail-value text-red">Red Sea route +$1.50/barrel</span>
          </div>
          <div className="detail-row">
            <span className="detail-label">RECOMMENDATION</span>
            <span className="detail-value text-amber">Reroute only if Hormuz risk exceeds 80%</span>
          </div>
        </div>
        <div className="modal-footer">
          <button className="btn-amber-full" onClick={() => setSelectedCorridor(null)}>ACKNOWLEDGE</button>
        </div>
      </div>
    </div>
  );
}
