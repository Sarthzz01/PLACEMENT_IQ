import React, { useEffect, useState } from 'react';
import { Layers, Play, Download, History, Filter, ArrowRight, ArrowLeftRight, CheckSquare, Square, BarChart3 } from 'lucide-react';
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, CartesianGrid, Legend } from 'recharts';
import AcademicJustification from '../../components/AcademicJustification';

const DEFAULT_DIMENSIONS = [
  'branch', 'gender', 'placement_training', 'placement_status',
  'cgpa_band', 'aptitude_band', 'attendance_band', 'coding_band',
  'internship_band', 'projects_band', 'backlog_band'
];

const DEFAULT_MEASURES = [
  'cgpa', 'attendance_percentage', 'dsa_questions_solved',
  'aptitude_score', 'coding_skill_score', 'mock_interview_score',
  'projects_count', 'internships_count', 'placement_prediction'
];

const DEFAULT_DIM_LABELS = {
  branch: 'Engineering Branch',
  gender: 'Gender',
  placement_training: 'Placement Training',
  placement_status: 'Placement Status',
  cgpa_band: 'CGPA Band',
  aptitude_band: 'Aptitude Band',
  attendance_band: 'Attendance Band',
  coding_band: 'Coding Skill Band',
  internship_band: 'Internship Band',
  projects_band: 'Projects Band',
  backlog_band: 'Active Backlog Band'
};

const DEFAULT_MEASURE_LABELS = {
  cgpa: 'Cumulative CGPA',
  attendance_percentage: 'Classroom Attendance %',
  dsa_questions_solved: 'DSA Questions Solved',
  aptitude_score: 'Quantitative Aptitude Score',
  coding_skill_score: 'Coding Skill Score (1-10)',
  mock_interview_score: 'Mock Interview Score (1-10)',
  projects_count: 'Technical Projects Count',
  internships_count: 'Internships Completed',
  placement_prediction: 'Placement Conversion Rate'
};

const CHART_COLORS = ['#2563EB', '#16A34A', '#F59E0B', '#9333EA', '#06B6D4', '#EC4899', '#64748B'];

