import React, { useState, useEffect, useRef } from 'react';
import { fetchLatestSignals } from '../services/api';
import './Intelligence.css';

const TABS = [
  { key: 'all', label: 'ALL SIGNALS' },
  { key: 'geopolitical', label: 'GEOPOLITICAL' },
  { key: 'maritime', label: 'MARITIME' },
  { key: 'sanctions', label: 'SANCTIONS' },
  { key: 'market', label: 'MARKET' },
];

interface SignalImpact {
  risk_delta: string;
  supply_impact: string;
  precedent: string;
}

interface SignalItem {
  id: string;
  timestamp: string;
  event_type: string;
  headline: string;
  corridor: string;
  confidence: string;
  classification: string[];
  body: string;
  impact: SignalImpact;
}

function severity(s: SignalItem): 'critical' | 'elevated' | 'routine' {
  if (s.classification.includes('critical')) return 'critical';
  if (s.classification.includes('escalated')) return 'elevated';
  return 'routine';
}

function signalAge(raw: string): string {
  const d = new Date(raw);
  if (isNaN(d.getTime())) return '0H';
  const diff = Date.now() - d.getTime();
  const hours = Math.floor(diff / 3600000);
  if (hours < 1) return '<1H';
  if (hours < 24) return `${hours}H`;
  return `${Math.floor(hours / 24)}D`;
}

function formatTimestamp(raw: string): string {
  const d = new Date(raw);
  if (isNaN(d.getTime())) return '--';
  return d.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', hour12: false }) + 'Z';
}

const Intelligence: React.FC = () => {
  const [activeTab, setActiveTab] = useState('all');
  const [signals, setSignals] = useState<SignalItem[]>([]);
  const [loading, setLoading] = useState(false);
  const [fadingIn, setFadingIn] = useState(false);
  const prevTab = useRef('all');

  useEffect(() => {
    const load = async () => {
      setLoading(true);
      setFadingIn(false);
      try {
        const data = await fetchLatestSignals(activeTab);
        await new Promise((r) => setTimeout(r, 200));
        const items: SignalItem[] = (data.signals ?? []).length > 0
          ? data.signals
          : getMockSignals(activeTab);
        setSignals(items);
      } catch {
        setSignals(getMockSignals(activeTab));
      } finally {
        setLoading(false);
        requestAnimationFrame(() => setFadingIn(true));
      }
    };
    prevTab.current = activeTab;
    load();
  }, [activeTab]);

  return (
    <div className="intel-page">
      <div className="intel-header-section">
        <div className="intel-header-left">
          <h2 className="intel-main-title">INTELLIGENCE TELEX</h2>
          <p className="intel-subtitle text-teal">SIGNAL INTERCEPT FEED // PRIORITY CHANNEL ALPHA</p>
        </div>
        <div className="intel-header-right">
          <div className="intel-meta">FEED STATUS: <span className="text-teal">ACTIVE</span></div>
          <div className="intel-meta">CLEARANCE: <span className="text-main">LEVEL 4</span></div>
          <div className="intel-timestamp">LAST SYNC: {new Date().toLocaleTimeString()}Z</div>
        </div>
      </div>

      <div className="intel-filter-bar">
        <div className="filter-tabs">
          {TABS.map((tab, i) => (
            <React.Fragment key={tab.key}>
              <button
                className={`filter-tab ${activeTab === tab.key ? 'active' : ''}`}
                onClick={() => setActiveTab(tab.key)}
              >
                {tab.label}
              </button>
              {i < TABS.length - 1 && <span className="tab-sep">|</span>}
            </React.Fragment>
          ))}
        </div>
        <div className="filter-right">
          <div className="signal-count">
            <span className="count-value text-amber">{signals.length}</span>
            <span className="count-label">ACTIVE SIGNALS</span>
          </div>
        </div>
      </div>

      <div className={`telex-feed ${fadingIn ? 'fade-in' : ''}`}>
        {loading ? (
          <div className="telex-loading">
            <span className="loading-dashes">━━━━</span>
            <span className="loading-text">FILTERING... {activeTab.toUpperCase()}</span>
            <span className="loading-dashes">━━━━</span>
          </div>
        ) : (
          signals.map((sig) => {
            const sev = severity(sig);
            return (
              <div key={sig.id} className={`telex-msg ${sev}`}>
                <div className={`telex-priority-bar ${sev}-bar`}></div>
                <div className="telex-timestamp-col">
                  <div className="telex-time">{formatTimestamp(sig.timestamp)}</div>
                  <div className="telex-age">{signalAge(sig.timestamp)}</div>
                  <div className={`telex-sev-tag ${sev}-tag`}>
                    {sev === 'critical' ? 'CRITICAL' : sev === 'elevated' ? 'ELEVATED' : 'ROUTINE'}
                  </div>
                </div>
                <div className="telex-body">
                  <h4 className="telex-headline">{sig.headline}</h4>
                  <div className="telex-classification">
                    {sig.classification.map((c) => (
                      <span key={c} className={`class-badge ${c}`}>{c.toUpperCase()}</span>
                    ))}
                    <span className="corridor-badge">{sig.corridor.toUpperCase()}</span>
                    <span className="conf-badge">CONFIDENCE: {sig.confidence.toUpperCase()}</span>
                  </div>
                  <p className="telex-content">{sig.body}</p>
                  <div className="telex-meta-row">
                    <div className="telex-metric">
                      <span className="tm-label">RISK DELTA</span>
                      <span className="tm-value text-amber">{sig.impact.risk_delta}</span>
                    </div>
                    <div className="telex-metric">
                      <span className="tm-label">IMPACT BASIS</span>
                      <span className="tm-value text-teal">{sig.impact.supply_impact}</span>
                    </div>
                    <div className="telex-metric">
                      <span className="tm-label">PRECEDENT</span>
                      <span className="tm-value text-muted">{sig.impact.precedent}</span>
                    </div>
                    <div className="telex-metric">
                      <span className="tm-label">DELAY</span>
                      <span className="tm-value text-muted">{signalAge(sig.timestamp)}</span>
                    </div>
                  </div>
                </div>
              </div>
            );
          })
        )}
      </div>
    </div>
  );
};

