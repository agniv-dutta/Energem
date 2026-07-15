import React, { useEffect, useState } from 'react';
import { X } from 'lucide-react';
import { fetchHistoricalComparison, type HistoricalComparisonResponse } from '../services/api';
import '../components/HistoricalComparisonModal.css';

interface Props {
  signalId: string;
  isOpen: boolean;
  onClose: () => void;
}

const HistoricalComparisonModal: React.FC<Props> = ({ signalId, isOpen, onClose }) => {
  const [data, setData] = useState<HistoricalComparisonResponse | null>(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (!isOpen || !signalId) return;
    setLoading(true);
    fetchHistoricalComparison(signalId)
      .then((resp) => { setData(resp); setLoading(false); })
      .catch(() => setLoading(false));
  }, [signalId, isOpen]);

  if (!isOpen) return null;

  const getSimilarityColor = (score: number) => {
    if (score >= 70) return 'critical';
    if (score >= 40) return 'elevated';
    return 'routine';
  };

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-content" onClick={(e) => e.stopPropagation()}>
        <div className="modal-header">
          <h2 className="modal-title">HISTORICAL PRECEDENT ANALYSIS</h2>
          <button className="modal-close" onClick={onClose}><X size={18} /></button>
        </div>

        <div className="modal-body">
          {loading ? (
            <div className="modal-loading">LOADING COMPARISON DATA...</div>
          ) : data ? (
            <div className="comparison-content">
              <div className="signal-summary">
                <h4>CURRENT SIGNAL</h4>
                <p>{data.current_signal.summary}</p>
                <div className="signal-meta">
                  <span>Corridor: {data.current_signal.corridor}</span>
                  <span>Probability: {data.current_signal.probability}%</span>
                  {data.current_signal.estimated_duration && (
                    <span>Est. Duration: {data.current_signal.estimated_duration} days</span>
                  )}
                </div>
              </div>

              <div className="recommendation">
                <h4>RECOMMENDATION</h4>
                <p>{data.recommendation}</p>
              </div>

              <div className="comparison-list">
                <h4>HISTORICAL COMPARISONS ({data.historical_comparisons.length})</h4>
                {data.historical_comparisons.map((item, idx) => (
                  <div key={idx} className="comparison-card">
                    <div className="card-header">
                      <span className="card-title">{item.historical_event}</span>
                      <span className={`card-score ${getSimilarityColor(item.similarity_score)}`}>
                        {item.similarity_score}% MATCH
                      </span>
                    </div>
                    <div className="card-date">{item.date} ({item.years_ago} years ago)</div>
                    <div className="card-metrics">
                      <div className="metric">
                        <span className="metric-label">HISTORICAL DURATION</span>
                        <span className="metric-value">{item.comparison.historical_event.actual_duration} days</span>
                      </div>
                      <div className="metric">
                        <span className="metric-label">SUPPLY LOSS</span>
                        <span className="metric-value">{item.comparison.historical_event.actual_supply_loss}%</span>
                      </div>
                      <div className="metric">
                        <span className="metric-label">SEVERITY DIFF</span>
                        <span className="metric-value">{item.comparison.delta.severity_diff > 0 ? '+' : ''}{item.comparison.delta.severity_diff}%</span>
                      </div>
                    </div>
                    <div className="card-lessons">
                      <span className="lessons-label">LESSONS:</span>
                      <span className="lessons-text">{item.lessons_learned}</span>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          ) : (
            <div className="modal-empty">No historical comparison available for this signal.</div>
          )}
        </div>
      </div>
    </div>
  );
};

export default HistoricalComparisonModal;
