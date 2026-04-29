export default function ForecastTable({ data }) {
  return (
    <div className="table-container">
      <table>
        <thead>
          <tr>
            <th>Timeline</th>
            <th>Projected Sales</th>
          </tr>
        </thead>
        <tbody>
          {data.map((d, i) => (
            <tr key={i}>
              <td>{d.date}</td>
              <td style={{ fontWeight: 600, color: 'var(--accent-blue)' }}>{d.forecast}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}