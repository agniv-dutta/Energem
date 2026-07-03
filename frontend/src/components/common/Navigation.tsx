import React from 'react';
import { NavLink } from 'react-router-dom';
import { Compass, Map, Activity, ShoppingCart, Cpu } from 'lucide-react';
import './Navigation.css';

const Navigation: React.FC = () => {
  return (
    <aside className="app-sidebar">
      <div className="sidebar-top">
        <div className="bearing-widget">
          <div className="bearing-visual">
            <div className="bearing-line"></div>
          </div>
          <div className="bearing-text">BEARING 000°</div>
          <div className="sector-info">
            <div className="sector-title">SECTOR: LOGISTICS</div>
            <div className="sector-ref">REF: EN-240-ALPHA</div>
          </div>
        </div>
      </div>
      
      <nav className="sidebar-nav">
        <NavLink to="/overview" className={({ isActive }) => isActive ? 'side-tab active' : 'side-tab'}>
          <Compass size={18} />
          <span>OVERVIEW</span>
        </NavLink>
        <NavLink to="/map" className={({ isActive }) => isActive ? 'side-tab active' : 'side-tab'}>
          <Map size={18} />
          <span>CORRIDOR MAP</span>
        </NavLink>
        <NavLink to="/simulator" className={({ isActive }) => isActive ? 'side-tab active' : 'side-tab'}>
          <Activity size={18} />
          <span>SIMULATOR</span>
        </NavLink>
        <NavLink to="/procurement" className={({ isActive }) => isActive ? 'side-tab active' : 'side-tab'}>
          <ShoppingCart size={18} />
          <span>PROCUREMENT</span>
        </NavLink>
        <NavLink to="/intelligence" className={({ isActive }) => isActive ? 'side-tab active' : 'side-tab'}>
          <Cpu size={18} />
          <span>INTELLIGENCE</span>
        </NavLink>
      </nav>
      
      <div className="sidebar-bottom">
        <div className="status-widget">
          <div className="status-indicator nominal"></div>
          <div className="status-text">
            <div>SYSTEM STATUS: NOMINAL</div>
            <div>DATA LATENCY: 40MS</div>
          </div>
        </div>
      </div>
    </aside>
  );
};

export default Navigation;
