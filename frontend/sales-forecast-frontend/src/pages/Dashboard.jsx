import { useState, useEffect } from "react";
import MetricCard from "../components/cards/MetricCard";
import SalesChart from "../components/charts/LineChart";
import StateFilter from "../components/filters/StateFilter";
import DateRangePicker from "../components/filters/DateRangePicker";
import Topbar from "../components/layout/Topbar";
import { fetchDashboardData } from "../services/api";

export default function Dashboard() {
  const [data, setData] = useState(null);
  const [selectedState, setSelectedState] = useState("All States");
  const [selectedDate, setSelectedDate] = useState("");
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const loadData = async () => {
      setLoading(true);
      try {
        const result = await fetchDashboardData(selectedState, selectedDate);
        setData(result);
      } catch (error) {
        console.error("Failed to fetch dashboard data:", error);
      } finally {
        setLoading(false);
      }
    };
    loadData();
  }, [selectedState, selectedDate]);

  const formatCurrency = (value) => {
    if (value >= 1000000) return `₹${(value / 1000000).toFixed(1)}M`;
    if (value >= 1000) return `₹${(value / 1000).toFixed(1)}K`;
    return `₹${value}`;
  };

  return (
    <div className="dashboard-wrapper">
      <Topbar title="Dashboard" />

      <div className="filter-row">
        <StateFilter onChange={setSelectedState} value={selectedState} />
        <DateRangePicker onChange={setSelectedDate} value={selectedDate} />
      </div>

      {loading ? (
        <div style={{ padding: '40px', textAlign: 'center', color: 'var(--text-secondary)' }}>
          Loading dashboard insights...
        </div>
      ) : data ? (
        <>
          <div className="metric-grid">
            <MetricCard
              title="Total Sales"
              value={formatCurrency(data.total_sales)}
            />
            <MetricCard
              title="Forecast (Next 8 Weeks)"
              value={formatCurrency(data.forecast_total)}
            />
            <MetricCard
              title="Best Model"
              value={data.best_model}
            />
          </div>

          <div className="card">
            <h2 style={{ fontSize: '1.1rem', fontWeight: 700, marginBottom: '20px', color: 'var(--text-primary)' }}>
              Sales Trend (Historical vs Forecast) - {selectedState}
            </h2>

            <div className="chart-container">
              <SalesChart data={data.trend} />
            </div>
          </div>
        </>
      ) : (
        <div style={{ padding: '40px', textAlign: 'center', color: 'red' }}>
          Error loading data from backend.
        </div>
      )}
    </div>
  );
}