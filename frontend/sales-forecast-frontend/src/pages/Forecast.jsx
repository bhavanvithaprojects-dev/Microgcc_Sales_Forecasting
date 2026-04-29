import { useState, useEffect } from "react";
import ForecastTable from "../components/tables/ForecastTable";
import StateFilter from "../components/filters/StateFilter";
import Topbar from "../components/layout/Topbar";
import { fetchDashboardData } from "../services/api";

export default function Forecast() {
  const [forecastData, setForecastData] = useState([]);
  const [selectedState, setSelectedState] = useState("All States");
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const loadForecast = async () => {
      setLoading(true);
      try {
        const data = await fetchDashboardData(selectedState);
        setForecastData(data.forecast_table);
      } catch (error) {
        console.error("Failed to fetch forecast:", error);
      } finally {
        setLoading(false);
      }
    };
    loadForecast();
  }, [selectedState]);

  return (
    <div className="forecast-page">
      <Topbar title="Forecast Details" />

      <div className="filter-row">
        <StateFilter onChange={setSelectedState} value={selectedState} />
      </div>

      <div className="info-banner">
        Showing forecasted sales for <strong>{selectedState}</strong> for the next 8 weeks based on historical trends and advanced machine learning models.
      </div>

      <div className="card">
        <h2 style={{ fontSize: '1.1rem', fontWeight: 700, marginBottom: '20px', color: '#fff' }}>
          Projected Sales Data
        </h2>
        {loading ? (
          <div style={{ color: 'var(--text-secondary)' }}>Calculating forecast...</div>
        ) : (
          <ForecastTable data={forecastData} />
        )}
      </div>
    </div>
  );
}