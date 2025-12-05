import React, { useState, useEffect } from 'react';
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

function Analytics() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [initialLoad, setInitialLoad] = useState(true);

  useEffect(() => {
    loadAnalytics();
    const interval = setInterval(loadAnalytics, 5000); // Refresh every 5 seconds for dynamic updates
    return () => clearInterval(interval);
  }, []);

  const loadAnalytics = async () => {
    try {
      // Only show loading on initial load, not on subsequent refreshes
      if (initialLoad) {
        setLoading(true);
      }
      
      const analytics = await api.getAnalytics();
      setData(analytics);
      
      if (initialLoad) {
        setInitialLoad(false);
        setLoading(false);
      }
      
      if (analytics && analytics.time_series) {
      }
    } catch (error) {
      // Silently handle connection errors (backend not running)
      if (!error.isConnectionError && error.message !== 'BACKEND_CONNECTION_ERROR') {
        console.error('Error loading analytics:', error);
      }
      
      // Set empty data structure on error
      if (!data) {
        setData({
          total_attacks: 0,
          high_risk_attacks: 0,
          unique_ips: 0,
          avg_ml_score: 0,
          top_countries: [],
          top_ports: [],
          top_ips: [],
          time_series: []
        });
      }
      
      if (initialLoad) {
        setInitialLoad(false);
        setLoading(false);
      }
    }
  };

  // Show loading only on initial load
  if (loading && initialLoad) {
    return <div className="page-container"><div className="loading">Loading analytics...</div></div>;
  }

  // If no data after initial load, show empty state but keep page visible
  if (!data) {
    return (
      <div className="page-container">
        <div className="page-header">
          <h1>Analytics</h1>
          <button onClick={loadAnalytics} className="refresh-btn">Refresh</button>
        </div>
        <div style={{ padding: '40px', textAlign: 'center', color: '#a0aec0' }}>
          No analytics data available. Waiting for data...
        </div>
      </div>
    );
  }

  // Use real data - no demo fallbacks for dynamic dashboard
  const totalAttacks = data.total_attacks || 0;
  const highRiskAttacks = data.high_risk_attacks || 0;
  const uniqueIps = data.unique_ips || 0;
  const avgMlScore = data.avg_ml_score || 0;
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
        <h1>Analytics</h1>
        <button onClick={loadAnalytics} className="refresh-btn">Refresh</button>
      </div>

      <div className="stats-grid">
        <div className="stat-card">
          <h3>Total Attacks</h3>
          <div className="value" style={{ color: '#ef4444' }}>{totalAttacks.toLocaleString()}</div>
        </div>
        <div className="stat-card">
          <h3>High-Risk Attacks</h3>
          <div className="value" style={{ color: '#f97316' }}>{highRiskAttacks.toLocaleString()}</div>
        </div>
        <div className="stat-card">
          <h3>Unique IPs</h3>
          <div className="value" style={{ color: '#4299e1' }}>{uniqueIps.toLocaleString()}</div>
        </div>
        <div className="stat-card">
          <h3>Avg ML Score</h3>
          <div className="value" style={{ color: '#eab308' }}>{avgMlScore.toFixed(4)}</div>
        </div>
      </div>

      <div className="chart-container">
        <div className="chart-title">Attacks Over Time (24h)</div>
        {data.time_series && data.time_series.length > 0 ? (() => {
          // Parse backend timestamps and create a map
          // Backend returns: 'YYYY-MM-DDTHH:00:00Z' format (UTC ISO format)
          const timeMap = {}; // Maps full timestamp string to count
          const parsedTimes = []; // Store parsed Date objects for finding latest time
          
          data.time_series.forEach(t => {
            const timeStr = t.time || '';
            if (timeStr) {
              // Store the count with the timestamp as key
              timeMap[timeStr] = t.count || 0;
              
              // Parse the timestamp (now in UTC ISO format: 'YYYY-MM-DDTHH:00:00Z')
              try {
                // Parse UTC ISO format
                const date = new Date(timeStr);
                if (!isNaN(date.getTime())) {
                  parsedTimes.push(date);
                }
              } catch (e) {
                // Ignore parsing errors
              }
            }
          });

          // Determine the reference time for the 24-hour window
          // Always use current UTC time to show live data (last 24 hours ending at CURRENT HOUR)
          // This ensures new attacks appear immediately and matches backend UTC timestamps
          const nowUTC = new Date();
          // Round down to current hour in UTC
          const currentHourUTC = nowUTC.getUTCHours();
          const currentDateUTC = new Date(Date.UTC(
            nowUTC.getUTCFullYear(),
            nowUTC.getUTCMonth(),
            nowUTC.getUTCDate(),
            currentHourUTC,
            0, 0, 0
          ));
          
          const labels = [];
          const chartData = [];
          
          // Generate 24 hours backwards from current UTC hour
          // This ensures we show the correct time range matching backend UTC data
          // Shows: [23 hours ago] ... [2 hours ago] [1 hour ago] [CURRENT HOUR]
          for (let i = 23; i >= 0; i--) {
            // Create target time in UTC by subtracting hours from current hour
            // i=23 means 23 hours ago, i=0 means current hour
            const targetTimeUTC = new Date(currentDateUTC);
            const targetHour = currentHourUTC - i;
            
            if (targetHour < 0) {
              // Previous day
              targetTimeUTC.setUTCDate(targetTimeUTC.getUTCDate() - 1);
              targetTimeUTC.setUTCHours(24 + targetHour);
            } else if (targetHour >= 24) {
              // Next day (shouldn't happen, but handle it)
              targetTimeUTC.setUTCDate(targetTimeUTC.getUTCDate() + 1);
              targetTimeUTC.setUTCHours(targetHour - 24);
            } else {
              // Same day
              targetTimeUTC.setUTCHours(targetHour);
            }
            
            // Ensure minutes/seconds are zero
            targetTimeUTC.setUTCMinutes(0);
            targetTimeUTC.setUTCSeconds(0);
            targetTimeUTC.setUTCMilliseconds(0);
            
            // Format for display: HH:00 (shows hour in local time for user readability)
            // Convert UTC to local for display
            const localTime = new Date(targetTimeUTC);
            const hourStr = `${localTime.getHours().toString().padStart(2, '0')}:00`;
            labels.push(hourStr);
            
            // Try to match backend timestamp format: 'YYYY-MM-DDTHH:00:00Z' (UTC ISO format)
            // Format the target time to match backend format exactly (in UTC)
            const year = targetTimeUTC.getUTCFullYear();
            const month = (targetTimeUTC.getUTCMonth() + 1).toString().padStart(2, '0');
            const day = targetTimeUTC.getUTCDate().toString().padStart(2, '0');
            const hour = targetTimeUTC.getUTCHours().toString().padStart(2, '0');
            const backendFormat = `${year}-${month}-${day}T${hour}:00:00Z`;
            
            // Try exact match first (most common case)
            let count = timeMap[backendFormat] || 0;
            
            // If no exact match, try to find by matching the hour and date
            // This handles any edge cases
            if (count === 0) {
              // Match by hour and same/adjacent date in UTC
              for (const [key, value] of Object.entries(timeMap)) {
                if (key.includes(`T${hour}:00:00Z`)) {
                  const backendDate = key.split('T')[0];
                  const targetDate = `${year}-${month}-${day}`;
                  
                  // Calculate day difference
                  const backendDateObj = new Date(backendDate + 'T00:00:00Z');
                  const targetDateObj = new Date(targetDate + 'T00:00:00Z');
                  const dayDiff = Math.abs(backendDateObj - targetDateObj) / (1000 * 60 * 60 * 24);
                  
                  // Allow same day or adjacent day
                  if (dayDiff < 2) {
                    count = value;
                    break;
                  }
                }
              }
            }
            
            // Debug: log current hour matching
            if (i === 0 && process.env.NODE_ENV === 'development') {
            }
            
            chartData.push(count);
          }
          
          // Debug: log the time range being displayed (only in development)
          if (process.env.NODE_ENV === 'development') {
            const totalDataPoints = chartData.filter(c => c > 0).length;
            if (totalDataPoints > 0) {
            }
          }

          return (
            <Line
              key={`time-series-${data.time_series.length}`}
              data={{
                labels: labels,
                datasets: [{
                  label: 'Attacks',
                  data: chartData,
                  borderColor: '#4299e1',
                  backgroundColor: 'rgba(66, 153, 225, 0.1)',
                  tension: 0.4,
                  fill: true,
                  pointRadius: 3,
                  pointHoverRadius: 5,
                  pointBackgroundColor: '#4299e1',
                  pointBorderColor: '#ffffff',
                  pointBorderWidth: 2
                }]
              }}
              options={{
                ...chartOptions,
                animation: {
                  duration: 300 // Quick animation for smooth updates
                },
                plugins: {
                  ...chartOptions.plugins,
                  tooltip: {
                    enabled: true,
                    mode: 'index',
                    intersect: false,
                    callbacks: {
                      label: function(context) {
                        return `Attacks: ${context.parsed.y}`;
                      }
                    }
                  }
                },
                scales: {
                  ...chartOptions.scales,
                  x: {
                    ...chartOptions.scales.x,
                    ticks: {
                      ...chartOptions.scales.x.ticks,
                      maxRotation: 45,
                      minRotation: 0,
                      autoSkip: true,
                      maxTicksLimit: 12
                    }
                  },
                  y: {
                    ...chartOptions.scales.y,
                    beginAtZero: true,
                    ticks: {
                      ...chartOptions.scales.y.ticks,
                      stepSize: Math.max(1, Math.ceil(Math.max(...chartData, 1) / 10))
                    }
                  }
                }
              }}
            />
          );
        })() : (
          <div style={{ padding: '40px', textAlign: 'center', color: '#a0aec0' }}>
            No time series data available
          </div>
        )}
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '20px' }}>
        <div className="chart-container">
          <div className="chart-title">Top Countries</div>
          <Bar
            data={{
              labels: (data.top_countries && data.top_countries.length > 0
                ? data.top_countries.map(c => c.country)
                : []),
              datasets: [{
                label: 'Attacks',
                data: (data.top_countries && data.top_countries.length > 0
                  ? data.top_countries.map(c => c.count || 0)
                  : []),
                backgroundColor: '#4299e1'
              }]
            }}
            options={chartOptions}
          />
        </div>

        <div className="chart-container">
          <div className="chart-title">Top IPs</div>
          <Bar
            data={{
              labels: (data.top_ips && data.top_ips.length > 0
                ? data.top_ips.map(ip => ip.ip.substring(0, 15) + (ip.ip.length > 15 ? '...' : ''))
                : []),
              datasets: [{
                label: 'Attacks',
                data: (data.top_ips && data.top_ips.length > 0
                  ? data.top_ips.map(ip => ip.count || 0)
                  : []),
                backgroundColor: '#ef4444'
              }]
            }}
            options={chartOptions}
          />
        </div>
      </div>

      <div className="chart-container">
        <div className="chart-title">Top Protocols</div>
        <Doughnut
          data={{
              labels: (data.top_ports && data.top_ports.length > 0
                ? data.top_ports.map(p => p.port || 'Unknown')
                : []),
            datasets: [{
                data: (data.top_ports && data.top_ports.length > 0
                  ? data.top_ports.map(p => p.count || 0)
                  : []),
              backgroundColor: ['#ef4444', '#f97316', '#eab308', '#22c55e', '#4299e1', '#8b5cf6']
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
  );
}

export default Analytics;

