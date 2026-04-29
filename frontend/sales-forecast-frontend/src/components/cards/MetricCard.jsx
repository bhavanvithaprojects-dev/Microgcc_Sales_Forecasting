export default function MetricCard({ title, value }) {
  return (
    <div className="card metric-card">
      <h4 className="metric-title">{title}</h4>
      <p className="metric-value">{value}</p>
    </div>
  );
}