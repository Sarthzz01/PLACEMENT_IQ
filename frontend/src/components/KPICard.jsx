import React from 'react';

export default function KPICard({ title, value, subtitle, icon, iconColor = 'blue' }) {
  return (
    <div className="kpi-card">
      <div className={`kpi-icon-box kpi-icon-${iconColor}`}>
        {icon}
      </div>
      <div>
        <div className="kpi-title">{title}</div>
        <div className="kpi-value">{value}</div>
        {subtitle && <div className="kpi-subtitle">{subtitle}</div>}
      </div>
    </div>
  );
}
