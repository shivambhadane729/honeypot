import React, { useState, useEffect } from 'react';
import { Chart as ChartJS, CategoryScale, LinearScale, BarElement, LineElement, PointElement, ArcElement, Title, Tooltip, Legend, Filler } from 'chart.js';
import { Bar, Line, Doughnut } from 'react-chartjs-2';
import { api } from '../api';
import '../App.css';

ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  LineElement,
  PointElement,
  ArcElement,
  Title,
  Tooltip,
  Legend,
  Filler
);

function Dashboard() {
  const [stats, setStats] = useState({
    total_logs: 0,
    unique_ips: 0,
    recent_activity_24h: 0,
    top_services: [],
    top_actions: [],
    top_countries: [],
    avg_ml_score: 0,
    high_risk_count: 0,
    anomaly_count: 0,
    risk_distribution: [],
    ml_score_trend: []
  });
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [isConnected, setIsConnected] = useState(false);
  const [lastUpdate, setLastUpdate] = useState(new Date());

  useEffect(() => {
    checkConnection();
    loadStats();
    // Refresh every 5 seconds for dynamic updates
    const interval = setInterval(() => {
      checkConnection();
      loadStats();
    }, 5000);
    return () => clearInterval(interval);
  }, []);

  const checkConnection = async () => {
    const connected = await api.checkHealth();
    setIsConnected(connected);
  };

  const loadStats = async () => {
    try {
      setError(null);
      const data = await api.getStats();
      setStats(data?.statistics || {
        total_logs: 0,
        unique_ips: 0,
        recent_activity_24h: 0,
        top_services: [],
        top_actions: [],
        top_countries: [],
        avg_ml_score: 0,
        high_risk_count: 0,
        anomaly_count: 0,
        risk_distribution: [],
        ml_score_trend: []
      });
      setLastUpdate(new Date());
      setIsConnected(true);
    } catch (error) {
      // Silently handle connection errors (backend not running)
      if (!error.isConnectionError && error.message !== 'BACKEND_CONNECTION_ERROR') {
        console.error('Error loading stats:', error);
      }
      setError(error.isConnectionError ? null : error.message);
      setIsConnected(false);
    } finally {
      setLoading(false);
    }
  };

  const chartOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        labels: {
          color: '#a0aec0',
          font: { size: 10 }
        }
      }
    },
    scales: {
      x: {
        grid: { color: '#4a5568' },
        ticks: { color: '#a0aec0', font: { size: 10 } }
      },
      y: {
        grid: { color: '#4a5568' },
        ticks: { color: '#a0aec0', font: { size: 10 } }
      }
    }
  };

  const pieOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        position: 'bottom',
        labels: {
          color: '#a0aec0',
          font: { size: 10 },
          padding: 15
        }
      }
    }
  };

  // Derived helper metrics for extra summary tiles
  const totalCountries = stats?.top_countries?.length || 0;
  // Low-risk events = total - high-risk (anomalies can overlap with high-risk, so don't double subtract)
  const lowRiskEvents = Math.max(
    (stats?.total_logs || 0) - (stats?.high_risk_count || 0),
    0
  );

  if (loading) {
    return <div className="App"><div className="loading">Loading dashboard...</div></div>;
  }

  // We no longer show the large fixed green \"Connected\" pill on the dashboard.
  // Connection problems are surfaced via the error banner below instead.
  const connectionStatus = null;

  // Calculate ML metrics
  const getRiskColor = (score) => {
    if (score >= 0.8) return '#ef4444';
    if (score >= 0.6) return '#f97316';
    if (score >= 0.4) return '#eab308';
    return '#22c55e';
  };

  // Use real data - no demo fallbacks for dynamic dashboard
  const avgMlScore = stats.avg_ml_score || 0;
  const highRiskCount = stats.high_risk_count || 0;
  const anomalyCount = stats.anomaly_count || 0;

  // Use real data - show empty state if no data
  const honeypotBarData = (stats?.top_services && stats.top_services.length > 0)
    ? {
        labels: stats.top_services.map(s => s.service),
        datasets: [{
          label: 'Attacks',
          data: stats.top_services.map(s => s.count),
          backgroundColor: ['#ef4444', '#f97316', '#eab308', '#22c55e', '#3b82f6']
        }]
      }
    : {
        labels: ['No Data'],
        datasets: [{
          label: 'Attacks',
          data: [0],
          backgroundColor: ['#4a5568']
        }]
      };

  const protocolBarData = (stats?.top_actions && stats.top_actions.length > 0)
    ? {
        labels: stats.top_actions.slice(0, 6).map(a => a.action),
        datasets: [{
          label: 'Attacks',
          data: stats.top_actions.slice(0, 6).map(a => a.count),
          backgroundColor: ['#ef4444', '#3b82f6', '#22c55e', '#8b5cf6', '#eab308', '#f97316']
        }]
      }
    : {
        labels: ['No Data'],
        datasets: [{
          label: 'Attacks',
          data: [0],
          backgroundColor: ['#4a5568']
        }]
      };

  const countryPieData = (stats?.top_countries && stats.top_countries.length > 0)
    ? {
        labels: stats.top_countries.slice(0, 10).map(c => c.country),
        datasets: [{
          data: stats.top_countries.slice(0, 10).map(c => c.count),
          backgroundColor: ['#8b5cf6', '#ec4899', '#22c55e', '#eab308', '#3b82f6', '#ef4444', '#f97316', '#06b6d4', '#f43f5e', '#10b981']
        }]
      }
    : {
        labels: ['No Data'],
        datasets: [{
          data: [0],
          backgroundColor: ['#4a5568']
        }]
      };

  const riskDistributionData = (stats?.risk_distribution && stats.risk_distribution.length > 0)
    ? {
        labels: stats.risk_distribution.map(r => r.risk_level || 'UNKNOWN'),
        datasets: [{
          data: stats.risk_distribution.map(r => r.count || 0),
          backgroundColor: ['#ef4444', '#f97316', '#eab308', '#22c55e', '#3b82f6']
        }]
      }
    : {
        labels: ['No Data'],
        datasets: [{
          data: [0],
          backgroundColor: ['#4a5568']
        }]
      };

  const mlScoreTrendData = (stats?.ml_score_trend && stats.ml_score_trend.length > 0)
    ? {
        labels: stats.ml_score_trend.map(t => {
          try {
            // Parse SQLite datetime format: 'YYYY-MM-DD HH:00:00'
            const timeStr = t.time || '';
            if (timeStr.includes(' ')) {
              const [datePart, timePart] = timeStr.split(' ');
              const [year, month, day] = datePart.split('-');
              const [hour] = timePart.split(':');
              return `${hour}:00`; // Format as HH:00
            }
            return new Date(t.time).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
          } catch {
            return t.time || 'Unknown';
          }
        }),
        datasets: [{
          label: 'Avg ML Score',
          data: stats.ml_score_trend.map(t => t.avg_score || 0),
          borderColor: '#eab308',
          backgroundColor: 'rgba(234, 179, 8, 0.1)',
          tension: 0.4,
          fill: true
        }, {
          label: 'Attack Count',
          data: stats.ml_score_trend.map(t => t.count || 0),
          borderColor: '#ef4444',
          backgroundColor: 'rgba(239, 68, 68, 0.1)',
          tension: 0.4,
          fill: true,
          yAxisID: 'y1'
        }]
      }
    : {
        labels: ['No Data'],
        datasets: [{
          label: 'Avg ML Score',
          data: [0],
          borderColor: '#4a5568',
          backgroundColor: 'rgba(74, 85, 104, 0.1)',
          tension: 0.4,
          fill: true
        }, {
          label: 'Attack Count',
          data: [0],
          borderColor: '#4a5568',
          backgroundColor: 'rgba(74, 85, 104, 0.1)',
          tension: 0.4,
          fill: true,
          yAxisID: 'y1'
        }]
      };

  return (
    <div className="App">
      {connectionStatus}
      {error && (
        <div style={{
          background: '#7f1d1d',
          border: '1px solid #ef4444',
          color: '#fca5a5',
          padding: '16px',
          margin: '16px',
          borderRadius: '8px',
          textAlign: 'center'
        }}>
          <strong>Backend Connection Error:</strong> {error}
        </div>
      )}

      {/* Dynamic Update Indicator - Small, unobtrusive in corner */}
      {isConnected && (
        <div style={{
          position: 'fixed',
          bottom: '10px',
          right: '10px',
          background: 'rgba(34, 197, 94, 0.8)',
          color: 'white',
          padding: '4px 8px',
          borderRadius: '12px',
          fontSize: '9px',
          zIndex: 998,
          boxShadow: '0 2px 8px rgba(0,0,0,0.3)',
          fontWeight: '500',
          backdropFilter: 'blur(10px)'
        }}>
          Live
        </div>
      )}

      <div className="main-content">
        {/* Primary Metrics Row */}
        <div className="grid-container">
          <div className="kibana-panel grid-3">
            <div className="kibana-panel-header">Total Attacks</div>
            <div className="kibana-panel-content">
              <div className="kibana-metric">
                <div className="kibana-metric-value" style={{ color: '#ef4444' }}>
                  {stats.total_logs?.toLocaleString() || 0}
                </div>
                <div className="kibana-metric-label">All Events Captured</div>
              </div>
            </div>
          </div>

          <div className="kibana-panel grid-3">
            <div className="kibana-panel-header">Unique Attacker IPs</div>
            <div className="kibana-panel-content">
              <div className="kibana-metric">
                <div className="kibana-metric-value" style={{ color: '#eab308' }}>
                  {stats.unique_ips?.toLocaleString() || 0}
                </div>
                <div className="kibana-metric-label">Distinct Sources</div>
              </div>
            </div>
          </div>

          <div className="kibana-panel grid-3">
            <div className="kibana-panel-header">Recent Activity (24h)</div>
            <div className="kibana-panel-content">
              <div className="kibana-metric">
                <div className="kibana-metric-value" style={{ color: '#22c55e' }}>
                  {stats.recent_activity_24h?.toLocaleString() || 0}
                </div>
                <div className="kibana-metric-label">Last 24 Hours</div>
              </div>
            </div>
          </div>

          <div className="kibana-panel grid-3">
            <div className="kibana-panel-header">Countries Observed</div>
            <div className="kibana-panel-content">
              <div className="kibana-metric">
                <div className="kibana-metric-value" style={{ color: '#3b82f6' }}>
                  {totalCountries.toLocaleString()}
                </div>
                <div className="kibana-metric-label">Geo-Enriched Attack Origins</div>
              </div>
            </div>
          </div>
        </div>

        {/* ML Metrics Row */}
        <div className="grid-container">
          <div className="kibana-panel grid-3">
            <div className="kibana-panel-header">Average ML Score</div>
            <div className="kibana-panel-content">
              <div className="kibana-metric">
                <div className="kibana-metric-value" style={{ color: getRiskColor(avgMlScore || 0) }}>
                  {(avgMlScore || 0).toFixed(4)}
                </div>
                <div className="kibana-metric-label">Ensemble Prediction</div>
                <div style={{ fontSize: '12px', color: '#a0aec0', marginTop: '8px' }}>
                  RF (70%) + IF (30%)
                </div>
              </div>
            </div>
          </div>

          <div className="kibana-panel grid-3">
            <div className="kibana-panel-header">High-Risk Attacks</div>
            <div className="kibana-panel-content">
              <div className="kibana-metric">
                <div className="kibana-metric-value" style={{ color: '#ef4444' }}>
                  {highRiskCount.toLocaleString()}
                </div>
                <div className="kibana-metric-label">Score ≥ 0.8</div>
                {stats.total_logs > 0 && (
                  <div style={{ fontSize: '12px', color: '#a0aec0', marginTop: '8px' }}>
                    {((highRiskCount / stats.total_logs) * 100).toFixed(1)}% of total
                  </div>
                )}
              </div>
            </div>
          </div>

          <div className="kibana-panel grid-3">
            <div className="kibana-panel-header">Anomalies Detected</div>
            <div className="kibana-panel-content">
              <div className="kibana-metric">
                <div className="kibana-metric-value" style={{ color: '#f97316' }}>
                  {anomalyCount.toLocaleString()}
                </div>
                <div className="kibana-metric-label">Isolation Forest</div>
                {stats.total_logs > 0 && (
                  <div style={{ fontSize: '12px', color: '#a0aec0', marginTop: '8px' }}>
                    {((anomalyCount / stats.total_logs) * 100).toFixed(1)}% of total
                  </div>
                )}
              </div>
            </div>
          </div>

          <div className="kibana-panel grid-3">
            <div className="kibana-panel-header">Low-Risk / Normal Events</div>
            <div className="kibana-panel-content">
              <div className="kibana-metric">
                <div className="kibana-metric-value" style={{ color: '#22c55e' }}>
                  {lowRiskEvents.toLocaleString()}
                </div>
                <div className="kibana-metric-label">Below High-Risk Threshold</div>
                {stats.total_logs > 0 && (
                  <div style={{ fontSize: '12px', color: '#a0aec0', marginTop: '8px' }}>
                    {((lowRiskEvents / stats.total_logs) * 100).toFixed(1)}% of total
                  </div>
                )}
              </div>
            </div>
          </div>
        </div>

        {/* Charts Row 1 - Service & Actions */}
        <div className="grid-container">
          <div className="kibana-panel grid-4">
            <div className="kibana-panel-header">Attacks by Service</div>
            <div className="kibana-panel-content">
              <div className="chart-container">
                <Bar data={honeypotBarData} options={{
                  ...chartOptions,
                  indexAxis: 'y',
                  plugins: { legend: { display: false } }
                }} />
              </div>
            </div>
          </div>

          <div className="kibana-panel grid-4">
            <div className="kibana-panel-header">Attack Actions</div>
            <div className="kibana-panel-content">
              <div className="chart-container">
                <Bar data={protocolBarData} options={{
                  ...chartOptions,
                  plugins: { legend: { display: false } }
                }} />
              </div>
            </div>
          </div>

          <div className="kibana-panel grid-4">
            <div className="kibana-panel-header">Attacks by Country</div>
            <div className="kibana-panel-content">
              <div className="chart-container">
                <Doughnut data={countryPieData} options={pieOptions} />
              </div>
            </div>
          </div>
        </div>

        {/* Charts Row 2 - ML Analytics */}
        <div className="grid-container">
          <div className="kibana-panel grid-6">
            <div className="kibana-panel-header">ML Score Trend (24h)</div>
            <div className="kibana-panel-content">
              <div className="chart-container">
                <Line data={mlScoreTrendData} options={{
                  ...chartOptions,
                  scales: {
                    ...chartOptions.scales,
                    x: {
                      ...chartOptions.scales.x,
                      ticks: {
                        ...chartOptions.scales.x.ticks,
                        maxRotation: 45,
                        minRotation: 0
                      }
                    },
                    y1: {
                      type: 'linear',
                      display: true,
                      position: 'right',
                      grid: { drawOnChartArea: false },
                      ticks: { color: '#a0aec0', font: { size: 10 } }
                    }
                  }
                }} />
              </div>
            </div>
          </div>

          <div className="kibana-panel grid-6">
            <div className="kibana-panel-header">Risk Level Distribution</div>
            <div className="kibana-panel-content">
              <div className="chart-container">
                <Doughnut data={riskDistributionData} options={pieOptions} />
              </div>
            </div>
          </div>
        </div>

      </div>
    </div>
  );
}

export default Dashboard;
