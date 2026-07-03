import React from 'react';
import Header from './Header';
import Navigation from './Navigation';
import Footer from './Footer';
import './Layout.css';

interface LayoutProps {
  children: React.ReactNode;
}

const Layout: React.FC<LayoutProps> = ({ children }) => {
  return (
    <div className="app-container">
      <div className="main-wrapper">
        <Navigation />
        <div className="main-content">
          <Header />
          <main className="content-area">
            {children}
          </main>
        </div>
      </div>
      <Footer />
    </div>
  );
};

export default Layout;
