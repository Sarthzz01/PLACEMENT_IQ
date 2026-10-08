import React from 'react';
import { Sparkles, Target, Award, BookOpen } from 'lucide-react';

export default function AcademicJustification({
  title,
  techniqueName,
  algorithmName,
  whyChosen,
  whyUsed,
  algorithmRationale,
  whatWeGet,
  projectOutcomes,
  institutionalImpact,
  dwmConcept,
  dwmConcepts
}) {
  const resolvedTechnique = techniqueName || algorithmName || '';

  // Process whyChosen / whyUsed / algorithmRationale
  let whyData = [];
  if (Array.isArray(whyChosen) && whyChosen.length > 0) {
    whyData = whyChosen;
  } else if (Array.isArray(whyUsed) && whyUsed.length > 0) {
    whyData = whyUsed;
  } else if (algorithmRationale) {
    whyData = [["Methodological Architecture", algorithmRationale]];
  }

  // Process whatWeGet / projectOutcomes / institutionalImpact
  let outcomesData = [];
  if (Array.isArray(whatWeGet) && whatWeGet.length > 0) {
    outcomesData = whatWeGet;
  } else if (Array.isArray(projectOutcomes) && projectOutcomes.length > 0) {
    outcomesData = projectOutcomes;
  } else if (typeof whatWeGet === 'string' && whatWeGet.trim()) {
    outcomesData = [["Placement Intelligence Deliverable", whatWeGet]];
  } else if (institutionalImpact) {
    outcomesData = [["Institutional Decision Support", institutionalImpact]];
  }

  const rawDwm = dwmConcept || dwmConcepts || '';
  const dwmTags = rawDwm ? rawDwm.split(/[,•|]+/).map(s => s.trim()).filter(Boolean) : [];

  return (
    <div className="justification-card">
      <div className="justification-header">
        <div style={{ display: 'flex', alignItems: 'center', gap: '10px', flexWrap: 'wrap' }}>
          <span className="justification-badge">
            <Sparkles size={13} /> ANALYTICAL CONCLUSION & PROJECT OUTCOMES
          </span>
          <h3 className="justification-title">{title}</h3>
        </div>
        {resolvedTechnique && <span className="justification-algo">{resolvedTechnique}</span>}
      </div>

      <div className="justification-grid">
        {/* Column 1: Why This Technique Was Selected */}
        <div className="justification-column">
          <div className="justification-col-header">
            <Target size={16} color="var(--primary)" />
            <span>Why We Use This Technique for PlacementIQ:</span>
          </div>
          <div className="justification-points">
            {whyData.map(([heading, desc], idx) => (
              <div key={idx} className="justification-point">
                <span className="justification-bullet">•</span>
                <div>
                  <strong style={{ color: 'var(--navy)' }}>{heading}: </strong>
                  <span>{desc}</span>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Column 2: What Our Project Gets By Using It */}
        <div className="justification-column">
          <div className="justification-col-header">
            <Award size={16} color="#16A34A" />
            <span>What Our Project Gets By Using This:</span>
          </div>
          <div className="justification-points">
            {outcomesData.map((item, idx) => {
              const heading = Array.isArray(item) ? item[0] : null;
              const desc = Array.isArray(item) ? item[1] : item;
              return (
                <div key={idx} className="justification-point">
                  <span className="justification-bullet" style={{ color: '#16A34A' }}>✓</span>
                  <div>
                    {heading && <strong style={{ color: 'var(--navy)' }}>{heading}: </strong>}
                    <span>{desc}</span>
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      </div>

      {institutionalImpact && outcomesData.length > 1 && (
        <div className="justification-impact-box">
          <div className="justification-impact-title">
            🏛️ Institutional Actionability & Placement Directorate Value:
          </div>
          <div className="justification-impact-body">
            {institutionalImpact}
          </div>
        </div>
      )}

      {dwmTags.length > 0 && (
        <div className="justification-concept">
          <div style={{ display: 'flex', alignItems: 'center', gap: '6px', fontWeight: 700, color: 'var(--navy)' }}>
            <BookOpen size={14} color="#64748B" />
            <span>Core DWM Foundations:</span>
          </div>
          {dwmTags.map((tag, i) => (
            <span key={i} className="justification-tag">{tag}</span>
          ))}
        </div>
      )}
    </div>
  );
}
