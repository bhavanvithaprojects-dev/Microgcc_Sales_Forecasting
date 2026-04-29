export default function ModelTable({ data }) {
  return (
    <div className="table-container">
      <table>
        <thead>
          <tr>
            <th>Algorithm</th>
            <th>RMSE</th>
            <th>MAE</th>
            <th>MAPE</th>
          </tr>
        </thead>

        <tbody>
          {data.map((m, i) => (
            <tr key={i} style={m.name === "XGBoost" ? { background: 'rgba(0, 123, 255, 0.05)' } : {}}>
              <td style={{ fontWeight: 600 }}>
                {m.name} {m.name === "XGBoost" && <span style={{ color: 'var(--accent-blue)', fontSize: '0.65rem', marginLeft: '12px', background: 'rgba(0, 123, 255, 0.1)', padding: '2px 6px', borderRadius: '4px' }}>BEST</span>}
              </td>
              <td>{m.rmse}</td>
              <td>{m.mae}</td>
              <td>{m.mape}%</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}