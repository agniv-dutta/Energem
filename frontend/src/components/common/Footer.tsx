import React from 'react';
import './Footer.css';

const Footer: React.FC = () => {
  return (
    <footer className="app-footer">
      <div className="footer-left">
        <span className="status-label">SYSTEM STATUS:</span> <span className="status-value">NOMINAL</span>
        <span className="separator">//</span>
        <span className="status-label">DATA LATENCY:</span> <span className="status-value">40MS</span>
      </div>
      <div className="footer-right">
        <span className="footer-link">LOGISTICS</span>
        <span className="separator">/</span>
        <span className="footer-link">TERMINALS</span>
        <span className="separator">/</span>
        <span className="footer-link">REFINERY STATS</span>
      </div>
    </footer>
  );
};

export default Footer;
