import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { Chart as ChartJS, CategoryScale, LinearScale, BarElement, LineElement, PointElement, ArcElement, Title, Tooltip, Legend, Filler } from 'chart.js';
import { Line, Bar, Doughnut } from 'react-chartjs-2';
import { api } from '../api';
import './Pages.css';

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

function Investigation() {
  const { ip } = useParams();
  const navigate = useNavigate();
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [searchIp, setSearchIp] = useState(ip || '');
  const [expandedLog, setExpandedLog] = useState(null);
  const [viewMode, setViewMode] = useState('overview'); // overview, timeline, details

  useEffect(() => {
    if (ip) {
      loadInvestigation(ip);
    }
  }, [ip]);

  const loadInvestigation = async (targetIp) => {
    try {
      setLoading(true);
      const investigation = await api.investigateIP(targetIp);
      setData(investigation);
    } catch (error) {
      console.error('Error loading investigation:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleSearch = () => {
    if (searchIp) {
      navigate(`/investigate/${searchIp}`);
    }
  };

  const exportInvestigation = () => {
    if (!data) return;
    
    const csv = [
      ['IP', 'Country', 'ISP', 'First Seen', 'Last Seen', 'Total Attacks', 'Avg Score', 'Max Score'].join(','),
      [
        data.ip,
        data.geo_info?.country || 'Unknown',
        data.geo_info?.isp || 'Unknown',
        data.stats?.first_seen || '',
        data.stats?.last_seen || '',
        data.stats?.total_attacks || 0,
        data.stats?.avg_score || 0,
        data.stats?.max_score || 0
      ].join(',')
    ].join('\n');

    const blob = new Blob([csv], { type: 'text/csv' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `investigation_${data.ip}_${new Date().toISOString().split('T')[0]}.csv`;
    a.click();
  };

  if (loading || !data) {
    return (
      <div className="page-container">
        <div className="page-header">
          <h1>IP Investigation</h1>
          <div className="filters">
            <input
              type="text"
              placeholder="Enter IP address..."
              value={searchIp}
              onChange={(e) => setSearchIp(e.target.value)}
              onKeyPress={(e) => e.key === 'Enter' && handleSearch()}
              className="filter-input"
            />
            <button onClick={handleSearch} className="refresh-btn">Investigate</button>
          </div>
        </div>
        <div className="loading">Loading investigation data...</div>
      </div>
    );
  }

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

  // Prepare chart data
  const scoreTrendData = data.score_trend && data.score_trend.length > 0 ? {
    labels: data.score_trend.map(t => {
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
      label: 'ML Score',
      data: data.score_trend.map(t => t.score || 0),
      borderColor: '#eab308',
      backgroundColor: 'rgba(234, 179, 8, 0.1)',
      tension: 0.4,
      fill: true
    }]
  } : null;

  // Service distribution
  const serviceCounts = {};
  data.logs?.forEach(log => {
    const service = log.target_service || 'Unknown';
    serviceCounts[service] = (serviceCounts[service] || 0) + 1;
  });

  const serviceDistributionData = {
    labels: Object.keys(serviceCounts),
    datasets: [{
      data: Object.values(serviceCounts),
      backgroundColor: ['#ef4444', '#f97316', '#eab308', '#22c55e', '#3b82f6', '#8b5cf6']
    }]
  };

  // Action distribution
  const actionCounts = {};
  data.logs?.forEach(log => {
    const action = log.action || 'Unknown';
    actionCounts[action] = (actionCounts[action] || 0) + 1;
  });

  const actionDistributionData = {
    labels: Object.keys(actionCounts).slice(0, 10),
    datasets: [{
      label: 'Actions',
      data: Object.keys(actionCounts).slice(0, 10).map(a => actionCounts[a]),
      backgroundColor: '#4299e1'
    }]
  };

  // Risk level distribution
  const riskCounts = {};
  data.logs?.forEach(log => {
    const risk = log.ml_risk_level || 'UNKNOWN';
    riskCounts[risk] = (riskCounts[risk] || 0) + 1;
  });

  const riskDistributionData = {
    labels: Object.keys(riskCounts),
    datasets: [{
      data: Object.values(riskCounts),
      backgroundColor: ['#ef4444', '#f97316', '#eab308', '#3b82f6']
    }]
  };

  const getRiskColor = (score) => {
    if (!score) return '#a0aec0';
    if (score >= 0.9) return '#ef4444';
    if (score >= 0.85) return '#f97316';
    if (score >= 0.75) return '#eab308';
    return '#3b82f6';
  };

  const getRiskLabel = (score) => {
    if (!score) return 'UNKNOWN';
    if (score >= 0.9) return 'CRITICAL';
    if (score >= 0.85) return 'HIGH';
    if (score >= 0.75) return 'MEDIUM';
    return 'LOW';
  };

  return (
    <div className="page-container">
      <div className="page-header">
        <h1>IP Investigation: {data.ip}</h1>
        <div className="filters">
          <input
            type="text"
            placeholder="Enter IP address..."
            value={searchIp}
            onChange={(e) => setSearchIp(e.target.value)}
            onKeyPress={(e) => e.key === 'Enter' && handleSearch()}
            className="filter-input"
          />
          <button onClick={handleSearch} className="refresh-btn">Investigate</button>
          <button onClick={exportInvestigation} className="refresh-btn" style={{ background: '#22c55e' }}>
            Export
          </button>
        </div>
      </div>

      {/* View Mode Tabs */}
      <div style={{ 
        display: 'flex', 
        gap: '8px', 
        marginBottom: '20px',
        borderBottom: '2px solid #2d3748'
      }}>
        <button
          onClick={() => setViewMode('overview')}
          style={{
            padding: '10px 20px',
            background: viewMode === 'overview' ? '#4299e1' : 'transparent',
            border: 'none',
            color: viewMode === 'overview' ? '#fff' : '#a0aec0',
            cursor: 'pointer',
            borderBottom: viewMode === 'overview' ? '2px solid #4299e1' : '2px solid transparent',
            marginBottom: '-2px'
          }}
        >
          Overview
        </button>
        <button
          onClick={() => setViewMode('timeline')}
          style={{
            padding: '10px 20px',
            background: viewMode === 'timeline' ? '#4299e1' : 'transparent',
            border: 'none',
            color: viewMode === 'timeline' ? '#fff' : '#a0aec0',
            cursor: 'pointer',
            borderBottom: viewMode === 'timeline' ? '2px solid #4299e1' : '2px solid transparent',
            marginBottom: '-2px'
          }}
        >
          Timeline
        </button>
        <button
          onClick={() => setViewMode('details')}
          style={{
            padding: '10px 20px',
            background: viewMode === 'details' ? '#4299e1' : 'transparent',
            border: 'none',
            color: viewMode === 'details' ? '#fff' : '#a0aec0',
            cursor: 'pointer',
            borderBottom: viewMode === 'details' ? '2px solid #4299e1' : '2px solid transparent',
            marginBottom: '-2px'
          }}
        >
          Detailed Logs
        </button>
      </div>

      {/* Overview Tab */}
      {viewMode === 'overview' && (
        <>
          {/* IP Information Card */}
          <div className="investigation-header">
            <h2 style={{ margin: '0 0 20px 0', color: '#f7fafc' }}>IP Information</h2>
            <div style={{ 
              display: 'grid', 
              gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))', 
              gap: '16px',
              color: '#a0aec0', 
              fontSize: '14px' 
            }}>
              <div>
                <strong style={{ color: '#cbd5e0' }}>IP Address:</strong>
                <div style={{ fontFamily: 'monospace', color: '#4299e1', fontSize: '16px', marginTop: '4px' }}>
                  {data.ip}
                </div>
              </div>
              
              {data.geo_info?.country && (
                <div>
                  <strong style={{ color: '#cbd5e0' }}>Location:</strong>
                  <div style={{ marginTop: '4px' }}>
                    {data.geo_info.city && `${data.geo_info.city}, `}
                    {data.geo_info.region && `${data.geo_info.region}, `}
                    {data.geo_info.country}
                  </div>
                </div>
              )}
              
              {data.geo_info?.isp && (
                <div>
                  <strong style={{ color: '#cbd5e0' }}>ISP:</strong>
                  <div style={{ marginTop: '4px' }}>{data.geo_info.isp}</div>
                </div>
              )}
              
              {data.stats?.first_seen && (
                <div>
                  <strong style={{ color: '#cbd5e0' }}>First Seen:</strong>
                  <div style={{ marginTop: '4px' }}>
                    {new Date(data.stats.first_seen).toLocaleString()}
                  </div>
                </div>
              )}
              
              {data.stats?.last_seen && (
                <div>
                  <strong style={{ color: '#cbd5e0' }}>Last Seen:</strong>
                  <div style={{ marginTop: '4px' }}>
                    {new Date(data.stats.last_seen).toLocaleString()}
                  </div>
                </div>
              )}

              {data.geo_info?.latitude && data.geo_info?.longitude && (
                <div>
                  <strong style={{ color: '#cbd5e0' }}>Coordinates:</strong>
                  <div style={{ marginTop: '4px', fontFamily: 'monospace' }}>
                    {data.geo_info.latitude.toFixed(4)}, {data.geo_info.longitude.toFixed(4)}
                  </div>
                  <a
                    href={`https://www.google.com/maps?q=${data.geo_info.latitude},${data.geo_info.longitude}`}
                    target="_blank"
                    rel="noopener noreferrer"
                    style={{ color: '#4299e1', fontSize: '12px', marginTop: '4px', display: 'block' }}
                  >
                    View on Map
                  </a>
                </div>
              )}
            </div>

            {/* Statistics Grid */}
            <div className="investigation-stats" style={{ marginTop: '24px' }}>
              <div className="investigation-stat">
                <div className="investigation-stat-label">Total Attacks</div>
                <div className="investigation-stat-value" style={{ color: '#ef4444' }}>
                  {data.stats?.total_attacks || 0}
                </div>
              </div>
              <div className="investigation-stat">
                <div className="investigation-stat-label">Avg ML Score</div>
                <div className="investigation-stat-value" style={{ color: '#eab308' }}>
                  {(data.stats?.avg_score || 0).toFixed(4)}
                </div>
              </div>
              <div className="investigation-stat">
                <div className="investigation-stat-label">Max ML Score</div>
                <div className="investigation-stat-value" style={{ color: '#f97316' }}>
                  {(data.stats?.max_score || 0).toFixed(4)}
                </div>
              </div>
              <div className="investigation-stat">
                <div className="investigation-stat-label">Unique Actions</div>
                <div className="investigation-stat-value" style={{ color: '#4299e1' }}>
                  {data.stats?.unique_actions || 0}
                </div>
              </div>
              <div className="investigation-stat">
                <div className="investigation-stat-label">Target Services</div>
                <div className="investigation-stat-value" style={{ color: '#22c55e' }}>
                  {data.stats?.unique_services || 0}
                </div>
              </div>
              <div className="investigation-stat">
                <div className="investigation-stat-label">Threat Level</div>
                <div className="investigation-stat-value" style={{ color: getRiskColor(data.stats?.avg_score) }}>
                  {getRiskLabel(data.stats?.avg_score)}
                </div>
              </div>
            </div>
          </div>

          {/* Charts Section */}
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(400px, 1fr))', gap: '20px', marginBottom: '20px' }}>
            {scoreTrendData && (
              <div className="chart-container" style={{ height: '300px' }}>
                <div className="chart-title">ML Score Trend Over Time (24h)</div>
                {scoreTrendData ? (
                  <Line data={scoreTrendData} options={{
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
                      }
                    }
                  }} />
                ) : (
                  <div className="no-data">No score trend data available</div>
                )}
              </div>
            )}

            <div className="chart-container" style={{ height: '300px' }}>
              <div className="chart-title">Service Distribution</div>
              <Doughnut 
                data={serviceDistributionData} 
                options={{
                  responsive: true,
                  maintainAspectRatio: false,
                  plugins: {
                    legend: {
                      position: 'bottom',
                      labels: { color: '#a0aec0', font: { size: 10 }, padding: 10 }
                    }
                  }
                }}
              />
            </div>

            <div className="chart-container" style={{ height: '300px' }}>
              <div className="chart-title">Action Distribution</div>
              <Bar data={actionDistributionData} options={chartOptions} />
            </div>

            {Object.keys(riskCounts).length > 0 && (
              <div className="chart-container" style={{ height: '300px' }}>
                <div className="chart-title">Risk Level Distribution</div>
                <Doughnut 
                  data={riskDistributionData} 
                  options={{
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                      legend: {
                        position: 'bottom',
                        labels: { color: '#a0aec0', font: { size: 10 }, padding: 10 }
                      }
                    }
                  }}
                />
              </div>
            )}
          </div>
        </>
      )}

      {/* Timeline Tab */}
      {viewMode === 'timeline' && (
        <div className="logs-list">
          <h2 style={{ margin: '0 0 20px 0', color: '#f7fafc' }}>Attack Timeline</h2>
          {data.logs && data.logs.length > 0 ? (
            <div style={{ position: 'relative' }}>
              {data.logs.map((log, index) => (
                <div key={index} style={{ 
                  marginBottom: '16px',
                  paddingLeft: '40px',
                  position: 'relative',
                  borderLeft: '2px solid #4a5568'
                }}>
                  <div style={{
                    position: 'absolute',
                    left: '-6px',
                    top: '0',
                    width: '12px',
                    height: '12px',
                    borderRadius: '50%',
                    background: getRiskColor(log.ml_score || 0),
                    border: '2px solid #1a202c'
                  }} />
                  <div className="log-item" style={{ marginBottom: 0 }}>
                    <div className="log-item-header">
                      <span className="log-item-time">{new Date(log.created_at || log.timestamp).toLocaleString()}</span>
                      <span className="log-item-action">{log.action}</span>
                    </div>
                    <div style={{ color: '#a0aec0', fontSize: '12px', marginTop: '8px' }}>
                      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '8px' }}>
                        <div><strong>Service:</strong> {log.target_service}</div>
                        {log.target_file && <div><strong>Target:</strong> {log.target_file}</div>}
                        {log.ml_score && (
                          <div>
                            <strong>ML Score:</strong>{' '}
                            <span style={{ color: getRiskColor(log.ml_score) }}>
                              {log.ml_score.toFixed(4)} ({getRiskLabel(log.ml_score)})
                            </span>
                          </div>
                        )}
                        {log.ml_risk_level && <div><strong>Risk:</strong> {log.ml_risk_level}</div>}
                      </div>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <div className="no-data">No timeline data available</div>
          )}
        </div>
      )}

      {/* Detailed Logs Tab */}
      {viewMode === 'details' && (
        <div className="logs-list">
          <h2 style={{ margin: '0 0 20px 0', color: '#f7fafc' }}>
            Detailed Activity Logs ({data.logs?.length || 0} entries)
          </h2>
          {data.logs && data.logs.length > 0 ? (
            data.logs.map((log, index) => (
              <div 
                key={index} 
                className="log-item"
                style={{ 
                  cursor: 'pointer',
                  transition: 'all 0.2s'
                }}
                onClick={() => setExpandedLog(expandedLog === index ? null : index)}
              >
                <div className="log-item-header">
                  <span className="log-item-time">
                    {new Date(log.created_at || log.timestamp).toLocaleString()}
                  </span>
                  <span className="log-item-action">{log.action}</span>
                  {log.ml_score && (
                    <span style={{
                      padding: '2px 8px',
                      background: getRiskColor(log.ml_score),
                      borderRadius: '4px',
                      fontSize: '11px',
                      fontWeight: '600',
                      color: '#fff'
                    }}>
                      {log.ml_score.toFixed(4)}
                    </span>
                  )}
                </div>
                <div style={{ color: '#a0aec0', fontSize: '12px', marginTop: '8px' }}>
                  <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '8px' }}>
                    <div><strong>Service:</strong> {log.target_service}</div>
                    {log.target_file && <div><strong>Target:</strong> {log.target_file}</div>}
                    {log.ml_risk_level && <div><strong>Risk Level:</strong> {log.ml_risk_level}</div>}
                    {log.is_anomaly !== undefined && (
                      <div><strong>Anomaly:</strong> {log.is_anomaly ? 'Yes' : 'No'}</div>
                    )}
                    {log.user_agent && <div><strong>User Agent:</strong> {log.user_agent}</div>}
                    {log.protocol && <div><strong>Protocol:</strong> {log.protocol}</div>}
                  </div>
                </div>
                
                {expandedLog === index && (
                  <div style={{
                    marginTop: '12px',
                    padding: '12px',
                    background: '#2d3748',
                    borderRadius: '4px',
                    border: '1px solid #4a5568',
                    fontSize: '11px',
                    fontFamily: 'monospace'
                  }}>
                    <div style={{ marginBottom: '8px', color: '#cbd5e0', fontWeight: '600' }}>
                      Full Log Details:
                    </div>
                    <pre style={{ 
                      margin: 0, 
                      color: '#a0aec0',
                      whiteSpace: 'pre-wrap',
                      wordBreak: 'break-word'
                    }}>
                      {JSON.stringify(log, null, 2)}
                    </pre>
                  </div>
                )}
              </div>
            ))
          ) : (
            <div className="no-data">No logs available for this IP</div>
          )}
        </div>
      )}
    </div>
  );
}

export default Investigation;
