import React from 'react';

export default function AcademicJustification({ title, algorithmName, whyUsed, institutionalImpact, dwmConcept }) {
  return (
    <div className="justification-card">
      <div className="justification-header">
        <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
          <span className="justification-badge">PROJECT JUSTIFICATION</span>
          <h3 className="justification-title">{title}</h3>
        </div>
        <span className="justification-algo">{algorithmName}</span>
      </div>

      <div className="justification-points">
        <div style={{ fontSize: '0.86rem', fontWeight: 700, color: 'var(--primary)', textTransform: 'uppercase', letterSpacing: '0.04em', marginBottom: '4px' }}>
          Why We Use This in Placement IQ:
        </div>
        {whyUsed && whyUsed.map(([heading, desc], idx) => (
          <div key={idx} className="justification-point">
            <span style={{ color: 'var(--primary)', fontWeight: 800, fontSize: '1rem', lineHeight: '1.4' }}>•</span>
            <div>
              <strong style={{ color: 'var(--navy)' }}>{heading}: </strong>
              <span>{desc}</span>
            </div>
          </div>
        ))}
      </div>

      <div className="justification-impact-box">
        <div className="justification-impact-title">
          🏛️ Institutional Impact & Administrative Value:
        </div>
        <div className="justification-impact-body">
          {institutionalImpact}
        </div>
      </div>

      {dwmConcept && (
        <div className="justification-concept">
          <strong style={{ color: 'var(--navy)' }}>DWM Curricular Concept: </strong>
          {dwmConcept}
        </div>
      )}
    </div>
  );
}
