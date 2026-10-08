import React, { useEffect, useState } from 'react';
import { History, TrendingUp, CheckCircle2, Clock } from 'lucide-react';
import { LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer, CartesianGrid } from 'recharts';

export default function PredictionHistory({ user }) {
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!user?.email) return;
    fetch(`/api/student/history/${encodeURIComponent(user.email)}`)
      .then(res => res.json())
      .then(data => {
        setHistory(data?.history || []);
        setLoading(false);
      })
      .catch(() => setLoading(false));
  }, [user]);

  if (loading) return <div style={{ padding: '40px', color: '#64748B' }}>Loading audit logs...</div>;

  const chartData = history.map((item, idx) => {
    const ts = item.timestamp || item.predicted_at || item.created_at || '';
    const isPlaced = (item.predicted_status === 'Placed') ||
                     (item.status === 'Placed') ||
                     (item.prediction === 1) ||
                     (Number(item.probability) >= 0.5);
    return {
      name: ts ? ts.split(' ')[0] : `Run ${idx + 1}`,
      probability: Math.round(Number(item.probability || 0) * 100),
      prediction: isPlaced ? 'Placed' : 'Not Placed'
    };
  }).reverse();

  return (
    <div>
      <div style={{ marginBottom: '24px' }}>
        <h2 style={{ fontSize: '1.6rem', fontWeight: 800, color: 'var(--navy)' }}>Prediction Audit History</h2>
        <p style={{ color: 'var(--text-muted)', fontSize: '0.92rem' }}>
          Historical record tracking your placement probability progression over time.
        </p>
      </div>

      {chartData.length > 1 && (
        <div className="campus-card">
          <div className="campus-card-header">
            <div className="card-title">Placement Probability Progression Over Time</div>
            <span className="badge badge-role">Historical Trajectory</span>
          </div>

          <div style={{ height: '300px' }}>
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={chartData} margin={{ top: 20, right: 30, left: 0, bottom: 5 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="#F1F5F9" />
                <XAxis dataKey="name" stroke="#64748B" />
                <YAxis domain={[0, 100]} stroke="#64748B" />
                <Tooltip formatter={(value) => [`${value}%`, 'Probability']} />
                <Line type="monotone" dataKey="probability" stroke="#2563EB" strokeWidth={3} dot={{ r: 5, fill: '#2563EB' }} activeDot={{ r: 8 }} />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </div>
      )}

      <div className="campus-card">
        <div className="campus-card-header">
          <div className="card-title">Audit Log Entries</div>
          <span className="badge badge-role">{history.length} Saved Records</span>
        </div>

        {history.length === 0 ? (
          <div style={{ textAlign: 'center', padding: '36px', color: '#64748B' }}>
            <History size={40} style={{ opacity: 0.3, marginBottom: '10px' }} />
            <p>No historical predictions recorded yet for this account.</p>
          </div>
        ) : (
          <div className="table-container">
            <table className="data-table">
              <thead>
                <tr>
                  <th>Timestamp</th>
                  <th>Assessment Type</th>
                  <th>Outcome</th>
                  <th>Probability</th>
                  <th>Audit Reference</th>
                </tr>
              </thead>
              <tbody>
                {history.map((row, i) => {
                  const isPlaced = (row.predicted_status === 'Placed') ||
                                   (row.status === 'Placed') ||
                                   (row.prediction === 1) ||
                                   (Number(row.probability) >= 0.5);
                  const timestamp = row.timestamp || row.predicted_at || row.created_at || '—';
                  const probPercent = (Number(row.probability || 0) * 100).toFixed(1);
                  return (
                    <tr key={row.id || i}>
                      <td style={{ color: '#0F172A', fontWeight: 600 }}>{timestamp}</td>
                      <td>Automated Placement Evaluation</td>
                      <td>
                        <span className={`badge ${isPlaced ? 'badge-placed' : 'badge-not-placed'}`}>
                          {isPlaced ? 'PLACED' : 'NOT PLACED'}
                        </span>
                      </td>
                      <td style={{ fontWeight: 700, color: isPlaced ? '#16A34A' : '#DC2626' }}>
                        {probPercent}%
                      </td>
                      <td style={{ fontSize: '0.78rem', color: '#94A3B8', fontFamily: 'monospace' }}>
                        ID #{row.id}
                      </td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  );
}
