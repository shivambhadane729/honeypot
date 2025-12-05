import React, { useState, useEffect } from 'react';
import { Line, Bar, Doughnut } from 'react-chartjs-2';
import { api } from '../api';
import './Pages.css';

function MLInsights() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadInsights();
    const interval = setInterval(loadInsights, 5000); // Refresh every 5 seconds for dynamic updates
    return () => clearInterval(interval);
  }, []);

  const loadInsights = async () => {
    try {
      setLoading(true);
      const insights = await api.getMLInsights();
      setData(insights || {});
    } catch (error) {
      // Silently handle connection errors (backend not running)
      if (!error.isConnectionError && error.message !== 'BACKEND_CONNECTION_ERROR') {
        console.error('Error loading ML insights:', error);
      }
      // Set empty data structure on error
      setData({
        avg_anomaly_score: 0,
        total_anomalies: 0,
        high_score_ips: [],
        anomaly_trend: [],
        risk_distribution: [],
        darknet_distribution: [],
        suspicious_traffic_count: 0,
        model_info: {}
      });
    } finally {
      setLoading(false);
    }
  };

  if (loading && !data) {
    return <div className="page-container"><div className="loading">Loading ML insights...</div></div>;
  }
  
  // Initialize with empty data if not loaded
  if (!data) {
    return (
      <div className="page-container">
        <div className="page-header">
          <h1>ML Insights</h1>
          <button onClick={loadInsights} className="refresh-btn">Refresh</button>
        </div>
        <div className="no-data">No ML insights available yet</div>
      </div>
    );
  }

  // Use real data only - no demo fallbacks
  const avgAnomaly = data.avg_anomaly_score || 0;
  const totalAnomalies = data.total_anomalies || 0;
  const highScoreCount = data.high_score_ips?.length || 0;
  const chartOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        labels: { color: '#a0aec0', font: { size: 10 } }
      }
    },
    scales: {
      x: { grid: { color: '#4a5568' }, ticks: { color: '#a0aec0' } },
      y: { grid: { color: '#4a5568' }, ticks: { color: '#a0aec0' } }
    }
  };

  return (
    <div className="page-container">
      <div className="page-header">
        <h1>ML Insights</h1>
        <button onClick={loadInsights} className="refresh-btn">Refresh</button>
      </div>

      <div className="stats-grid">
        <div className="stat-card">
          <h3>Average Anomaly Score</h3>
          <div className="value" style={{ color: '#eab308' }}>{avgAnomaly.toFixed(4)}</div>
        </div>
        <div className="stat-card">
          <h3>Total Anomalies</h3>
          <div className="value" style={{ color: '#ef4444' }}>{totalAnomalies.toLocaleString()}</div>
        </div>
        <div className="stat-card">
          <h3>High-Score IPs</h3>
          <div className="value" style={{ color: '#f97316' }}>{highScoreCount}</div>
        </div>
        <div className="stat-card">
          <h3>Suspicious Traffic (Tor/VPN)</h3>
          <div className="value" style={{ color: '#a855f7' }}>
            {(data.suspicious_traffic_count || 0).toLocaleString()}
          </div>
        </div>
      </div>

      <div className="chart-container">
        <div className="chart-title">Anomaly Score Trend (24h)</div>
        <Line
          data={{
            labels: (data.anomaly_trend && data.anomaly_trend.length > 0
              ? data.anomaly_trend.map(t => {
                  try {
                    // Parse SQLite datetime format: 'YYYY-MM-DD HH:00:00'
                    const timeStr = t.time || '';
                    if (timeStr.includes(' ')) {
                      const [datePart, timePart] = timeStr.split(' ');
                      const [hour] = timePart.split(':');
                      return `${hour}:00`; // Format as HH:00
                    }
                    return new Date(t.time).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
                  } catch {
                    return t.time || 'Unknown';
                  }
                })
              : []),
            datasets: [{
              label: 'Average Score',
              data: (data.anomaly_trend && data.anomaly_trend.length > 0
                ? data.anomaly_trend.map(t => t.avg_score)
                : []),
              borderColor: '#eab308',
              backgroundColor: 'rgba(234, 179, 8, 0.1)',
              tension: 0.4,
              fill: true
            }, {
              label: 'Attack Count',
              data: (data.anomaly_trend && data.anomaly_trend.length > 0
                ? data.anomaly_trend.map(t => t.count)
                : []),
              borderColor: '#ef4444',
              backgroundColor: 'rgba(239, 68, 68, 0.1)',
              tension: 0.4,
              fill: true,
              yAxisID: 'y1'
            }]
          }}
          options={{
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
                ticks: { color: '#a0aec0' }
              }
            }
          }}
        />
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '20px' }}>
        <div className="chart-container">
          <div className="chart-title">High-Score IPs (Score ≥ 0.8)</div>
          <Bar
            data={{
              labels: (data.high_score_ips && data.high_score_ips.length > 0
                ? data.high_score_ips.map(ip => ip.ip.substring(0, 15) + '...')
                : []),
              datasets: [{
                label: 'Average Score',
                data: (data.high_score_ips && data.high_score_ips.length > 0
                  ? data.high_score_ips.map(ip => ip.avg_score)
                  : []),
                backgroundColor: '#ef4444'
              }]
            }}
            options={chartOptions}
          />
        </div>

        <div className="chart-container">
          <div className="chart-title">Risk Level Distribution</div>
          <Doughnut
            data={{
              labels: (data.risk_distribution && data.risk_distribution.length > 0
                ? data.risk_distribution.map(r => r.risk_level)
                : []),
              datasets: [{
                data: (data.risk_distribution && data.risk_distribution.length > 0
                  ? data.risk_distribution.map(r => r.count)
                  : []),
                backgroundColor: ['#ef4444', '#f97316', '#eab308', '#22c55e']
              }]
            }}
            options={{
              responsive: true,
              maintainAspectRatio: false,
              plugins: {
                legend: { labels: { color: '#a0aec0' }, position: 'bottom' }
              }
            }}
          />
        </div>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '20px', marginTop: '20px' }}>
        <div className="chart-container">
          <div className="chart-title">CIC-DarkNet Traffic Type Distribution</div>
          <Doughnut
            data={{
              labels: (data.darknet_distribution && data.darknet_distribution.length > 0
                ? data.darknet_distribution.map(d => d.traffic_type)
                : []),
              datasets: [{
                data: (data.darknet_distribution && data.darknet_distribution.length > 0
                  ? data.darknet_distribution.map(d => d.count)
                  : []),
                backgroundColor: ['#22c55e', '#3b82f6', '#ef4444', '#f97316']
              }]
            }}
            options={{
              responsive: true,
              maintainAspectRatio: false,
              plugins: {
                legend: { labels: { color: '#a0aec0' }, position: 'bottom' }
              }
            }}
          />
        </div>

        <div className="chart-container">
          <div className="chart-title">ML Model Ensemble</div>
          <div style={{ padding: '20px', color: '#a0aec0' }}>
            {data.model_info && (
              <div>
                <div style={{ marginBottom: '15px' }}>
                  <strong style={{ color: '#fff' }}>{data.model_info.random_forest?.name}</strong>
                  <div>Accuracy: {(data.model_info.random_forest?.accuracy * 100).toFixed(2)}%</div>
                  <div>Weight: {(data.model_info.random_forest?.weight * 100).toFixed(0)}%</div>
                </div>
                <div style={{ marginBottom: '15px' }}>
                  <strong style={{ color: '#fff' }}>{data.model_info.isolation_forest?.name}</strong>
                  <div>Accuracy: {(data.model_info.isolation_forest?.accuracy * 100).toFixed(2)}%</div>
                  <div>Weight: {(data.model_info.isolation_forest?.weight * 100).toFixed(0)}%</div>
                </div>
                <div>
                  <strong style={{ color: '#fff' }}>{data.model_info.darknet?.name}</strong>
                  <div>Accuracy: {(data.model_info.darknet?.accuracy * 100).toFixed(2)}%</div>
                  <div>Weight: {(data.model_info.darknet?.weight * 100).toFixed(0)}%</div>
                  <div style={{ fontSize: '0.9em', marginTop: '5px' }}>
                    {data.model_info.darknet?.purpose}
                  </div>
                </div>
              </div>
            )}
          </div>
        </div>
      </div>

      <div className="chart-container">
        <div className="chart-title">Top High-Score IPs Details</div>
        <table className="events-table">
          <thead>
            <tr>
              <th>IP Address</th>
              <th>Average Score</th>
              <th>Attack Count</th>
            </tr>
          </thead>
          <tbody>
            {data.high_score_ips && data.high_score_ips.length > 0 ? (
              data.high_score_ips.map((ip, index) => (
                <tr key={index}>
                  <td className="ip-cell">{ip.ip}</td>
                  <td>
                    <span style={{ color: ip.avg_score >= 0.8 ? '#ef4444' : '#f97316' }}>
                      {ip.avg_score.toFixed(4)}
                    </span>
                  </td>
                  <td>{ip.count}</td>
                </tr>
              ))
            ) : (
              <tr>
                <td colSpan="3" style={{ textAlign: 'center', color: '#a0aec0' }}>No high-score IPs yet</td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
}

export default MLInsights;