export default function OLAPAnalytics() {
  const [activeTab, setActiveTab] = useState('slice');
  const [meta, setMeta] = useState(null);
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [history, setHistory] = useState([]);

  // Shared measure & aggregation
  const [measure, setMeasure] = useState('cgpa');
  const [aggFunc, setAggFunc] = useState('Average');

  // Slice state
  const [sliceDim, setSliceDim] = useState('branch');
  const [sliceVal, setSliceVal] = useState('CSE');
  const [sliceBreakdown, setSliceBreakdown] = useState('gender');

  // Dice state
  const [diceBranch, setDiceBranch] = useState('All');
  const [diceGender, setDiceGender] = useState('All');
  const [diceStatus, setDiceStatus] = useState('Placed');
  const [diceTraining, setDiceTraining] = useState('All');
  const [diceRowDim, setDiceRowDim] = useState('branch');
  const [diceColDim, setDiceColDim] = useState('gender');

  // Roll-up state
  const [rollupRowDetailed, setRollupRowDetailed] = useState('branch');
  const [rollupRowSub, setRollupRowSub] = useState('gender');
  const [rollupCol, setRollupCol] = useState('placement_status');

  // Drill-down state
  const [drillRowSummary, setDrillRowSummary] = useState('branch');
  const [drillRowDetail, setDrillRowDetail] = useState('gender');
  const [drillCol, setDrillCol] = useState('placement_status');

  // Pivot state
  const [pivotRow, setPivotRow] = useState('branch');
  const [pivotCol, setPivotCol] = useState('placement_status');

  // Drill-across state
  const [drillAcrossDim, setDrillAcrossDim] = useState('branch');
  const [selectedMeasures, setSelectedMeasures] = useState(['cgpa', 'aptitude_score', 'coding_skill_score', 'placement_prediction']);

  const loadHistory = () => {
    fetch('/api/admin/olap/history')
      .then(r => r.json())
      .then(d => setHistory(d.history || []))
      .catch(console.error);
  };

  useEffect(() => {
    fetch('/api/admin/olap/meta')
      .then(r => r.json())
      .then(d => {
        setMeta(d);
        if (d.dimension_values?.branch?.length > 0) {
          setSliceVal(d.dimension_values.branch[0]);
        }
      })
      .catch(console.error);

    loadHistory();
  }, []);

  // When sliceDim changes, automatically update sliceVal to the first valid distinct value
  useEffect(() => {
    if (meta?.dimension_values?.[sliceDim]?.length > 0) {
      setSliceVal(meta.dimension_values[sliceDim][0]);
    }
  }, [sliceDim, meta]);

  const dimensions = meta?.dimensions || DEFAULT_DIMENSIONS;
  const measures = meta?.measures || DEFAULT_MEASURES;
  const aggregations = ['Average', 'Count', 'Sum', 'Min', 'Max', 'Median'];
  const dimLabels = meta?.dim_labels || DEFAULT_DIM_LABELS;
  const measureLabels = meta?.measure_labels || DEFAULT_MEASURE_LABELS;
  const dimValues = meta?.dimension_values || {};

  const toggleMeasure = (mKey) => {
    if (selectedMeasures.includes(mKey)) {
      if (selectedMeasures.length > 1) {
        setSelectedMeasures(selectedMeasures.filter(m => m !== mKey));
      }
    } else {
      setSelectedMeasures([...selectedMeasures, mKey]);
    }
  };

  const handleSwapPivot = () => {
    const temp = pivotRow;
    setPivotRow(pivotCol);
    setPivotCol(temp);
  };

  const executeQuery = async (op) => {
    setLoading(true);
    setError('');
    try {
      let payload = {
        operation: op,
        measure,
        agg_func: aggFunc
      };

      if (op === 'slice') {
        payload.dimension = sliceDim;
        payload.slice_value = sliceVal;
        payload.row_dim = sliceBreakdown !== 'none' ? sliceBreakdown : null;
      } else if (op === 'dice') {
        const conditions = {};
        if (diceBranch && diceBranch !== 'All') conditions.branch = [diceBranch];
        if (diceGender && diceGender !== 'All') conditions.gender = [diceGender];
        if (diceStatus && diceStatus !== 'All') conditions.placement_status = [diceStatus];
        if (diceTraining && diceTraining !== 'All') conditions.placement_training = [diceTraining];
        payload.dice_conditions = conditions;
        payload.row_dim = diceRowDim;
        payload.col_dim = diceColDim !== 'none' ? diceColDim : null;
      } else if (op === 'rollup') {
        payload.row_dim = rollupRowDetailed;
        payload.col_dim = rollupCol !== 'none' ? rollupCol : null;
        payload.filters = {
          current_rows: [rollupRowDetailed, rollupRowSub].filter(Boolean),
          target_rows: [rollupRowDetailed].filter(Boolean),
          current_cols: [rollupCol].filter(Boolean),
          target_cols: []
        };
      } else if (op === 'drilldown') {
        payload.row_dim = drillRowSummary;
        payload.col_dim = drillCol !== 'none' ? drillCol : null;
        payload.filters = {
          current_rows: [drillRowSummary].filter(Boolean),
          target_rows: [drillRowSummary, drillRowDetail].filter(Boolean),
          current_cols: [drillCol].filter(Boolean),
          target_cols: []
        };
      } else if (op === 'pivot') {
        payload.row_dim = pivotRow;
        payload.col_dim = pivotCol;
      } else if (op === 'drill_across') {
        payload.dimension = drillAcrossDim;
        payload.row_dim = drillAcrossDim;
        payload.measures = selectedMeasures;
      }

      const res = await fetch('/api/admin/olap/query', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });
      const data = await res.json();
      if (!res.ok) throw new Error(data.detail || 'OLAP query failed');
      setResults(data);
      loadHistory();
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const downloadCSV = () => {
    const rows = results?.rows || results?.data;
    if (!rows || rows.length === 0) return;
    const cols = results.columns;
    const csvRows = [
      cols.join(','),
      ...rows.map(r => cols.map(c => `"${r[c] ?? ''}"`).join(','))
    ];
    const blob = new Blob([csvRows.join('\n')], { type: 'text/csv' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `olap_${activeTab}_matrix.csv`;
    a.click();
    URL.revokeObjectURL(url);
  };

  // Render chart data from results
  const renderChart = (matrixCols, matrixRows) => {
    if (!matrixCols || !matrixRows || matrixRows.length === 0) return null;
    const xKey = matrixCols[0];
    const barKeys = matrixCols.slice(1);
    if (barKeys.length === 0) return null;

    const chartData = matrixRows.slice(0, 12).map(r => {
      const item = { name: String(r[xKey] ?? '') };
      barKeys.forEach(k => {
        const val = Number(r[k]);
        item[k] = !isNaN(val) ? Number(val.toFixed(2)) : 0;
      });
      return item;
    });

    return (
      <div style={{ height: '280px', marginTop: '20px' }}>
        <ResponsiveContainer width="100%" height="100%">
          <BarChart data={chartData} margin={{ top: 15, right: 20, bottom: 25, left: 10 }}>
            <CartesianGrid stroke="#F1F5F9" strokeDasharray="3 3" />
            <XAxis dataKey="name" stroke="#64748B" tick={{ fontSize: 11 }} />
            <YAxis stroke="#64748B" tick={{ fontSize: 11 }} />
            <Tooltip />
            <Legend />
            {barKeys.slice(0, 4).map((k, idx) => (
              <Bar key={k} dataKey={k} fill={CHART_COLORS[idx % CHART_COLORS.length]} radius={[4, 4, 0, 0]} />
            ))}
          </BarChart>
        </ResponsiveContainer>
      </div>
    );
  };

  return (
    <div>
      <div style={{ marginBottom: '24px' }}>
        <h2 style={{ fontSize: '1.6rem', fontWeight: 800, color: 'var(--navy)' }}>Multi-Dimensional OLAP Cube Analytics</h2>
        <p style={{ color: 'var(--text-muted)', fontSize: '0.92rem' }}>
          Explore 15,000+ student records with precise multidimensional Slice, Dice, 2D Roll-Up, 2D Drill-Down, Cross-Tabular Pivot, and Multi-Fact Drill-Across operations.
        </p>
      </div>

      {/* Tabs */}
      <div className="tabs-container">
        {[
          { id: 'slice', label: '1. Slice' },
          { id: 'dice', label: '2. Dice' },
          { id: 'rollup', label: '3. 2D Roll-Up' },
          { id: 'drilldown', label: '4. 2D Drill-Down' },
          { id: 'pivot', label: '5. Pivot' },
          { id: 'drill_across', label: '6. Drill-Across' },
          { id: 'history', label: '7. Query History' }
        ].map(t => (
          <button
            key={t.id}
            className={`tab-btn ${activeTab === t.id ? 'active' : ''}`}
            onClick={() => setActiveTab(t.id)}
          >
            {t.label}
          </button>
        ))}
      </div>

      {activeTab !== 'history' && (
        <div className="campus-card">
          <div className="campus-card-header">
            <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
              <Layers size={18} color="var(--primary)" />
              <div className="card-title">
                {activeTab === 'slice' && 'OLAP Slice Controls (Sub-Plane Filter)'}
                {activeTab === 'dice' && 'OLAP Dice Controls (Bounded Sub-Cube Selection)'}
                {activeTab === 'rollup' && '2-Dimensional Roll-Up (Dimension Generalization)'}
                {activeTab === 'drilldown' && '2-Dimensional Drill-Down (Granular De-Aggregation)'}
                {activeTab === 'pivot' && 'OLAP Pivot Controls (Cross-Tabulation Rotation)'}
                {activeTab === 'drill_across' && 'OLAP Drill-Across Controls (Multi-Fact Synthesis)'}
              </div>
            </div>

            <button className="btn btn-primary" onClick={() => executeQuery(activeTab)} disabled={loading}>
              <Play size={16} /> {loading ? 'Computing Sub-Cube...' : 'Execute OLAP Operation'}
            </button>
          </div>

          {/* Operation Specific Inputs */}
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(220px, 1fr))', gap: '16px', marginBottom: '16px' }}>
            {/* SLICE CONTROLS */}
            {activeTab === 'slice' && (
              <>
                <div className="form-group">
                  <label className="form-label">Slice Dimension (Fixed Plane)</label>
                  <select className="form-select" value={sliceDim} onChange={e => setSliceDim(e.target.value)}>
                    {dimensions.map(d => (
                      <option key={d} value={d}>{dimLabels[d] || d}</option>
                    ))}
                  </select>
                </div>

                <div className="form-group">
                  <label className="form-label">Slice Constant Value</label>
                  <select className="form-select" value={sliceVal} onChange={e => setSliceVal(e.target.value)}>
                    {(dimValues[sliceDim] || []).map(val => (
                      <option key={val} value={val}>{val}</option>
                    ))}
                  </select>
                </div>

                <div className="form-group">
                  <label className="form-label">Secondary Breakdown Axis</label>
                  <select className="form-select" value={sliceBreakdown} onChange={e => setSliceBreakdown(e.target.value)}>
                    <option value="none">None (Overall Cohort Aggregate)</option>
                    {dimensions.filter(d => d !== sliceDim).map(d => (
                      <option key={d} value={d}>{dimLabels[d] || d}</option>
                    ))}
                  </select>
                </div>
              </>
            )}

            {/* DICE CONTROLS */}
            {activeTab === 'dice' && (
              <>
                <div className="form-group">
                  <label className="form-label">Branch Filter</label>
                  <select className="form-select" value={diceBranch} onChange={e => setDiceBranch(e.target.value)}>
                    <option value="All">All Branches</option>
                    {(dimValues.branch || []).map(b => <option key={b} value={b}>{b}</option>)}
                  </select>
                </div>

                <div className="form-group">
                  <label className="form-label">Gender Filter</label>
                  <select className="form-select" value={diceGender} onChange={e => setDiceGender(e.target.value)}>
                    <option value="All">All Genders</option>
                    {(dimValues.gender || []).map(g => <option key={g} value={g}>{g}</option>)}
                  </select>
                </div>

                <div className="form-group">
                  <label className="form-label">Placement Status Filter</label>
                  <select className="form-select" value={diceStatus} onChange={e => setDiceStatus(e.target.value)}>
                    <option value="All">All Statuses</option>
                    <option value="Placed">Placed</option>
                    <option value="Not Placed">Not Placed</option>
                  </select>
                </div>

                <div className="form-group">
                  <label className="form-label">Row Dimension</label>
                  <select className="form-select" value={diceRowDim} onChange={e => setDiceRowDim(e.target.value)}>
                    {dimensions.map(d => <option key={d} value={d}>{dimLabels[d] || d}</option>)}
                  </select>
                </div>

                <div className="form-group">
                  <label className="form-label">Column Dimension</label>
                  <select className="form-select" value={diceColDim} onChange={e => setDiceColDim(e.target.value)}>
                    <option value="none">None</option>
                    {dimensions.filter(d => d !== diceRowDim).map(d => <option key={d} value={d}>{dimLabels[d] || d}</option>)}
                  </select>
                </div>
              </>
            )}

            {/* ROLL-UP CONTROLS */}
            {activeTab === 'rollup' && (
              <>
                <div className="form-group">
                  <label className="form-label">Primary Dimension</label>
                  <select className="form-select" value={rollupRowDetailed} onChange={e => setRollupRowDetailed(e.target.value)}>
                    {dimensions.map(d => <option key={d} value={d}>{dimLabels[d] || d}</option>)}
                  </select>
                </div>

                <div className="form-group">
                  <label className="form-label">Secondary Granularity (To Roll Up)</label>
                  <select className="form-select" value={rollupRowSub} onChange={e => setRollupRowSub(e.target.value)}>
                    {dimensions.filter(d => d !== rollupRowDetailed).map(d => <option key={d} value={d}>{dimLabels[d] || d}</option>)}
                  </select>
                </div>

                <div className="form-group">
                  <label className="form-label">Column Dimension</label>
                  <select className="form-select" value={rollupCol} onChange={e => setRollupCol(e.target.value)}>
                    <option value="placement_status">Placement Status</option>
                    <option value="placement_training">Placement Training</option>
                    <option value="none">None</option>
                  </select>
                </div>
              </>
            )}

            {/* DRILL-DOWN CONTROLS */}
            {activeTab === 'drilldown' && (
              <>
                <div className="form-group">
                  <label className="form-label">Summary Row Dimension</label>
                  <select className="form-select" value={drillRowSummary} onChange={e => setDrillRowSummary(e.target.value)}>
                    {dimensions.map(d => <option key={d} value={d}>{dimLabels[d] || d}</option>)}
                  </select>
                </div>

                <div className="form-group">
                  <label className="form-label">De-aggregate With (Drill-Down Dimension)</label>
                  <select className="form-select" value={drillRowDetail} onChange={e => setDrillRowDetail(e.target.value)}>
                    {dimensions.filter(d => d !== drillRowSummary).map(d => <option key={d} value={d}>{dimLabels[d] || d}</option>)}
                  </select>
                </div>

                <div className="form-group">
                  <label className="form-label">Column Dimension</label>
                  <select className="form-select" value={drillCol} onChange={e => setDrillCol(e.target.value)}>
                    <option value="placement_status">Placement Status</option>
                    <option value="placement_training">Placement Training</option>
                    <option value="none">None</option>
                  </select>
                </div>
              </>
            )}

            {/* PIVOT CONTROLS */}
            {activeTab === 'pivot' && (
              <>
                <div className="form-group">
                  <label className="form-label">Row Dimension</label>
                  <select className="form-select" value={pivotRow} onChange={e => setPivotRow(e.target.value)}>
                    {dimensions.map(d => <option key={d} value={d}>{dimLabels[d] || d}</option>)}
                  </select>
                </div>

                <div className="form-group">
                  <label className="form-label">Column Dimension</label>
                  <select className="form-select" value={pivotCol} onChange={e => setPivotCol(e.target.value)}>
                    {dimensions.filter(d => d !== pivotRow).map(d => <option key={d} value={d}>{dimLabels[d] || d}</option>)}
                  </select>
                </div>

                <div className="form-group" style={{ display: 'flex', alignItems: 'flex-end' }}>
                  <button className="btn btn-secondary" style={{ width: '100%', gap: '8px' }} onClick={handleSwapPivot}>
                    <ArrowLeftRight size={16} /> Swap Axes (⇄)
                  </button>
                </div>
              </>
            )}

            {/* DRILL-ACROSS CONTROLS */}
            {activeTab === 'drill_across' && (
              <>
                <div className="form-group">
                  <label className="form-label">Target Dimension</label>
                  <select className="form-select" value={drillAcrossDim} onChange={e => setDrillAcrossDim(e.target.value)}>
                    {dimensions.map(d => <option key={d} value={d}>{dimLabels[d] || d}</option>)}
                  </select>
                </div>
              </>
            )}

            {/* COMMON MEASURE & AGGREGATION (Hidden for Drill-Across which has multi-measures) */}
            {activeTab !== 'drill_across' && (
              <>
                <div className="form-group">
                  <label className="form-label">Additive Measure</label>
                  <select className="form-select" value={measure} onChange={e => setMeasure(e.target.value)}>
                    {measures.map(m => (
                      <option key={m} value={m}>{measureLabels[m] || m}</option>
                    ))}
                  </select>
                </div>

                <div className="form-group">
                  <label className="form-label">Aggregation Function</label>
                  <select className="form-select" value={aggFunc} onChange={e => setAggFunc(e.target.value)}>
                    {aggregations.map(a => <option key={a} value={a}>{a.toUpperCase()}</option>)}
                  </select>
                </div>
              </>
            )}
          </div>

          {/* Drill-Across Multi-Measure Checklist */}
          {activeTab === 'drill_across' && (
            <div style={{ marginTop: '10px', paddingTop: '16px', borderTop: '1px solid #F1F5F9' }}>
              <label className="form-label" style={{ marginBottom: '10px' }}>
                Select Multi-Measure Facts to Consolidate ({selectedMeasures.length} selected):
              </label>
              <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '10px' }}>
                {measures.map(m => {
                  const checked = selectedMeasures.includes(m);
                  return (
                    <div
                      key={m}
                      onClick={() => toggleMeasure(m)}
                      style={{
                        display: 'flex',
                        alignItems: 'center',
                        gap: '8px',
                        padding: '8px 12px',
                        background: checked ? '#EFF6FF' : '#F8FAFC',
                        border: `1px solid ${checked ? 'var(--primary)' : '#E2E8F0'}`,
                        borderRadius: '8px',
                        cursor: 'pointer',
                        fontSize: '0.85rem',
                        fontWeight: checked ? 700 : 500,
                        color: checked ? 'var(--primary)' : '#334155'
                      }}
                    >
                      {checked ? <CheckSquare size={16} color="var(--primary)" /> : <Square size={16} color="#94A3B8" />}
                      <span>{measureLabels[m] || m}</span>
                    </div>
                  );
                })}
              </div>
            </div>
          )}
        </div>
      )}

      {error && (
        <div style={{ background: '#FEF2F2', color: '#DC2626', border: '1px solid #FECACA', padding: '14px 18px', borderRadius: '10px', marginBottom: '20px' }}>
          <strong>Query Error:</strong> {error}
        </div>
      )}

      {/* BEFORE / AFTER COMPARISON FOR ROLLUP AND DRILLDOWN */}
      {results && (activeTab === 'rollup' || activeTab === 'drilldown') && results.before_columns && results.before_rows && (
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(420px, 1fr))', gap: '20px', marginBottom: '24px' }}>
          {/* Before Table */}
          <div className="campus-card">
            <div className="campus-card-header">
              <div className="card-title">
                {activeTab === 'rollup' ? 'Before: Granular View (Detailed Cohorts)' : 'Before: Summary View (High-Level)'}
              </div>
              <span className="badge badge-role">Initial State</span>
            </div>
            <div className="table-container">
              <table className="data-table">
                <thead>
                  <tr>
                    {results.before_columns.map(col => <th key={col}>{col}</th>)}
                  </tr>
                </thead>
                <tbody>
                  {results.before_rows.slice(0, 10).map((row, i) => (
                    <tr key={i}>
                      {results.before_columns.map((col, j) => (
                        <td key={j} style={{ fontWeight: j === 0 ? 700 : 400 }}>
                          {typeof row[col] === 'number' ? row[col].toFixed(2) : String(row[col] ?? '')}
                        </td>
                      ))}
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>

          {/* After Table */}
          <div className="campus-card">
            <div className="campus-card-header">
              <div className="card-title">
                {activeTab === 'rollup' ? 'After: Generalised Roll-Up (Summary View)' : 'After: De-aggregated Drill-Down (Detailed View)'}
              </div>
              <span className="badge" style={{ background: '#DCFCE7', color: '#16A34A', border: '1px solid #86EFAC' }}>
                Output State
              </span>
            </div>
            <div className="table-container">
              <table className="data-table">
                <thead>
                  <tr>
                    {results.columns.map(col => <th key={col}>{col}</th>)}
                  </tr>
                </thead>
                <tbody>
                  {(results.rows || results.data || []).slice(0, 10).map((row, i) => (
                    <tr key={i}>
                      {results.columns.map((col, j) => (
                        <td key={j} style={{ fontWeight: j === 0 ? 700 : 400 }}>
                          {typeof row[col] === 'number' ? row[col].toFixed(2) : String(row[col] ?? '')}
                        </td>
                      ))}
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        </div>
      )}

      {/* Query Results Main Table & Chart */}
      {results && activeTab !== 'history' && (
        <div className="campus-card" style={{ marginBottom: '24px' }}>
          <div className="campus-card-header">
            <div>
              <div className="card-title">OLAP Result Matrix: {results.operation?.toUpperCase()}</div>
              <div className="card-subtitle">
                Aggregated {results.row_count ?? results.count ?? (results.rows?.length || 0)} rows from Data Warehouse
              </div>
            </div>

            <button className="btn btn-secondary" onClick={downloadCSV}>
              <Download size={16} /> Export Matrix (CSV)
            </button>
          </div>

          <div className="table-container">
            <table className="data-table">
              <thead>
                <tr>
                  {results.columns.map(col => (
                    <th key={col}>{dimLabels[col] || measureLabels[col] || col}</th>
                  ))}
                </tr>
              </thead>
              <tbody>
                {(results.rows || results.data || []).map((row, i) => (
                  <tr key={i}>
                    {results.columns.map((col, j) => (
                      <td key={j} style={{ fontWeight: j === 0 ? 700 : 400 }}>
                        {typeof row[col] === 'number' ? row[col].toFixed(2) : String(row[col] ?? '')}
                      </td>
                    ))}
                  </tr>
                ))}
              </tbody>
            </table>
          </div>

          {/* Visual Bar Chart */}
          {renderChart(results.columns, results.rows || results.data)}
        </div>
      )}

      {/* History Tab */}
      {activeTab === 'history' && (
        <div className="campus-card">
          <div className="campus-card-header">
            <div className="card-title">OLAP Audit & Execution Log</div>
            <span className="badge badge-role">{history.length} Queries Logged</span>
          </div>

          {history.length > 0 ? (
            <div className="table-container">
              <table className="data-table">
                <thead>
                  <tr>
                    <th>Timestamp</th>
                    <th>Operation</th>
                    <th>Parameters / Filters</th>
                    <th>Result Rows</th>
                  </tr>
                </thead>
                <tbody>
                  {history.map((h, i) => (
                    <tr key={i}>
                      <td>{h.timestamp}</td>
                      <td><span className="badge badge-role">{h.operation}</span></td>
                      <td style={{ maxWidth: '400px', fontSize: '0.82rem' }}>{h.filters}</td>
                      <td style={{ fontWeight: 700 }}>{h.result_rows}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          ) : (
            <div style={{ padding: '36px', textAlign: 'center', color: '#64748B' }}>
              No OLAP operations logged yet. Execute an operation to track audit history.
            </div>
          )}
        </div>
      )}

      {/* Academic Justification */}
      <AcademicJustification
        title="Multi-Dimensional OLAP Cube Operations & Strategic Navigation"
        algorithmName="OLAP Operations: Slice • Dice • 2D Roll-Up • 2D Drill-Down • Pivot • Drill-Across"
        whyUsed={[
          ["Interactive Dimensional Slicing & Dicing", "Standard static tables only show flat, predefined views of student cohorts. The Slice operation isolates a specific sub-plane along a single dimension (e.g. Branch = CSE), while Dice extracts a localized sub-cube bounded by multiple simultaneous criteria (e.g. Branch IN ['CSE', 'IT'] and Placement Status = 'Placed'). This allows placement officers to isolate niche talent pools instantly for incoming specialized recruiters."],
          ["Bidirectional Hierarchical Navigation (Roll-Up & Drill-Down)", "Academic leadership requires insights at different levels of abstraction. Simultaneous 2D Roll-Up summarizes granular data upward along conceptual hierarchies (Student → Branch → Campus Institution), revealing macro placement trends. Conversely, Drill-Down navigates downward from high-level statistics into granular candidate records, enabling immediate targeted academic counseling for high-risk students."],
          ["Axis Rotation (Pivot) & Multi-Fact Synthesis (Drill-Across)", "The Pivot operation reorients cube axes to present cross-tabulated contingency matrices (e.g. Academic Performance vs Placement Rate), surfacing hidden dimensional dependencies. Drill-Across spans multiple fact domains, consolidating student co-curricular milestones with final hiring conversion into a unified analytical matrix."]
        ]}
        institutionalImpact="Transforms placement intelligence from reactive post-semester reviews into proactive, real-time decision-making—allowing placement deans to continuously evaluate departmental conversion rates, optimize faculty training allocations, and track cohort progress."
        dwmConcept="Multi-Dimensional Data Cube (MOLAP / ROLAP), Slice & Dice Projections, Concept Hierarchies & Dimension Generalization, Granular Decomposition, Cross-Tabular Rotation, Multi-Fact Federation."
      />
    </div>
  );
}
