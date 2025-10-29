import React from 'react';
import './StatsCard.css';

function StatsCard({ title, value, icon, color = '#4ecdc4' }) {
  return (
    <div className="stats-card" style={{ borderLeftColor: color }}>
      <div className="stats-icon">{icon}</div>
      <div className="stats-content">
        <h3>{title}</h3>
        <p className="stats-value">{value}</p>
      </div>
    </div>
  );
}

export default StatsCard;
