import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid,
  Legend,
  ResponsiveContainer,
} from "recharts";

export default function SalesChart({ data }) {
  const formatYAxis = (value) => {
    if (value >= 1000000) return `${(value / 1000000).toFixed(1)}M`;
    if (value >= 1000) return `${(value / 1000).toFixed(0)}K`;
    return value;
  };

  return (
    <div style={{ width: '100%', height: 400 }}>
      <ResponsiveContainer>
        <LineChart data={data} margin={{ top: 10, right: 30, left: 20, bottom: 0 }}>
          <CartesianGrid strokeDasharray="3 3" stroke="#eee" vertical={false} />
          <XAxis 
            dataKey="date" 
            stroke="#6c757d" 
            fontSize={12}
            tickLine={false}
            axisLine={false}
            dy={10}
          />
          <YAxis 
            stroke="#6c757d" 
            fontSize={12}
            tickLine={false}
            axisLine={false}
            tickFormatter={formatYAxis}
            width={60}
          />
          <Tooltip 
            formatter={(value) => [`₹${value.toLocaleString()}`, "Sales"]}
            contentStyle={{ 
              backgroundColor: '#fff', 
              border: '1px solid #ddd', 
              borderRadius: '4px',
              boxShadow: '0 2px 4px rgba(0,0,0,0.1)'
            }}
          />
          <Legend 
            iconType="rect" 
            wrapperStyle={{ paddingTop: '20px', fontSize: '12px' }} 
          />

          <Line
            type="monotone"
            dataKey="historical"
            stroke="#007BFF"
            strokeWidth={2}
            dot={{ r: 4, fill: '#007BFF' }}
            activeDot={{ r: 6 }}
            name="Historical Sales"
          />
          <Line
            type="monotone"
            dataKey="forecast"
            stroke="#6F42C1"
            strokeWidth={2}
            strokeDasharray="5 5"
            dot={{ r: 4, fill: '#6F42C1' }}
            activeDot={{ r: 6 }}
            name="Forecasted Trend"
          />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}