function getMockSignals(tab: string): SignalItem[] {
  const now = new Date();
  const all: Record<string, SignalItem[]> = {
    geopolitical: [
      { id: 'SIG-GEO-01', timestamp: now.toISOString(), event_type: 'sanctions', headline: 'HORMUZ STRAIT — KINETIC ACTIVITY DETECTED', corridor: 'hormuz', confidence: 'high', classification: ['critical'], body: 'Multiple fast-attack craft observed conducting interdiction maneuvers near 26.5°N, 56.2°E. Pattern consistent with IRGCN harassment operations.', impact: { risk_delta: '+18%', supply_impact: '340K BBL/DAY', precedent: '2022-YEM-ATK' } },
      { id: 'SIG-GEO-02', timestamp: new Date(now.getTime() - 3600000).toISOString(), event_type: 'embargo', headline: 'IRAN — ESCALATION RHETORIC AT UN ASSEMBLY', corridor: 'hormuz', confidence: 'medium', classification: ['escalated'], body: 'Iranian delegation warns of retaliatory action if oil exports are further restricted. Diplomatic channels indicate heightened tension.', impact: { risk_delta: '+8%', supply_impact: '180K BBL/DAY', precedent: '2023-UNSC-04' } },
    ],
    maritime: [
      { id: 'SIG-MAR-01', timestamp: now.toISOString(), event_type: 'route_blockade', headline: 'RED SEA — COMMERCIAL VESSEL COURSE DEVIATION', corridor: 'red_sea', confidence: 'high', classification: ['critical'], body: 'MARE ATLANTIS (IMO 9823456) forced course deviation near Bab al-Mandab. Houthi patrol activity reported in area.', impact: { risk_delta: '+22%', supply_impact: '290K BBL/DAY', precedent: '2023-RED-ATK' } },
      { id: 'SIG-MAR-02', timestamp: new Date(now.getTime() - 7200000).toISOString(), event_type: 'port_closure', headline: 'ARCTIC NSR — ICE FORMATION ADVANCED', corridor: 'rus-ind', confidence: 'medium', classification: [], body: 'Northern Sea Route ice coverage 12 days ahead of seasonal average. Transit window closing for COR-RUS-IND-01.', impact: { risk_delta: '+5%', supply_impact: '160K BBL/DAY', precedent: '2024-NSR-ICE' } },
    ],
    sanctions: [
      { id: 'SIG-SAN-01', timestamp: now.toISOString(), event_type: 'sanctions', headline: 'OFAC — 14 IRANIAN ENTITIES DESIGNATED', corridor: 'iran-india', confidence: 'high', classification: ['escalated'], body: 'US Treasury designates entities linked to Iranian petroleum exports. Includes 3 shipping companies. 90-day compliance window.', impact: { risk_delta: '+12%', supply_impact: '180K BBL/DAY', precedent: '2022-SANC-03' } },
      { id: 'SIG-SAN-02', timestamp: new Date(now.getTime() - 14400000).toISOString(), event_type: 'sanctions', headline: 'EU — RUSSIA SANCTIONS PACKAGE 14 APPROVED', corridor: 'rus-ind', confidence: 'high', classification: [], body: 'New measures targeting shadow fleet vessels transporting Russian crude above price cap. Estimated 8% supply impact.', impact: { risk_delta: '+6%', supply_impact: '110K BBL/DAY', precedent: '2023-EU-SANC' } },
    ],
    market: [
      { id: 'SIG-MKT-01', timestamp: now.toISOString(), event_type: 'price_spike', headline: 'BRENT CRUDE — INTRADAY VOLATILITY ALERT', corridor: 'global', confidence: 'medium', classification: ['escalated'], body: 'Brent futures (BZ=F) registered 3.2% intraday swing. Current spot: $84.22/BBL. Options implied volatility at 6-month high.', impact: { risk_delta: '+9%', supply_impact: '0 BBL/DAY', precedent: '2023-BRENT-SPIKE' } },
      { id: 'SIG-MKT-02', timestamp: new Date(now.getTime() - 10800000).toISOString(), event_type: 'opec_action', headline: 'OPEC+ — EMERGENCY MEETING CONSIDERED', corridor: 'global', confidence: 'low', classification: [], body: 'OPEC+ delegates consider emergency meeting to address potential supply disruption. Market awaiting official statement.', impact: { risk_delta: '+4%', supply_impact: '0 BBL/DAY', precedent: '2020-OPEC-EMERG' } },
    ],
    all: [
      { id: 'SIG-001', timestamp: now.toISOString(), event_type: 'sanctions', headline: 'HORMUZ STRAIT — KINETIC ACTIVITY DETECTED', corridor: 'hormuz', confidence: 'high', classification: ['critical'], body: 'Multiple fast-attack craft observed. Pattern consistent with IRGCN harassment. Commercial tanker forced course deviation.', impact: { risk_delta: '+18%', supply_impact: '340K BBL/DAY', precedent: '2022-YEM-ATK' } },
      { id: 'SIG-002', timestamp: new Date(now.getTime() - 3600000).toISOString(), event_type: 'sanctions', headline: 'OFAC — 14 IRANIAN ENTITIES DESIGNATED', corridor: 'iran-india', confidence: 'high', classification: ['escalated'], body: 'US Treasury designates entities linked to Iranian petroleum exports. 90-day compliance window for Indian refiners.', impact: { risk_delta: '+12%', supply_impact: '180K BBL/DAY', precedent: '2022-SANC-03' } },
      { id: 'SIG-003', timestamp: new Date(now.getTime() - 7200000).toISOString(), event_type: 'price_spike', headline: 'BRENT CRUDE — INTRADAY VOLATILITY ALERT', corridor: 'global', confidence: 'medium', classification: ['escalated'], body: 'Brent futures 3.2% intraday swing. Options implied volatility at 6-month high. Pattern correlation with Q4-2023 Red Sea disruption.', impact: { risk_delta: '+9%', supply_impact: '0 BBL/DAY', precedent: '2023-BRENT-SPIKE' } },
      { id: 'SIG-004', timestamp: new Date(now.getTime() - 14400000).toISOString(), event_type: 'port_closure', headline: 'ARCTIC NSR — SEASONAL ICE FORMATION', corridor: 'rus-ind', confidence: 'medium', classification: [], body: 'Northern Sea Route ice coverage advancing 12 days ahead of schedule. COR-RUS-IND-01 transit window closing.', impact: { risk_delta: '+5%', supply_impact: '160K BBL/DAY', precedent: '2024-NSR-ICE' } },
    ],
  };
  return all[tab] || all.all;
}

export default Intelligence;
