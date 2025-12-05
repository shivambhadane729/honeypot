import React, { useState, useEffect } from 'react';
import { api } from '../api';

function ConnectionStatus() {
  const [isConnected, setIsConnected] = useState(false);
  const [checking, setChecking] = useState(true);

  useEffect(() => {
    checkConnection();
    const interval = setInterval(checkConnection, 10000); // Check every 10 seconds
    return () => clearInterval(interval);
  }, []);

  const checkConnection = async () => {
    try {
      const connected = await api.checkHealth();
      setIsConnected(connected);
    } catch {
      setIsConnected(false);
    } finally {
      setChecking(false);
    }
  };

  // Hide the green \"Backend Connected\" box completely.
  // Only show a small red warning chip when the backend is NOT reachable.
  if (checking || isConnected) return null;

  return (
    <div className="connection-status disconnected">
      <span className="connection-status__indicator">🔴</span>
      <span className="connection-status__label">Backend Disconnected</span>
    </div>
  );
}

export default ConnectionStatus;

