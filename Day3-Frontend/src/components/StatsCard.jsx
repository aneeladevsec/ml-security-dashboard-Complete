import React from 'react';
import './StatsCard.css';

function StatsCard({ title, value, icon, danger }) {
  return (
    <div className={`stat-card ${danger ? 'danger' : ''}`}>
      <div className="stat-icon">{icon}</div>
      <div className="stat-content">
        <h3>{title}</h3>
        <p className="stat-value">{value}</p>
      </div>
    </div>
  );
}

export default StatsCard;
