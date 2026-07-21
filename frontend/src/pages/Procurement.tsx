import React, { useEffect, useMemo, useState, useCallback } from 'react';
import './Procurement.css';
import { authorizeRecommendations, exportProcurementPresentation, fetchProcurementRecommendations } from '../services/api';

type ProcurementStatus = 'generated' | 'pending_approval' | 'approved' | 'pending_execution' | 'executed' | 'rejected';

type ProcurementRecommendation = {
  id: string;
  scenario_id: string;
  priority: string;
  supplier: string;
  volume_bbl_per_day: number;
  eta_days: number;
  cost_premium_per_barrel: number;
  geopolitical_risk: 'low' | 'medium' | 'high';
  confidence: number;
  reasoning: string;
  status: ProcurementStatus;
  approved_by?: string | null;
  approved_at?: string | null;
  status_detail: string;
};

type ProcurementResponse = {
  scenario_id: string;
  authority_level: string;
  recommendations: ProcurementRecommendation[];
  execution_readiness: {
    total_approved_volume: number;
    can_execute_all: boolean;
    blockers: string[];
  };
};

const statusLabels: Record<ProcurementStatus, string> = {
  generated: 'GENERATED',
  pending_approval: 'PENDING APPROVAL',
  approved: 'APPROVED',
  pending_execution: 'PENDING EXECUTION',
  executed: 'EXECUTED',
  rejected: 'REJECTED',
};

