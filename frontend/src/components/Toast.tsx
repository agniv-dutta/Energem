import { useEffect } from 'react';
import { useAppStore } from '../store/useAppStore';
import './Toast.css';

export default function Toast() {
  const toast = useAppStore((s) => s.toast);
  const clearToast = useAppStore((s) => s.clearToast);

  useEffect(() => {
    if (toast) {
      const t = setTimeout(clearToast, 4000);
      return () => clearTimeout(t);
    }
  }, [toast, clearToast]);

  if (!toast) return null;

  return (
    <div className={`toast-overlay ${toast.type}`}>
      <div className="toast-content">
        <span className="toast-icon">{toast.type === 'success' ? '✓' : '✗'}</span>
        <span className="toast-message">{toast.message}</span>
      </div>
    </div>
  );
}
