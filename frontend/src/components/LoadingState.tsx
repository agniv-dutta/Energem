import React from 'react';

interface LoadingStateProps {
  message?: string;
  className?: string;
}

const LoadingState: React.FC<LoadingStateProps> = ({ message = 'LOADING...', className = '' }) => {
  return (
    <div className={`loading-state ${className}`}>
      <div className="loading-bar"></div>
      <span>{message}</span>
    </div>
  );
};

export default LoadingState;
