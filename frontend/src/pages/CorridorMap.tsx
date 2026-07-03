import React from 'react';
import './CorridorMap.css';

const CorridorMap: React.FC = () => {
  return (
    <div className="corridor-page">
      {/* Scrolling Ticker */}
      <div className="ticker-bar">
        <div className="ticker-content">
          <span>SYSTEM STATUS: NOMINAL</span>
          <span className="ticker-sep">//</span>
          <span>DATA LATENCY: 40MS</span>
          <span className="ticker-sep">//</span>
          <span className="text-amber">HORMUZ THREAT LEVEL: ELEVATED</span>
          <span className="ticker-sep">//</span>
          <span>SUEZ THROUGHPUT: -12%</span>
          <span className="ticker-sep">//</span>
          <span>CRUDE SPOT: 84.22 USD</span>
          <span className="ticker-sep">//</span>
          <span>GLOBAL FLOW RATE: 78.4M BBL/DAY</span>
          <span className="ticker-sep">//</span>
          <span>SYSTEM STATUS: NOMINAL</span>
          <span className="ticker-sep">//</span>
          <span>DATA LATENCY: 40MS</span>
          <span className="ticker-sep">//</span>
          <span className="text-amber">HORMUZ THREAT LEVEL: ELEVATED</span>
          <span className="ticker-sep">//</span>
          <span>SUEZ THROUGHPUT: -12%</span>
          <span className="ticker-sep">//</span>
          <span>CRUDE SPOT: 84.22 USD</span>
          <span className="ticker-sep">//</span>
          <span>GLOBAL FLOW RATE: 78.4M BBL/DAY</span>
        </div>
      </div>

      {/* Title Section */}
      <div className="corridor-title-section">
        <div className="corridor-title-left">
          <h2 className="corridor-title">SUPPLY CORRIDOR ALPHA-7</h2>
          <p className="corridor-subtitle">P&amp;ID SCHEMATIC // REAL-TIME TRANSIT VECTORING</p>
        </div>
        <div className="corridor-title-right">
          <div className="latency-badge text-red">LATENCY: 40MS</div>
          <div className="timestamp">2023-10-27 14:42:01 ZULU</div>
        </div>
      </div>

      {/* Map Schematic Area */}
      <div className="map-schematic panel">
        <svg viewBox="0 0 900 420" className="schematic-svg" xmlns="http://www.w3.org/2000/svg">
          {/* Russia Node */}
          <rect x="60" y="80" width="60" height="30" fill="#2a2a2a" stroke="#555" strokeWidth="1"/>
          <text x="90" y="115" fill="#888" fontSize="10" textAnchor="middle" fontFamily="'Share Tech Mono', monospace">RUSSIA</text>

          {/* Dotted teal line from Russia going right and down */}
          <line x1="120" y1="95" x2="300" y2="95" stroke="#75c4b8" strokeWidth="1" strokeDasharray="4 4" opacity="0.7"/>
          <line x1="300" y1="95" x2="420" y2="200" stroke="#75c4b8" strokeWidth="1" strokeDasharray="4 4" opacity="0.7"/>
          <line x1="420" y1="200" x2="420" y2="260" stroke="#75c4b8" strokeWidth="1" strokeDasharray="4 4" opacity="0.7"/>

          {/* Red dashed lines - horizontal routes */}
          <line x1="0" y1="230" x2="380" y2="230" stroke="#d85252" strokeWidth="1.5" strokeDasharray="6 4" opacity="0.8"/>
          <line x1="520" y1="230" x2="900" y2="230" stroke="#d85252" strokeWidth="1.5" strokeDasharray="6 4" opacity="0.8"/>

          {/* Second red dashed line lower */}
          <line x1="0" y1="340" x2="350" y2="340" stroke="#d85252" strokeWidth="1.5" strokeDasharray="6 4" opacity="0.5"/>

          {/* Diagonal connector line */}
          <line x1="420" y1="290" x2="350" y2="340" stroke="#75c4b8" strokeWidth="1" strokeDasharray="4 4" opacity="0.5"/>

          {/* Chokepoint Popup Box */}
          <rect x="380" y="220" width="180" height="80" fill="#1a1a1a" stroke="#555" strokeWidth="1"/>
          
          {/* Popup header */}
          <text x="395" y="242" fill="#e0e0e0" fontSize="10" fontFamily="'Share Tech Mono', monospace" letterSpacing="1">CHOKEPOINT: HORMUZ</text>
          <polygon points="565,228 572,234 565,240" fill="#d09c5a"/>
          
          {/* Divider */}
          <line x1="390" y1="250" x2="550" y2="250" stroke="#333" strokeWidth="0.5"/>
          
          {/* Risk Index */}
          <text x="395" y="268" fill="#888" fontSize="9" fontFamily="'Share Tech Mono', monospace">RISK INDEX</text>
          <text x="540" y="268" fill="#d85252" fontSize="11" fontFamily="'Share Tech Mono', monospace" textAnchor="end" fontWeight="bold">84%</text>
          
          {/* Throughput */}
          <text x="395" y="286" fill="#888" fontSize="9" fontFamily="'Share Tech Mono', monospace">THROUGHPUT</text>
          <text x="540" y="286" fill="#75c4b8" fontSize="11" fontFamily="'Share Tech Mono', monospace" textAnchor="end" fontWeight="bold">1.5M BBL</text>
          
          {/* Red bar under throughput */}
          <rect x="395" y="292" width="145" height="3" fill="#d85252"/>
        </svg>

        {/* Legend */}
        <div className="map-legend panel">
          <div className="legend-item">
            <div className="legend-swatch" style={{backgroundColor: '#75c4b8'}}></div>
            <span>OPTIMAL FLOW</span>
          </div>
          <div className="legend-item">
            <div className="legend-swatch" style={{backgroundColor: '#d09c5a'}}></div>
            <span>THROTTLED / RISK</span>
          </div>
          <div className="legend-item">
            <div className="legend-swatch" style={{backgroundColor: '#d85252'}}></div>
            <span>CRITICAL BLOCKADE</span>
          </div>
        </div>
      </div>

      {/* Globe Overview Label */}
      <div className="globe-section">
        <div className="globe-label">GGN° OVERVIEW</div>
      </div>

      {/* Risk Manifest Log Table */}
      <div className="manifest-section">
        <div className="manifest-header">
          <span className="manifest-title">RISK MANIFEST LOG // SEGMENT DATA</span>
          <span className="auto-refresh">AUTO-REFRESH: 5S</span>
        </div>
        <table className="manifest-table">
          <thead>
            <tr>
              <th>CORRIDOR ID</th>
              <th>THREAT VECTOR</th>
              <th>RISK SCORE</th>
              <th>HEATMAP</th>
              <th>ACTION</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td>COR-RUS-IND-01</td>
              <td className="text-teal">ARCTIC ROUTE DELTA</td>
              <td>14.2%</td>
              <td>
                <div className="heatmap-bar">
                  <div className="heatmap-fill heatmap-low" style={{width: '14%'}}></div>
                </div>
              </td>
              <td><button className="table-btn">DETAILS</button></td>
            </tr>
            <tr>
              <td>COR-IRQ-IND-04</td>
              <td className="text-amber">HORMUZ STRAIT X</td>
              <td>84.0%</td>
              <td>
                <div className="heatmap-bar">
                  <div className="heatmap-fill heatmap-high" style={{width: '84%'}}></div>
                </div>
              </td>
              <td><button className="table-btn table-btn-danger">REROUTE</button></td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default CorridorMap;
