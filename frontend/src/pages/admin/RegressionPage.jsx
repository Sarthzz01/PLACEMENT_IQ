import React, { useEffect, useState } from 'react';
import { ScatterChart, Scatter, XAxis, YAxis, Tooltip, ResponsiveContainer, CartesianGrid, BarChart, Bar } from 'recharts';
import AcademicJustification from '../../components/AcademicJustification';

export default function RegressionPage() {
  const [data, setData] = useState(null);
  const [target, setTarget] = useState('aptitude_score');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    setLoading(true);
    fetch(`/api/admin/regression?target_col=${target}`)
      .then(r => r.json())
      .then(d => {
        setData(d);
        setLoading(false);
      })
      .catch(() => setLoading(false));
  }, [target]);

  const slr = data?.artifacts?.['Simple Linear Regression'];
  const mlr = data?.artifacts?.['Multiple Linear Regression'];

  // Combine actual and predicted for scatter
  const scatterData = (slr?.actual_sample || []).map((act, i) => ({
    actual: act,
    predicted: slr?.pred_sample?.[i] || 0
  }));

  const resData = (slr?.residuals_sample || []).slice(0, 30).map((res, i) => ({
    index: i + 1,
    residual: res
  }));

  return (
    <div>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '24px', flexWrap: 'wrap', gap: '12px' }}>
        <div>
          <h2 style={{ fontSize: '1.6rem', fontWeight: 800, color: 'var(--navy)' }}>Continuous Numerical Regression Analysis</h2>
          <p style={{ color: 'var(--text-muted)', fontSize: '0.92rem' }}>
            Fit Simple Linear Regression (SLR) and Multiple Linear Regression (MLR) on candidate placement competency targets.
          </p>
        </div>

        <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
          <label style={{ fontSize: '0.85rem', fontWeight: 700, color: '#334155' }}>Continuous Target:</label>
          <select className="form-select" style={{ width: '200px' }} value={target} onChange={e => setTarget(e.target.value)}>
            <option value="aptitude_score">Aptitude Score</option>
            <option value="coding_skill_score">Coding Skill Score</option>
            <option value="cgpa">Cumulative CGPA</option>
          </select>
        </div>
      </div>

      {loading ? (
        <div style={{ padding: '40px', color: '#64748B' }}>Fitting regression equations...</div>
      ) : (
        <>
          {/* Regression Equations Cards */}
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(340px, 1fr))', gap: '20px', marginBottom: '24px' }}>
            <div className="campus-card">
              <div className="campus-card-header">
                <div className="card-title">Simple Linear Regression (SLR)</div>
                <span className="badge badge-role">R² = {slr?.r2}</span>
              </div>
              <div style={{ background: '#F8FAFC', padding: '14px', borderRadius: '8px', fontFamily: 'monospace', fontSize: '0.88rem', color: '#0F172A', marginBottom: '12px' }}>
                {slr?.equation || 'y = β₀ + β₁x'}
              </div>
              <div style={{ fontSize: '0.82rem', color: '#64748B' }}>
                Evaluates univariate baseline predicting {target} from primary academic predictor.
              </div>
            </div>

            <div className="campus-card">
              <div className="campus-card-header">
                <div className="card-title">Multiple Linear Regression (MLR)</div>
                <span className="badge" style={{ background: '#F0FDF4', color: '#16A34A', border: '1px solid #86EFAC' }}>R² = {mlr?.r2}</span>
              </div>
              <div style={{ background: '#F8FAFC', padding: '14px', borderRadius: '8px', fontFamily: 'monospace', fontSize: '0.85rem', color: '#0F172A', marginBottom: '12px', maxHeight: '90px', overflowY: 'auto' }}>
                {mlr?.equation || 'y = β₀ + Σ(βⱼxⱼ)'}
              </div>
              <div style={{ fontSize: '0.82rem', color: '#64748B' }}>
                Multivariate expansion incorporating co-curricular, problem solving, and GPA features.
              </div>
            </div>
          </div>

          {/* Metrics Table */}
          <div className="campus-card" style={{ marginBottom: '24px' }}>
            <div className="campus-card-header">
              <div className="card-title">Goodness-of-Fit & Error Benchmarks</div>
              <span className="badge badge-role">Test Set Evaluation</span>
            </div>

            <div className="table-container">
              <table className="data-table">
                <thead>
                  <tr>
                    <th>Regression Model</th>
                    <th>R² Score (Explained Variance)</th>
                    <th>Mean Squared Error (MSE)</th>
                    <th>Mean Absolute Error (MAE)</th>
                  </tr>
                </thead>
                <tbody>
                  {data?.metrics?.map((row, i) => (
                    <tr key={i}>
                      <td style={{ fontWeight: 700, color: '#0F172A' }}>{row.Model}</td>
                      <td style={{ fontWeight: 700, color: 'var(--primary)' }}>
                        {(Number(row['R² Score'] ?? row['R²'] ?? row.R2 ?? 0)).toFixed(4)}
                      </td>
                      <td>{(Number(row.MSE ?? 0)).toFixed(4)}</td>
                      <td>{(Number(row.MAE ?? 0)).toFixed(4)}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>

          {/* Charts Grid */}
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(400px, 1fr))', gap: '20px', marginBottom: '24px' }}>
            <div className="campus-card">
              <div className="campus-card-header">
                <div className="card-title">Actual vs. Predicted Values</div>
                <span className="badge badge-role">SLR Fit</span>
              </div>
              <div style={{ height: '300px' }}>
                <ResponsiveContainer width="100%" height="100%">
                  <ScatterChart margin={{ top: 20, right: 20, bottom: 20, left: 20 }}>
                    <CartesianGrid stroke="#F1F5F9" />
                    <XAxis type="number" dataKey="actual" name="Actual" stroke="#64748B" />
                    <YAxis type="number" dataKey="predicted" name="Predicted" stroke="#64748B" />
                    <Tooltip cursor={{ strokeDasharray: '3 3' }} />
                    <Scatter name="Students" data={scatterData} fill="#2563EB" opacity={0.6} />
                  </ScatterChart>
                </ResponsiveContainer>
              </div>
            </div>

            <div className="campus-card">
              <div className="campus-card-header">
                <div className="card-title">Sample Residual Errors</div>
                <span className="badge badge-role">Residual Diagnostics</span>
              </div>
              <div style={{ height: '300px' }}>
                <ResponsiveContainer width="100%" height="100%">
                  <BarChart data={resData} margin={{ top: 20, right: 20, bottom: 20, left: 20 }}>
                    <CartesianGrid stroke="#F1F5F9" />
                    <XAxis dataKey="index" stroke="#64748B" />
                    <YAxis stroke="#64748B" />
                    <Tooltip />
                    <Bar dataKey="residual" fill="#6366F1" radius={[4, 4, 0, 0]} />
                  </BarChart>
                </ResponsiveContainer>
              </div>
            </div>
          </div>
        </>
      )}

      {/* Academic Justification */}
      <AcademicJustification
        title="Continuous Placement Competency & Skill Estimation"
        algorithmName="Simple Linear Regression (SLR) & Multiple Linear Regression (MLR)"
        whyUsed={[
          ["Univariate Baseline with SLR", "Simple Linear Regression isolates the direct, single-variable predictive power of foundational academic metrics (like CGPA) against quantitative skill targets (like Aptitude Score). By computing the slope and R², it demonstrates the empirical ceiling of relying solely on classroom marks for hiring competency."],
          ["Multivariate Weight Decomposition with MLR", "Multiple Linear Regression models the composite interaction of academic, coding, and experiential attributes simultaneously. The learned regression coefficients (β) quantify the exact marginal return for each unit increase in a feature (e.g., how much each additional project or 10 DSA questions lifts expected aptitude/coding competency), holding all other variables constant."],
          ["Residual Analysis & Error Diagnostics", "Visualizing residual error distributions verifies the fundamental Gauss-Markov assumptions (homoscedasticity, normality of error terms, zero mean). Centered, bell-shaped residual distributions validate that our linear formulations capture the true continuous trend without systematic bias."]
        ]}
        institutionalImpact="Equips placement advisors with quantifiable, parametric equations to set realistic semester-by-semester skill improvement milestones for students, moving beyond qualitative advice to precise numerical guidance."
        dwmConcept="Continuous Numerical Prediction, Ordinary Least Squares (OLS) Optimization, Multivariate Coefficient Interpretation, Residual Diagnostics."
      />
    </div>
  );
}
