export default function Topbar({ title }) {
  return (
    <div style={{ marginBottom: '32px' }}>
      <h1 className="page-title">{title}</h1>
      <div style={{ color: 'var(--text-secondary)', fontSize: '0.9rem' }}>
        Real-time insights & predictive analytics &nbsp;•&nbsp; <span style={{ color: 'var(--blue)' }}>Last updated: Today</span>
      </div>
    </div>
  );
}