const Procurement: React.FC = () => {
  const [data, setData] = useState<ProcurementResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [lastUpdated, setLastUpdated] = useState<string>('--:--:--Z');

  const load = useCallback(async () => {
    try {
      setLoading(true);
      setError(null);
      const response = (await fetchProcurementRecommendations()) as ProcurementResponse;
      setData(response);
      setLastUpdated(new Date().toISOString().replace(/\.\d{3}Z$/, 'Z'));
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load procurement recommendations');
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    void load();
  }, [load]);

  const allIds = useMemo(
    () => data?.recommendations.filter((item) => item.status === 'pending_approval' || item.status === 'generated').map((item) => item.id) ?? [],
    [data],
  );

  const handleAuthorizeAll = async () => {
    if (!allIds.length) return;

    try {
      setSubmitting(true);
      setError(null);
      const response = await authorizeRecommendations({
        recommendation_ids: allIds,
        authorized_by: 'directorate_b_console',
        authorization_level: 'directorate_b',
        reason: 'Supply disruption - authorized via dashboard',
      });

      const approvedItems: Array<{ id: string; status: string; approved_at?: string }> = response.recommendations ?? [];
      const approvedMap = new Map(approvedItems.map((item) => [item.id, item]));
      setData((current) => {
        if (!current) return current;
        return {
          ...current,
          recommendations: current.recommendations.map((item) => {
            const approved = approvedMap.get(item.id);
            if (!approved) return item;
            return {
              ...item,
              status: approved.status as ProcurementStatus,
              approved_at: approved.approved_at ?? item.approved_at,
              status_detail: 'Approved by directorate_b_console',
            };
          }),
          execution_readiness: {
            ...current.execution_readiness,
            total_approved_volume: response.total_volume_bbl,
            can_execute_all: true,
            blockers: [],
          },
        };
      });
      setLastUpdated(new Date().toISOString().replace(/\.\d{3}Z$/, 'Z'));
    } catch (err) {
      const message = err instanceof Error ? err.message : 'Authorization failed';
      setError(message);
    } finally {
      setSubmitting(false);
    }
  };

  const handleExportPresentation = async () => {
    try {
      const response = await exportProcurementPresentation();
      const blob = response.data;
      const url = window.URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', `energem_procurement_${new Date().toISOString().split('T')[0]}.pptx`);
      document.body.appendChild(link);
      link.click();
      link.parentElement?.removeChild(link);
      window.URL.revokeObjectURL(url);
    } catch {
      alert('Failed to export procurement report');
    }
  };

  const totalVolume = data?.recommendations.reduce((sum, item) => sum + item.volume_bbl_per_day, 0) ?? 0;
  const totalCost = data?.recommendations.reduce((sum, item) => sum + item.volume_bbl_per_day * item.cost_premium_per_barrel, 0) ?? 0;

  return (
    <div className="procurement-page">
      <div className="proc-header-section">
        <div className="proc-header-left">
          <h2 className="proc-main-title">PROCUREMENT<br />RECOMMENDATIONS</h2>
          <p className="proc-subtitle text-teal">STRATEGIC ACQUISITION MANIFEST // SECTOR 7G-12</p>
        </div>
        <div className="proc-header-right">
          <div className="proc-meta-line">LAST UPDATED: {lastUpdated}</div>
          <div className="proc-authority">AUTHORITY LEVEL:</div>
          <div className="proc-authority-value">{data?.authority_level?.toUpperCase() ?? 'OMEGA'}</div>
        </div>
      </div>

      <div className="proc-summary-row panel">
        <div className="proc-summary-item">
          <span className="proc-summary-label">SCENARIO</span>
          <span className="proc-summary-value">{data?.scenario_id ?? '--'}</span>
        </div>
        <div className="proc-summary-item">
          <span className="proc-summary-label">TOTAL VOLUME</span>
          <span className="proc-summary-value text-teal">{totalVolume.toLocaleString()} BBL/DAY</span>
        </div>
        <div className="proc-summary-item">
          <span className="proc-summary-label">EST. COST PREMIUM</span>
          <span className="proc-summary-value text-amber">${Math.round(totalCost).toLocaleString()}</span>
        </div>
        <div className="proc-summary-item">
          <span className="proc-summary-label">READY TO EXECUTE</span>
          <span className={`proc-summary-value ${data?.execution_readiness.can_execute_all ? 'text-teal' : 'text-amber'}`}>
            {data?.execution_readiness.can_execute_all ? 'YES' : 'NO'}
          </span>
        </div>
      </div>

      {error ? <div className="proc-error panel">{error}</div> : null}

      <div className="proc-cards">
        {(loading ? Array.from({ length: 3 }) : (data?.recommendations ?? [])).map((item: unknown, index: number) => {
          const recommendation = loading ? null : (item as ProcurementRecommendation);
          const status = recommendation?.status ?? 'generated';
          const confidenceBars = recommendation ? Math.max(1, Math.min(10, Math.round(recommendation.confidence / 10))) : 0;

          return (
            <div className={`proc-card panel ${status === 'rejected' ? 'locked' : ''}`} key={loading ? `skeleton-${index}` : recommendation!.id}>
              <div className={`proc-card-accent ${status === 'approved' ? 'approved-accent' : status === 'pending_approval' ? 'pending-accent' : 'locked-accent'}`}></div>
              <div className="proc-card-number">{String(index + 1).padStart(2, '0')}</div>
              <div className="proc-card-body">
                <h3 className={`proc-card-title ${status === 'rejected' ? 'dimmed' : ''}`}>
                  {loading ? 'LOADING RECOMMENDATION...' : `PRIORITY ${recommendation!.priority} — ${recommendation!.supplier.toUpperCase()}`}
                </h3>
                <div className="proc-card-metrics">
                  <div className="proc-metric">
                    <div className="proc-metric-label">VOLUME</div>
                    <div className="proc-metric-value text-teal">{loading ? '--' : `${recommendation?.volume_bbl_per_day.toLocaleString()} BBL/DAY`}</div>
                  </div>
                  <div className="proc-metric">
                    <div className="proc-metric-label">EST. ARRIVAL</div>
                    <div className="proc-metric-value text-teal">{loading ? '--' : `${recommendation?.eta_days} DAYS`}</div>
                  </div>
                  <div className="proc-metric">
                    <div className="proc-metric-label">RISK</div>
                    <div className={`proc-metric-value ${recommendation?.geopolitical_risk === 'high' ? 'text-red' : recommendation?.geopolitical_risk === 'medium' ? 'text-amber' : 'text-teal'}`}>
                      {loading ? '--' : recommendation?.geopolitical_risk.toUpperCase()}
                    </div>
                  </div>
                  <div className="proc-metric">
                    <div className="proc-metric-label">COST PREMIUM</div>
                    <div className="proc-metric-value text-teal">{loading ? '--' : `$${recommendation?.cost_premium_per_barrel.toFixed(2)}`}</div>
                  </div>
                </div>
                <div className="proc-card-footer">
                  <div className={`proc-badge ${status}`}>{statusLabels[status]}</div>
                  <span className="proc-footer-text">{loading ? 'Synchronizing procurement manifest...' : recommendation?.status_detail}</span>
                </div>
              </div>
              <div className="proc-card-confidence">
                <div className="confidence-label">CONFIDENCE METRIC</div>
                <div className="confidence-bars">
                  {Array.from({ length: 10 }).map((_, barIndex) => (
                    <div
                      key={barIndex}
                      className={`conf-bar ${loading ? '' : barIndex < confidenceBars ? 'filled' : ''} ${loading ? '' : barIndex >= 8 && barIndex < confidenceBars ? 'dark' : ''}`}
                    ></div>
                  ))}
                </div>
                <div className="confidence-footer">
                  <span>{loading ? '--' : `${recommendation?.confidence}% PROB`}</span>
                  <span>{loading ? '--' : recommendation?.status === 'approved' ? 'AUTHORIZED' : 'PENDING'}</span>
                </div>
              </div>
            </div>
          );
        })}
      </div>

      <div className="proc-readiness panel">
        <div>
          <div className="proc-readiness-label">EXECUTION READINESS</div>
          <div className="proc-readiness-value">{data?.execution_readiness.blockers.length ? 'BLOCKED' : 'CLEAR'}</div>
        </div>
        <div className="proc-readiness-blockers">
          {data?.execution_readiness.blockers.length ? data.execution_readiness.blockers.join(' • ') : 'All selected recommendations are ready for approval flow.'}
        </div>
      </div>

      <div className="proc-authorize-section">
        <button className="authorize-btn" onClick={handleAuthorizeAll} disabled={loading || submitting || allIds.length === 0}>
          {submitting ? 'AUTHORIZING...' : 'AUTHORIZE ALL PRIMARY RECOMMENDATIONS'}
        </button>
        <button className="export-btn" onClick={handleExportPresentation} disabled={loading}>
          EXPORT AS PPTX
        </button>
      </div>
    </div>
  );
};

export default Procurement;
