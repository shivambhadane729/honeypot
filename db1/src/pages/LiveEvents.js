import React, { useState, useEffect } from 'react';
import { api } from '../api';
import './Pages.css';

function LiveEvents() {
  const [events, setEvents] = useState([]);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState({ sourceIp: '', minScore: '' });

  useEffect(() => {
    loadEvents();
    const interval = setInterval(loadEvents, 5000); // Refresh every 5 seconds
    return () => clearInterval(interval);
  }, []); // Remove filter dependency to avoid infinite loops

  const loadEvents = async () => {
    try {
      setLoading(true);
      const data = await api.getLiveEvents(
        100, // Increased limit
        filter.sourceIp || null,
        filter.minScore ? parseFloat(filter.minScore) : null
      );
      const eventsList = data.events || data || [];
      setEvents(Array.isArray(eventsList) ? eventsList : []);
      if (eventsList.length > 0) {
      }
    } catch (error) {
      // Silently handle connection errors (backend not running)
      if (error.isConnectionError || error.message === 'BACKEND_CONNECTION_ERROR') {
        // Don't log connection errors to console
        setEvents([]);
      } else {
        console.error('Error loading events:', error);
        setEvents([]);
      }
    } finally {
      setLoading(false);
    }
  };

  const getRiskColor = (score, isAnomaly) => {
    if (isAnomaly || score >= 0.8) return '#ef4444'; // Red
    if (score >= 0.6) return '#f97316'; // Orange
    if (score >= 0.4) return '#eab308'; // Yellow
    return '#22c55e'; // Green
  };

  const getRiskBadge = (score, isAnomaly) => {
    if (isAnomaly || score >= 0.8) return 'HIGH';
    if (score >= 0.6) return 'MEDIUM';
    if (score >= 0.4) return 'LOW';
    return 'MINIMAL';
  };

  return (
    <div className="page-container">
      <div className="page-header">
        <h1>Live Events</h1>
        <div className="filters">
          <input
            type="text"
            placeholder="Filter by IP..."
            value={filter.sourceIp}
            onChange={(e) => setFilter({ ...filter, sourceIp: e.target.value })}
            className="filter-input"
          />
          <input
            type="number"
            placeholder="Min ML Score..."
            step="0.1"
            min="0"
            max="1"
            value={filter.minScore}
            onChange={(e) => setFilter({ ...filter, minScore: e.target.value })}
            className="filter-input"
          />
          <button onClick={loadEvents} className="refresh-btn">Refresh</button>
        </div>
      </div>

      {loading && <div className="loading">Loading events...</div>}

      <div className="events-table-container">
        <table className="events-table">
          <thead>
            <tr>
              <th>Time</th>
              <th>IP</th>
              <th>Country</th>
              <th>Protocol</th>
              <th>Service</th>
              <th>Action</th>
              <th>ML Score</th>
              <th>Status</th>
            </tr>
          </thead>
          <tbody>
            {events.map((event) => (
              <tr key={event.id}>
                <td>{new Date(event.time).toLocaleString()}</td>
                <td className="ip-cell">{event.ip}</td>
                <td>{event.country}</td>
                <td>{event.protocol}</td>
                <td>{event.service}</td>
                <td>{event.action}</td>
                <td>
                  <span style={{ 
                    color: getRiskColor(event.ml_score || 0, event.is_anomaly),
                    fontWeight: (event.ml_score || 0) >= 0.6 ? 'bold' : 'normal'
                  }}>
                    {(event.ml_score || 0).toFixed(4)}
                  </span>
                </td>
                <td>
                  <span style={{ 
                    color: getRiskColor(event.ml_score || 0, event.is_anomaly),
                    fontWeight: '600'
                  }}>
                    {getRiskBadge(event.ml_score || 0, event.is_anomaly)}
                  </span>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
        {events.length === 0 && !loading && (
          <div className="no-data">No events found</div>
        )}
      </div>
    </div>
  );
}

export default LiveEvents;

