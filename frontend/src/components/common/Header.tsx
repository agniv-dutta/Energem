import React from 'react';
import { NavLink } from 'react-router-dom';
import { Settings, Bell } from 'lucide-react';
import './Header.css';

const Header: React.FC = () => {
  return (
    <header className="app-header">
      <div className="header-brand">
        <div className="logo-box">
          <div className="logo-inner-circle"></div>
        </div>
        <div className="brand-text">
          <h1>ENERGEM</h1>
          <p>NATIONAL ENERGY SUPPLY INTELLIGENCE</p>
        </div>
      </div>
      
      <nav className="header-nav">
        <NavLink to="/overview" className={({ isActive }) => isActive ? 'nav-tab active' : 'nav-tab'}>OVERVIEW</NavLink>
        <NavLink to="/map" className={({ isActive }) => isActive ? 'nav-tab active' : 'nav-tab'}>CORRIDOR MAP</NavLink>
        <NavLink to="/simulator" className={({ isActive }) => isActive ? 'nav-tab active' : 'nav-tab'}>SIMULATOR</NavLink>
        <NavLink to="/procurement" className={({ isActive }) => isActive ? 'nav-tab active' : 'nav-tab'}>PROCUREMENT</NavLink>
        <NavLink to="/intelligence" className={({ isActive }) => isActive ? 'nav-tab active' : 'nav-tab'}>INTELLIGENCE</NavLink>
      </nav>
      
      <div className="header-actions">
        <button className="icon-btn"><Settings size={20} /></button>
        <button className="icon-btn"><Bell size={20} /></button>
        <div className="time-display">0905Z</div>
      </div>
    </header>
  );
};

export default Header;
