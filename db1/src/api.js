// API service for connecting to backend
const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000';

// Helper function to handle API calls with better error messages
const fetchWithErrorHandling = async (url, options = {}) => {
  try {
    const response = await fetch(url, {
      ...options,
      headers: {
        'Content-Type': 'application/json',
        ...options.headers
      }
    });
    
    if (!response.ok) {
      const errorText = await response.text();
      throw new Error(`API Error (${response.status}): ${errorText || response.statusText}`);
    }
    
    return response.json();
  } catch (error) {
    // Check for network/connection errors
    const isConnectionError = 
      error.message.includes('Failed to fetch') || 
      error.message.includes('ERR_CONNECTION_REFUSED') || 
      error.message.includes('ERR_INTERNET_DISCONNECTED') || 
      error.message.includes('ERR_NETWORK') ||
      error.name === 'TypeError' ||
      error.message.includes('NetworkError');
    
    if (isConnectionError) {
      // Create a silent connection error (don't log to console)
      const silentError = new Error('BACKEND_CONNECTION_ERROR');
      silentError.isConnectionError = true;
      silentError.originalError = error;
      throw silentError;
    }
    throw error;
  }
};

export const api = {
  // Check if backend is available
  checkHealth: async () => {
    try {
      const controller = new AbortController();
      const timeoutId = setTimeout(() => controller.abort(), 3000);
      const response = await fetch(`${API_BASE_URL}/health`, { 
        signal: controller.signal,
        cache: 'no-cache'
      });
      clearTimeout(timeoutId);
      return response.ok;
    } catch {
      return false;
    }
  },

  // Live Events
  getLiveEvents: async (limit = 50, sourceIp = null, minScore = null) => {
    const params = new URLSearchParams({ limit: limit.toString() });
    if (sourceIp) params.append('source_ip', sourceIp);
    if (minScore !== null) params.append('min_score', minScore.toString());
    
    return fetchWithErrorHandling(`${API_BASE_URL}/api/live-events?${params}`);
  },

  // Analytics
  getAnalytics: async () => {
    return fetchWithErrorHandling(`${API_BASE_URL}/api/analytics`);
  },

  // Map Data
  getMapData: async () => {
    return fetchWithErrorHandling(`${API_BASE_URL}/api/map-data`);
  },

  // ML Insights
  getMLInsights: async () => {
    return fetchWithErrorHandling(`${API_BASE_URL}/api/ml-insights`);
  },

  // Alerts
  getAlerts: async (threshold = 0.85, limit = 50) => {
    const params = new URLSearchParams({
      threshold: threshold.toString(),
      limit: limit.toString()
    });
    return fetchWithErrorHandling(`${API_BASE_URL}/api/alerts?${params}`);
  },

  // Investigation
  investigateIP: async (ip) => {
    return fetchWithErrorHandling(`${API_BASE_URL}/api/investigate/${ip}`);
  },

  // Stats (for dashboard)
  getStats: async () => {
    return fetchWithErrorHandling(`${API_BASE_URL}/stats`);
  }
};

