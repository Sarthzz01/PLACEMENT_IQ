import React, { useEffect, useState } from 'react';
import { Database, Table, Play, RefreshCw, Key, Layers, CheckCircle2 } from 'lucide-react';
import AcademicJustification from '../../components/AcademicJustification';

export default function DataWarehouse() {
  const [info, setInfo] = useState(null);
  const [selectedTable, setSelectedTable] = useState('FactPlacement');
  const [sampleRows, setSampleRows] = useState([]);
  const [sql, setSql] = useState(`SELECT d.branch, p.placement_status, 
       ROUND(AVG(f.cgpa), 2) AS avg_cgpa, 
       ROUND(AVG(f.coding_skill_score), 2) AS avg_coding,
       COUNT(*) AS total_students
FROM FactPlacement f
JOIN DimStudent d ON f.student_key = d.student_key
JOIN DimPlacement p ON f.student_key = p.student_key
GROUP BY d.branch, p.placement_status
ORDER BY d.branch;`);
  const [sqlResults, setSqlResults] = useState(null);
  const [sqlError, setSqlError] = useState('');
  const [loading, setLoading] = useState(true);
  const [rebuilding, setRebuilding] = useState(false);
  const [rebuildMsg, setRebuildMsg] = useState('');

  useEffect(() => {
    fetch('/api/admin/warehouse')
      .then(r => r.json())
      .then(d => {
        setInfo(d);
        setLoading(false);
      })
      .catch(() => setLoading(false));
  }, []);

  useEffect(() => {
    if (!selectedTable) return;
    fetch(`/api/admin/warehouse/sample/${selectedTable}`)
      .then(r => r.json())
      .then(d => setSampleRows(d.records || []))
      .catch(console.error);
  }, [selectedTable]);

  const handleRunSQL = async () => {
    setSqlError('');
    try {
      const res = await fetch('/api/admin/warehouse/query', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ sql })
      });
      const data = await res.json();
      if (!res.ok) throw new Error(data.detail || 'SQL Error');
      setSqlResults(data.rows || []);
    } catch (err) {
      setSqlError(err.message);
    }
  };

  const handleRebuild = async () => {
    setRebuilding(true);
    setRebuildMsg('');
    try {
      const res = await fetch('/api/admin/warehouse/rebuild', { method: 'POST' });
      const data = await res.json();
      setRebuildMsg(data.message || 'Data warehouse rebuilt successfully.');
      setTimeout(() => setRebuildMsg(''), 4000);
    } catch (err) {
      console.error(err);
    } finally {
      setRebuilding(false);
    }
  };

  if (loading) return <div style={{ padding: '40px', color: '#64748B' }}>Loading data warehouse catalog...</div>;

  const tableList = info?.schema_def ? Object.keys(info.schema_def) : ['FactPlacement', 'DimStudent', 'DimAcademic', 'DimSkills', 'DimEngagement', 'DimPlacement'];

  return (
    <div>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '24px', flexWrap: 'wrap', gap: '12px' }}>
        <div>
          <h2 style={{ fontSize: '1.6rem', fontWeight: 800, color: 'var(--navy)' }}>Star-Schema Data Warehouse</h2>
          <p style={{ color: 'var(--text-muted)', fontSize: '0.92rem' }}>
            Relational dimensional modeling decoupling operational student records from high-throughput analytical OLAP cubes.
          </p>
        </div>
        <button className="btn btn-secondary" onClick={handleRebuild} disabled={rebuilding}>
          <RefreshCw size={16} className={rebuilding ? 'animate-spin' : ''} /> {rebuilding ? 'Rebuilding...' : 'Force Rebuild Warehouse'}
        </button>
      </div>

      {rebuildMsg && (
        <div style={{ background: '#F0FDF4', color: '#16A34A', border: '1px solid #86EFAC', padding: '12px 18px', borderRadius: '10px', marginBottom: '20px', display: 'flex', alignItems: 'center', gap: '8px' }}>
          <CheckCircle2 size={18} /> {rebuildMsg}
        </div>
      )}

      {/* Star Schema Architecture Visualization Card */}
      <div className="campus-card" style={{ marginBottom: '24px' }}>
        <div className="campus-card-header">
          <div className="card-title">Star Schema Visual Topology</div>
          <span className="badge badge-role">SQLite Data Warehouse</span>
        </div>

        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '14px', marginBottom: '18px' }}>
          <div style={{ background: '#EFF6FF', border: '1px solid #BFDBFE', borderRadius: '10px', padding: '14px' }}>
            <strong style={{ color: 'var(--primary)', fontSize: '0.9rem' }}>DimStudent</strong>
            <div style={{ fontSize: '0.78rem', color: '#64748B', marginTop: '4px' }}>student_key (PK), age, gender, branch</div>
          </div>
          <div style={{ background: '#EFF6FF', border: '1px solid #BFDBFE', borderRadius: '10px', padding: '14px' }}>
            <strong style={{ color: 'var(--primary)', fontSize: '0.9rem' }}>DimAcademic</strong>
            <div style={{ fontSize: '0.78rem', color: '#64748B', marginTop: '4px' }}>student_key (PK), cgpa, backlogs, attendance</div>
          </div>
          <div style={{ background: '#EFF6FF', border: '1px solid #BFDBFE', borderRadius: '10px', padding: '14px' }}>
            <strong style={{ color: 'var(--primary)', fontSize: '0.9rem' }}>DimSkills</strong>
            <div style={{ fontSize: '0.78rem', color: '#64748B', marginTop: '4px' }}>student_key (PK), dsa, leetcode, coding, aptitude</div>
          </div>
          <div style={{ background: '#EFF6FF', border: '1px solid #BFDBFE', borderRadius: '10px', padding: '14px' }}>
            <strong style={{ color: 'var(--primary)', fontSize: '0.9rem' }}>DimEngagement</strong>
            <div style={{ fontSize: '0.78rem', color: '#64748B', marginTop: '4px' }}>student_key (PK), internships, projects, repos</div>
          </div>
        </div>

        <div style={{ textAlign: 'center', margin: '8px 0' }}>
          <div style={{ display: 'inline-block', background: '#0F172A', color: '#FFFFFF', borderRadius: '12px', padding: '18px 36px', boxShadow: 'var(--shadow-md)' }}>
            <div style={{ fontSize: '0.74rem', textTransform: 'uppercase', letterSpacing: '0.08em', color: '#60A5FA', fontWeight: 800 }}>
              CENTRAL FACT TABLE
            </div>
            <div style={{ fontSize: '1.4rem', fontWeight: 900, margin: '4px 0' }}>FactPlacement</div>
            <div style={{ fontSize: '0.8rem', color: '#CBD5E1' }}>
              fact_id (PK) • student_key (FK) • cgpa • attendance • aptitude • coding • internships • projects • placement_prediction
            </div>
          </div>
        </div>
      </div>

      {/* Interactive Table Browser */}
      <div className="campus-card">
        <div className="campus-card-header">
          <div className="card-title">Interactive Warehouse Table Inspector</div>
          <div style={{ display: 'flex', gap: '8px' }}>
            {tableList.map(t => (
              <button
                key={t}
                className={`btn ${selectedTable === t ? 'btn-primary' : 'btn-secondary'}`}
                style={{ fontSize: '0.8rem', padding: '6px 12px' }}
                onClick={() => setSelectedTable(t)}
              >
                {t}
              </button>
            ))}
          </div>
        </div>

        {sampleRows.length > 0 ? (
          <div className="table-container">
            <table className="data-table">
              <thead>
                <tr>
                  {Object.keys(sampleRows[0]).map(col => (
                    <th key={col}>{col}</th>
                  ))}
                </tr>
              </thead>
              <tbody>
                {sampleRows.map((row, i) => (
                  <tr key={i}>
                    {Object.values(row).map((val, j) => (
                      <td key={j}>{String(val)}</td>
                    ))}
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        ) : (
          <div style={{ padding: '20px', color: '#64748B', textAlign: 'center' }}>No sample records found.</div>
        )}
      </div>

      {/* SQL Workbench */}
      <div className="campus-card">
        <div className="campus-card-header">
          <div className="card-title">Live SQL Analytics Workbench</div>
          <button className="btn btn-primary" onClick={handleRunSQL}>
            <Play size={16} /> Run SQL Query
          </button>
        </div>

        <div className="form-group">
          <textarea
            className="form-textarea"
            rows={5}
            style={{ fontFamily: 'monospace', fontSize: '0.88rem' }}
            value={sql}
            onChange={e => setSql(e.target.value)}
          />
        </div>

        {sqlError && (
          <div style={{ background: '#FEF2F2', color: '#DC2626', padding: '10px 14px', borderRadius: '8px', fontSize: '0.85rem', marginBottom: '16px' }}>
            SQL Error: {sqlError}
          </div>
        )}

        {sqlResults && (
          <div>
            <div style={{ fontWeight: 600, fontSize: '0.88rem', marginBottom: '8px', color: '#0F172A' }}>
              Query returned {sqlResults.length} records:
            </div>
            <div className="table-container">
              <table className="data-table">
                <thead>
                  {sqlResults.length > 0 && (
                    <tr>
                      {Object.keys(sqlResults[0]).map(k => (
                        <th key={k}>{k}</th>
                      ))}
                    </tr>
                  )}
                </thead>
                <tbody>
                  {sqlResults.map((r, i) => (
                    <tr key={i}>
                      {Object.values(r).map((v, j) => (
                        <td key={j}>{String(v)}</td>
                      ))}
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        )}
      </div>

      {/* Academic Justification */}
      <AcademicJustification
        title="Star Schema Dimensional Modeling & Analytical Federation"
        algorithmName="Star Schema Architecture • FactPlacement • Conformed Dimensions"
        whyUsed={[
          ["Analytical Read Optimization over Normalized 3NF", "Operational relational databases (OLTP) employ highly normalized 3rd Normal Form (3NF) to guarantee transactional integrity during student registration. However, running aggregate analytical queries across 3NF tables necessitates extensive, expensive multi-table joins. The Star Schema de-normalizes conformed dimensions around a centralized FactPlacement table, drastically minimizing join depth and accelerating analytical aggregation speed."],
          ["Conformed Dimensional Integrity Across Campus", "Conformed dimensions (DimStudent, DimAcademic, DimSkills, DimEngagement, DimPlacement) standardize attribute hierarchies across campus departments. This ensures complete semantic consistency—meaning 'Placement Status' or 'CGPA Tier' represents the exact same calculation whether queried by the Career Office, Academic Deans, or Machine Learning pipelines."],
          ["Decoupling Operational Transactions from Analytical Pipelines", "By persisting processed and validated candidate records in a dedicated analytical warehouse (placement_dw.sqlite), real-time student profile updates are fully isolated from intensive predictive analytics, OLAP cube slicing, and model training jobs, preventing operational database locking."]
        ]}
        institutionalImpact="Provides university administrators with an authoritative single source of truth for institutional placement metrics, enabling instant generation of regulatory compliance reports (e.g. NAAC, NBA, NIRF) without impacting live student registration systems."
        dwmConcept="Dimensional Modeling, Star Schema, Fact Table (Grain & Additive Measures), Conformed Dimensions, Surrogate Keys, Data Mart Federation."
      />
    </div>
  );
}
