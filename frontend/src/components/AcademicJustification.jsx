import React, { useState } from 'react';
import {
  Sparkles, Target, Award, BookOpen, ChevronDown, ChevronUp,
  CheckCircle2, Compass
} from 'lucide-react';

// Extract first punchy sentence for concise executive conclusions
const extractShortSentence = (text) => {
  if (!text) return '';
  const clean = String(text).trim();
  const match = clean.match(/^([^\.\!\?]+[\.\!\?])/);
  if (match && match[1] && match[1].length > 20) {
    return match[1];
  }
  return clean.length > 160 ? `${clean.slice(0, 157)}...` : clean;
};

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
  const [expanded, setExpanded] = useState(false);
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

  // Short primary bullet points for minimized view
  const primaryWhy = whyData.length > 0 ? whyData[0] : null;
  const primaryOutcome = outcomesData.length > 0 ? outcomesData[0] : null;

  return (
    <div className="justification-card" style={{
      background: '#FFFFFF',
      border: '1px solid #E2E8F0',
      borderTop: '3px solid var(--primary)',
      borderRadius: 10,
      padding: '16px 20px',
      marginTop: '24px',
      marginBottom: '20px',
      boxShadow: '0 1px 3px rgba(0,0,0,0.05)'
    }}>
      {/* Top Header Row */}
      <div style={{
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'space-between',
        flexWrap: 'wrap',
        gap: 10,
        marginBottom: 12,
        paddingBottom: 10,
        borderBottom: '1px solid #F1F5F9'
      }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: 10, flexWrap: 'wrap' }}>
          <span style={{
            background: '#EFF6FF',
            color: '#1D4ED8',
            fontSize: '0.72rem',
            fontWeight: 800,
            textTransform: 'uppercase',
            letterSpacing: '0.04em',
            padding: '3px 8px',
            borderRadius: 6,
            display: 'inline-flex',
            alignItems: 'center',
            gap: 5,
            border: '1px solid #BFDBFE'
          }}>
            <Sparkles size={12} color="#2563EB" /> Page Conclusion
          </span>

          <h4 style={{
            fontSize: '0.98rem',
            fontWeight: 800,
            color: 'var(--navy)',
            margin: 0
          }}>
            {title ? title.split(':')[0] : 'Analytical Summary'}
          </h4>
        </div>

        <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
          {resolvedTechnique && (
            <span style={{
              fontSize: '0.75rem',
              color: '#475569',
              background: '#F1F5F9',
              padding: '3px 10px',
              borderRadius: 20,
              border: '1px solid #E2E8F0',
              fontWeight: 600
            }}>
              {resolvedTechnique}
            </span>
          )}

          <button
            type="button"
            onClick={() => setExpanded(!expanded)}
            style={{
              background: '#FFFFFF',
              border: '1px solid #CBD5E1',
              borderRadius: 20,
              padding: '3px 10px',
              fontSize: '0.74rem',
              fontWeight: 700,
              color: 'var(--navy)',
              cursor: 'pointer',
              display: 'inline-flex',
              alignItems: 'center',
              gap: 4,
              transition: 'all 0.15s ease'
            }}
          >
            {expanded ? <ChevronUp size={13} /> : <ChevronDown size={13} />}
            {expanded ? 'Collapse Summary' : 'Full Academic Details'}
          </button>
        </div>
      </div>

      {/* ============================================================== */}
      {/* 1. DEFAULT MINIMIZED CONCLUSION VIEW                            */}
      {/* ============================================================== */}
      {!expanded ? (
        <div>
          <div style={{
            display: 'grid',
            gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))',
            gap: 12,
            marginBottom: 10
          }}>
            {/* Short Point 1: Core Methodology */}
            {primaryWhy && (
              <div style={{
                background: '#F8FAFC',
                border: '1px solid #E2E8F0',
                borderRadius: 8,
                padding: '10px 14px',
                fontSize: '0.82rem'
              }}>
                <div style={{
                  display: 'flex',
                  alignItems: 'center',
                  gap: 6,
                  fontWeight: 800,
                  color: 'var(--primary)',
                  marginBottom: 4,
                  fontSize: '0.75rem',
                  textTransform: 'uppercase'
                }}>
                  <Target size={13} /> Why This Technique:
                </div>
                <div style={{ color: 'var(--text-body)', lineHeight: 1.5 }}>
                  <strong style={{ color: 'var(--navy)' }}>{primaryWhy[0]}: </strong>
                  <span>{extractShortSentence(primaryWhy[1])}</span>
                </div>
              </div>
            )}

            {/* Short Point 2: Core Deliverable */}
            {primaryOutcome && (
              <div style={{
                background: '#F0FDF4',
                border: '1px solid #BBF7D0',
                borderRadius: 8,
                padding: '10px 14px',
                fontSize: '0.82rem'
              }}>
                <div style={{
                  display: 'flex',
                  alignItems: 'center',
                  gap: 6,
                  fontWeight: 800,
                  color: '#166534',
                  marginBottom: 4,
                  fontSize: '0.75rem',
                  textTransform: 'uppercase'
                }}>
                  <Award size={13} /> Key Deliverable:
                </div>
                <div style={{ color: '#14532D', lineHeight: 1.5 }}>
                  <strong style={{ color: '#166534' }}>{Array.isArray(primaryOutcome) ? primaryOutcome[0] : 'Outcome'}: </strong>
                  <span>{extractShortSentence(Array.isArray(primaryOutcome) ? primaryOutcome[1] : primaryOutcome)}</span>
                </div>
              </div>
            )}
          </div>

          {/* Institutional Bottom Banner */}
          {institutionalImpact && (
            <div style={{
              background: '#F8FAFC',
              borderLeft: '3px solid var(--primary)',
              borderRadius: 4,
              padding: '8px 12px',
              fontSize: '0.8rem',
              color: 'var(--text-body)',
              lineHeight: 1.5,
              display: 'flex',
              alignItems: 'center',
              gap: 8
            }}>
              <CheckCircle2 size={15} color="var(--primary)" style={{ flexShrink: 0 }} />
              <div>
                <strong style={{ color: 'var(--navy)' }}>Institutional Takeaway: </strong>
                <span>{extractShortSentence(institutionalImpact)}</span>
              </div>
            </div>
          )}

          {/* DWM Tags Row */}
          {dwmTags.length > 0 && (
            <div style={{
              display: 'flex',
              alignItems: 'center',
              gap: 6,
              flexWrap: 'wrap',
              marginTop: 10,
              paddingTop: 8,
              borderTop: '1px solid #F1F5F9'
            }}>
              <span style={{ fontSize: '0.72rem', fontWeight: 700, color: 'var(--text-muted)' }}>Foundations:</span>
              {dwmTags.slice(0, 4).map((tag, i) => (
                <span
                  key={i}
                  style={{
                    background: '#F1F5F9',
                    color: '#475569',
                    fontSize: '0.72rem',
                    fontWeight: 600,
                    padding: '2px 8px',
                    borderRadius: 4
                  }}
                >
                  {tag}
                </span>
              ))}
            </div>
          )}
        </div>
      ) : (
        /* ============================================================== */
        /* 2. FULL EXPANDED ACADEMIC VIVA VIEW                            */
        /* ============================================================== */
        <div>
          <div style={{
            display: 'grid',
            gridTemplateColumns: 'repeat(auto-fit, minmax(340px, 1fr))',
            gap: 16,
            marginBottom: 16
          }}>
            {/* Column 1: Detailed Why */}
            <div style={{
              background: '#F8FAFC',
              border: '1px solid #E2E8F0',
              borderRadius: 8,
              padding: '14px 16px'
            }}>
              <div style={{
                display: 'flex',
                alignItems: 'center',
                gap: 6,
                fontSize: '0.8rem',
                fontWeight: 800,
                color: 'var(--navy)',
                textTransform: 'uppercase',
                marginBottom: 10,
                paddingBottom: 6,
                borderBottom: '1px solid #E2E8F0'
              }}>
                <Target size={15} color="var(--primary)" />
                Why We Use This Technique for PlacementIQ:
              </div>
              <div style={{ display: 'flex', flexDirection: 'column', gap: 10 }}>
                {whyData.map(([heading, desc], idx) => (
                  <div key={idx} style={{ fontSize: '0.84rem', lineHeight: 1.55 }}>
                    <strong style={{ color: 'var(--navy)' }}>• {heading}: </strong>
                    <span style={{ color: 'var(--text-body)' }}>{desc}</span>
                  </div>
                ))}
              </div>
            </div>

            {/* Column 2: Detailed What */}
            <div style={{
              background: '#F0FDF4',
              border: '1px solid #BBF7D0',
              borderRadius: 8,
              padding: '14px 16px'
            }}>
              <div style={{
                display: 'flex',
                alignItems: 'center',
                gap: 6,
                fontSize: '0.8rem',
                fontWeight: 800,
                color: '#166534',
                textTransform: 'uppercase',
                marginBottom: 10,
                paddingBottom: 6,
                borderBottom: '1px solid #BBF7D0'
              }}>
                <Award size={15} color="#16A34A" />
                What Our Project Gets By Using This:
              </div>
              <div style={{ display: 'flex', flexDirection: 'column', gap: 10 }}>
                {outcomesData.map((item, idx) => {
                  const heading = Array.isArray(item) ? item[0] : null;
                  const desc = Array.isArray(item) ? item[1] : item;
                  return (
                    <div key={idx} style={{ fontSize: '0.84rem', lineHeight: 1.55 }}>
                      <strong style={{ color: '#166534' }}>✓ {heading ? `${heading}: ` : ''}</strong>
                      <span style={{ color: '#14532D' }}>{desc}</span>
                    </div>
                  );
                })}
              </div>
            </div>
          </div>

          {institutionalImpact && (
            <div style={{
              background: '#F0FDF4',
              borderLeft: '4px solid #16A34A',
              padding: '12px 16px',
              borderRadius: 6,
              fontSize: '0.84rem',
              color: '#14532D',
              lineHeight: 1.6,
              marginBottom: 12
            }}>
              <strong style={{ color: '#166534', display: 'block', marginBottom: 2 }}>
                🏛️ Institutional Actionability & Placement Directorate Value:
              </strong>
              {institutionalImpact}
            </div>
          )}

          {dwmTags.length > 0 && (
            <div style={{
              display: 'flex',
              alignItems: 'center',
              gap: 6,
              flexWrap: 'wrap',
              paddingTop: 10,
              borderTop: '1px solid #E2E8F0'
            }}>
              <span style={{ fontSize: '0.78rem', fontWeight: 700, color: 'var(--navy)' }}>Core Foundations:</span>
              {dwmTags.map((tag, i) => (
                <span
                  key={i}
                  style={{
                    background: '#F1F5F9',
                    color: '#334155',
                    fontSize: '0.75rem',
                    fontWeight: 600,
                    padding: '3px 9px',
                    borderRadius: 4
                  }}
                >
                  {tag}
                </span>
              ))}
            </div>
          )}
        </div>
      )}
    </div>
  );
}
