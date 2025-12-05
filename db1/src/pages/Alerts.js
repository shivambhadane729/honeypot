import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { Chart as ChartJS, CategoryScale, LinearScale, BarElement, LineElement, PointElement, ArcElement, Title, Tooltip, Legend, Filler } from 'chart.js';
import { Bar, Line, Doughnut } from 'react-chartjs-2';
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

function Alerts() {
  const navigate = useNavigate();
  const [alerts, setAlerts] = useState([]);
  const [ipGroups, setIpGroups] = useState([]);
  const [filteredIpGroups, setFilteredIpGroups] = useState([]);
  const [loading, setLoading] = useState(true);
  const [threshold, setThreshold] = useState(0.5); // Lower threshold to show more alerts
  const [filterRiskLevel, setFilterRiskLevel] = useState('ALL');
  const [filterCountry, setFilterCountry] = useState('ALL');
  const [sortBy, setSortBy] = useState('attacks'); // attacks, score, time
  const [stats, setStats] = useState({
    total: 0,
    critical: 0,
    high: 0,
    medium: 0,
    low: 0
  });

  useEffect(() => {
    loadAlerts();
    const interval = setInterval(loadAlerts, 5000); // Refresh every 5 seconds for dynamic updates
    return () => clearInterval(interval);
  }, [threshold]);

  // Also refresh when component mounts to ensure latest data
  useEffect(() => {
    loadAlerts();
  }, []);

  // Group alerts by IP address
  const groupAlertsByIP = (alertsList) => {
    const ipGroups = {};
    alertsList.forEach(alert => {
      const ip = alert.source_ip || 'Unknown';
      if (!ipGroups[ip]) {
        ipGroups[ip] = {
          ip: ip,
          country: alert.country || 'Unknown',
          city: alert.city || 'Unknown',
          isp: alert.isp || 'Unknown',
          alerts: [],
          totalAttacks: 0,
          attackTypes: new Set(),
          services: new Set(),
          maxScore: 0,
          avgScore: 0,
          firstSeen: null,
          lastSeen: null,
          riskLevel: 'MINIMAL'
        };
      }
      ipGroups[ip].alerts.push(alert);
      ipGroups[ip].totalAttacks++;
      if (alert.predicted_attack_type) ipGroups[ip].attackTypes.add(alert.predicted_attack_type);
      if (alert.service) ipGroups[ip].services.add(alert.service);
      if (alert.score > ipGroups[ip].maxScore) ipGroups[ip].maxScore = alert.score;
      if (!ipGroups[ip].firstSeen || new Date(alert.timestamp) < new Date(ipGroups[ip].firstSeen)) {
        ipGroups[ip].firstSeen = alert.timestamp;
      }
      if (!ipGroups[ip].lastSeen || new Date(alert.timestamp) > new Date(ipGroups[ip].lastSeen)) {
        ipGroups[ip].lastSeen = alert.timestamp;
      }
    });
    
    // Calculate average scores and determine risk level
    Object.values(ipGroups).forEach(group => {
      const scores = group.alerts.map(a => a.score || 0).filter(s => s > 0);
      group.avgScore = scores.length > 0 ? scores.reduce((a, b) => a + b, 0) / scores.length : 0;
      group.attackTypes = Array.from(group.attackTypes);
      group.services = Array.from(group.services);
      
      // Determine risk level based on max score
      if (group.maxScore >= 0.8) group.riskLevel = 'HIGH';
      else if (group.maxScore >= 0.6) group.riskLevel = 'MEDIUM';
      else if (group.maxScore >= 0.4) group.riskLevel = 'LOW';
      else group.riskLevel = 'MINIMAL';
    });
    
    return Object.values(ipGroups);
  };

  useEffect(() => {
    filterAndSortIpGroups();
  }, [ipGroups, filterRiskLevel, filterCountry, sortBy]);

  const loadAlerts = async () => {
    try {
      // Only show loading on initial load, not on refreshes
      if (alerts.length === 0 && ipGroups.length === 0) {
        setLoading(true);
      }
      
      // Request all alerts (no limit) for dynamic updates
      const data = await api.getAlerts(threshold, 10000); // Increased limit to 10,000
      const alertsList = data.alerts || data || [];
      const alertsArray = Array.isArray(alertsList) ? alertsList : [];
      setAlerts(alertsArray);
      
      // Group alerts by IP
      const grouped = groupAlertsByIP(alertsArray);
      setIpGroups(grouped);
      
      
      // Calculate statistics
      const statsData = {
        total: alertsArray.length,
        critical: alertsArray.filter(a => a.score >= 0.9).length,
        high: alertsArray.filter(a => a.score >= 0.85 && a.score < 0.9).length,
        medium: alertsArray.filter(a => a.score >= 0.75 && a.score < 0.85).length,
        low: alertsArray.filter(a => a.score < 0.75).length
      };
      setStats(statsData);
    } catch (error) {
      // Silently handle connection errors (backend not running)
      if (!error.isConnectionError && error.message !== 'BACKEND_CONNECTION_ERROR') {
        console.error('Error loading alerts:', error);
      }
      // Don't clear existing data on error, just keep what we have for dynamic updates
      if (alerts.length === 0 && ipGroups.length === 0) {
        setAlerts([]);
        setIpGroups([]);
        setStats({ total: 0, critical: 0, high: 0, medium: 0, low: 0 });
      }
    } finally {
      setLoading(false);
    }
  };

  const filterAndSortIpGroups = () => {
    let filtered = [...ipGroups];

    // Filter by risk level
    if (filterRiskLevel !== 'ALL') {
      filtered = filtered.filter(group => {
        if (filterRiskLevel === 'CRITICAL') return group.maxScore >= 0.9;
        if (filterRiskLevel === 'HIGH') return group.maxScore >= 0.8 && group.maxScore < 0.9;
        if (filterRiskLevel === 'MEDIUM') return group.maxScore >= 0.6 && group.maxScore < 0.8;
        if (filterRiskLevel === 'LOW') return group.maxScore < 0.6;
        return true;
      });
    }

    // Filter by country
    if (filterCountry !== 'ALL') {
      filtered = filtered.filter(group => group.country === filterCountry);
    }

    // Sort
    if (sortBy === 'attacks') {
      filtered.sort((a, b) => b.totalAttacks - a.totalAttacks);
    } else if (sortBy === 'score') {
      filtered.sort((a, b) => b.maxScore - a.maxScore);
    } else if (sortBy === 'time') {
      filtered.sort((a, b) => new Date(b.lastSeen) - new Date(a.lastSeen));
    }

    setFilteredIpGroups(filtered);
  };

  const getRiskClass = (score) => {
    if (score >= 0.9) return 'critical';
    if (score >= 0.85) return 'high';
    if (score >= 0.75) return 'medium';
    return 'low';
  };

  const getRiskLabel = (score) => {
    if (score >= 0.9) return 'CRITICAL';
    if (score >= 0.85) return 'HIGH';
    if (score >= 0.75) return 'MEDIUM';
    return 'LOW';
  };

  const getRiskColor = (score) => {
    if (score >= 0.9) return '#ef4444';
    if (score >= 0.85) return '#f97316';
    if (score >= 0.75) return '#eab308';
    return '#3b82f6';
  };

  const handleInvestigate = (ip) => {
    navigate(`/investigate/${ip}`);
  };

  const exportAlerts = () => {
    const csv = [
      ['IP', 'Country', 'Total Attacks', 'Max Score', 'Avg Score', 'Attack Types', 'Services', 'First Seen', 'Last Seen'].join(','),
      ...filteredIpGroups.map(g => [
        g.ip,
        g.country,
        g.totalAttacks,
        g.maxScore.toFixed(4),
        g.avgScore.toFixed(4),
        g.attackTypes.join(';'),
        g.services.join(';'),
        g.firstSeen,
        g.lastSeen
      ].join(','))
    ].join('\n');

    const blob = new Blob([csv], { type: 'text/csv' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `alerts_by_ip_${new Date().toISOString().split('T')[0]}.csv`;
    a.click();
  };

  // Get unique values for filters
  const uniqueCountries = [...new Set(ipGroups.map(g => g.country))].filter(c => c && c !== 'Unknown');
  const alertStats = stats;
  const displayIpGroups = filteredIpGroups;

  // Chart data
  const riskDistributionData = {
    labels: ['CRITICAL', 'HIGH', 'MEDIUM', 'LOW'],
    datasets: [{
      data: [alertStats.critical, alertStats.high, alertStats.medium, alertStats.low],
      backgroundColor: ['#ef4444', '#f97316', '#eab308', '#3b82f6']
    }]
  };

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

  const pieOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        position: 'bottom',
        labels: { color: '#a0aec0', font: { size: 10 }, padding: 15 }
      }
    }
  };

  return (
    <div className="page-container">
      <div className="page-header">
        <h1>Security Alerts</h1>
        <div className="filters">
          <input
            type="number"
            placeholder="Threshold..."
            step="0.05"
            min="0"
            max="1"
            value={threshold}
            onChange={(e) => setThreshold(parseFloat(e.target.value) || 0.5)}
            className="filter-input"
            style={{ width: '120px' }}
          />
          <button onClick={loadAlerts} className="refresh-btn">Refresh</button>
          <button onClick={exportAlerts} className="refresh-btn" style={{ background: '#22c55e' }}>
            Export CSV
          </button>
        </div>
      </div>

      {/* Statistics Cards */}
      <div className="stats-grid" style={{ marginBottom: '20px' }}>
        <div className="stat-card">
          <h3>Total Alerts</h3>
          <div className="value" style={{ color: '#f7fafc' }}>{alertStats.total}</div>
        </div>
        <div className="stat-card" style={{ borderLeft: '4px solid #ef4444' }}>
          <h3>Critical</h3>
          <div className="value" style={{ color: '#ef4444' }}>{alertStats.critical}</div>
        </div>
        <div className="stat-card" style={{ borderLeft: '4px solid #f97316' }}>
          <h3>High Risk</h3>
          <div className="value" style={{ color: '#f97316' }}>{alertStats.high}</div>
        </div>
        <div className="stat-card" style={{ borderLeft: '4px solid #eab308' }}>
          <h3>Medium Risk</h3>
          <div className="value" style={{ color: '#eab308' }}>{alertStats.medium}</div>
        </div>
        <div className="stat-card" style={{ borderLeft: '4px solid #3b82f6' }}>
          <h3>Low Risk</h3>
          <div className="value" style={{ color: '#3b82f6' }}>{alertStats.low}</div>
        </div>
      </div>

      {/* Charts */}
      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '20px', marginBottom: '20px' }}>
        <div className="chart-container" style={{ height: '300px' }}>
          <div className="chart-title">Risk Level Distribution</div>
          <Doughnut data={riskDistributionData} options={pieOptions} />
        </div>
        <div className="chart-container" style={{ height: '300px' }}>
          <div className="chart-title">Alerts Overview</div>
          <Bar
            data={{
              labels: ['Total', 'Critical', 'High', 'Medium', 'Low'],
              datasets: [{
                label: 'Alerts',
                data: [alertStats.total, alertStats.critical, alertStats.high, alertStats.medium, alertStats.low],
                backgroundColor: ['#f7fafc', '#ef4444', '#f97316', '#eab308', '#3b82f6']
              }]
            }}
            options={chartOptions}
          />
        </div>
      </div>

      {/* Filters */}
      <div style={{ 
        background: '#1a202c', 
        borderRadius: '8px', 
        padding: '16px', 
        marginBottom: '20px',
        display: 'flex',
        gap: '12px',
        flexWrap: 'wrap',
        alignItems: 'center'
      }}>
        <div style={{ color: '#a0aec0', fontSize: '14px', fontWeight: '600' }}>Filters:</div>
        
        <select
          value={filterRiskLevel}
          onChange={(e) => setFilterRiskLevel(e.target.value)}
          className="filter-input"
          style={{ width: '150px' }}
        >
          <option value="ALL">All Risk Levels</option>
          <option value="CRITICAL">Critical</option>
          <option value="HIGH">High</option>
          <option value="MEDIUM">Medium</option>
          <option value="LOW">Low</option>
        </select>

        <select
          value={filterCountry}
          onChange={(e) => setFilterCountry(e.target.value)}
          className="filter-input"
          style={{ width: '150px' }}
        >
          <option value="ALL">All Countries</option>
          {uniqueCountries.map(country => (
            <option key={country} value={country}>{country}</option>
          ))}
        </select>

        <select
          value={sortBy}
          onChange={(e) => setSortBy(e.target.value)}
          className="filter-input"
          style={{ width: '150px' }}
        >
          <option value="attacks">Sort by Attack Count</option>
          <option value="score">Sort by Max Score</option>
          <option value="time">Sort by Last Seen</option>
        </select>

        <div style={{ marginLeft: 'auto', color: '#a0aec0', fontSize: '14px' }}>
          Showing {filteredIpGroups.length} of {ipGroups.length} IP addresses
        </div>
      </div>

      {loading && <div className="loading">Loading alerts...</div>}

      {/* IP Groups List - Grouped by IP Address */}
      <div>
        {displayIpGroups.map((group) => (
          <div 
            key={group.ip} 
            className={`alert-card ${getRiskClass(group.maxScore)}`} 
            style={{
              borderLeftWidth: '4px',
              cursor: 'pointer',
              transition: 'all 0.2s',
              marginBottom: '16px'
            }}
            onClick={() => handleInvestigate(group.ip)}
          >
            <div className="alert-header">
              <div style={{ display: 'flex', alignItems: 'center', gap: '12px', flexWrap: 'wrap' }}>
                <span className="alert-ip" style={{ fontSize: '18px', fontWeight: '700' }}>{group.ip}</span>
                <span style={{ 
                  padding: '4px 10px', 
                  background: getRiskColor(group.maxScore),
                  borderRadius: '4px',
                  fontSize: '12px',
                  fontWeight: '600',
                  color: '#fff'
                }}>
                  {getRiskLabel(group.maxScore)}
                </span>
                {group.country && group.country !== 'Unknown' && (
                  <span style={{ color: '#a0aec0', fontSize: '14px' }}>📍 {group.country}</span>
                )}
                {group.city && group.city !== 'Unknown' && (
                  <span style={{ color: '#718096', fontSize: '13px' }}>{group.city}</span>
                )}
              </div>
              <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
                <div className="alert-score" style={{ color: getRiskColor(group.maxScore), fontSize: '16px', fontWeight: '700' }}>
                  {group.maxScore.toFixed(4)}
                </div>
                <button
                  onClick={(e) => {
                    e.stopPropagation();
                    handleInvestigate(group.ip);
                  }}
                  className="refresh-btn"
                  style={{ 
                    padding: '8px 16px', 
                    fontSize: '13px',
                    background: '#4299e1',
                    fontWeight: '600'
                  }}
                >
                  Investigate
                </button>
              </div>
            </div>
            <div className="alert-details" style={{ marginTop: '16px' }}>
              {/* Aggregated Statistics */}
              <div style={{ 
                display: 'grid', 
                gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', 
                gap: '16px',
                marginBottom: '16px'
              }}>
                <div style={{ background: '#1a202c', padding: '12px', borderRadius: '6px' }}>
                  <div style={{ color: '#a0aec0', fontSize: '11px', marginBottom: '4px' }}>TOTAL ATTACKS</div>
                  <div style={{ color: '#ef4444', fontSize: '24px', fontWeight: '700' }}>{group.totalAttacks}</div>
                </div>
                <div style={{ background: '#1a202c', padding: '12px', borderRadius: '6px' }}>
                  <div style={{ color: '#a0aec0', fontSize: '11px', marginBottom: '4px' }}>MAX SCORE</div>
                  <div style={{ color: getRiskColor(group.maxScore), fontSize: '24px', fontWeight: '700' }}>
                    {group.maxScore.toFixed(4)}
                  </div>
                </div>
                <div style={{ background: '#1a202c', padding: '12px', borderRadius: '6px' }}>
                  <div style={{ color: '#a0aec0', fontSize: '11px', marginBottom: '4px' }}>AVG SCORE</div>
                  <div style={{ color: '#eab308', fontSize: '24px', fontWeight: '700' }}>
                    {group.avgScore.toFixed(4)}
                  </div>
                </div>
                <div style={{ background: '#1a202c', padding: '12px', borderRadius: '6px' }}>
                  <div style={{ color: '#a0aec0', fontSize: '11px', marginBottom: '4px' }}>ATTACK TYPES</div>
                  <div style={{ color: '#f7fafc', fontSize: '14px', fontWeight: '600' }}>
                    {group.attackTypes.length > 0 ? group.attackTypes.join(', ') : 'UNKNOWN'}
                  </div>
                </div>
              </div>

              {/* Attack Types and Services */}
              <div style={{ 
                display: 'grid', 
                gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))', 
                gap: '12px',
                marginBottom: '12px'
              }}>
                <div>
                  <strong style={{ color: '#a0aec0', fontSize: '12px' }}>Attack Types ({group.attackTypes.length}):</strong>
                  <div style={{ marginTop: '4px', display: 'flex', flexWrap: 'wrap', gap: '6px' }}>
                    {group.attackTypes.map((type, idx) => (
                      <span key={idx} style={{
                        padding: '4px 8px',
                        background: '#2d3748',
                        borderRadius: '4px',
                        fontSize: '11px',
                        color: '#ef4444'
                      }}>
                        {type}
                      </span>
                    ))}
                    {group.attackTypes.length === 0 && (
                      <span style={{ color: '#718096', fontSize: '12px' }}>No attack types detected</span>
                    )}
                  </div>
                </div>
                <div>
                  <strong style={{ color: '#a0aec0', fontSize: '12px' }}>Services Targeted ({group.services.length}):</strong>
                  <div style={{ marginTop: '4px', display: 'flex', flexWrap: 'wrap', gap: '6px' }}>
                    {group.services.map((service, idx) => (
                      <span key={idx} style={{
                        padding: '4px 8px',
                        background: '#2d3748',
                        borderRadius: '4px',
                        fontSize: '11px',
                        color: '#4299e1'
                      }}>
                        {service}
                      </span>
                    ))}
                    {group.services.length === 0 && (
                      <span style={{ color: '#718096', fontSize: '12px' }}>No services detected</span>
                    )}
                  </div>
                </div>
              </div>

              {/* Time Range */}
              <div style={{ 
                display: 'grid', 
                gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', 
                gap: '12px',
                fontSize: '12px',
                color: '#a0aec0'
              }}>
                <div>
                  <strong>First Seen:</strong> {group.firstSeen ? new Date(group.firstSeen).toLocaleString() : 'Unknown'}
                </div>
                <div>
                  <strong>Last Seen:</strong> {group.lastSeen ? new Date(group.lastSeen).toLocaleString() : 'Unknown'}
                </div>
                {group.isp && group.isp !== 'Unknown' && (
                  <div>
                    <strong>ISP:</strong> {group.isp}
                  </div>
                )}
              </div>
            </div>
          </div>
        ))}
        
        {filteredIpGroups.length === 0 && !loading && (
          <div className="no-data">
            No alerts found matching your filters
            {threshold > 0 && ` (threshold: ${threshold.toFixed(2)})`}
          </div>
        )}
      </div>
    </div>
  );
}

export default Alerts;
