import { useState, useEffect } from "react";
import ModelTable from "../components/tables/ModelTable";
import Topbar from "../components/layout/Topbar";
import { fetchModelsData } from "../services/api";

export default function Models() {
  const [models, setModels] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const loadModels = async () => {
      try {
        const data = await fetchModelsData();
        setModels(data);
      } catch (error) {
        console.error("Failed to fetch models:", error);
      } finally {
        setLoading(false);
      }
    };
    loadModels();
  }, []);

  return (
    <div className="models-page">
      <Topbar title="Model Comparison" />

      <div className="info-banner">
        Comparison of various forecasting models based on accuracy metrics. <strong>XGBoost</strong> is currently the best performing model.
      </div>

      <div className="card">
        <h2 style={{ fontSize: '1.1rem', fontWeight: 700, marginBottom: '20px', color: '#fff' }}>
          Performance Metrics
        </h2>
        {loading ? (
          <div style={{ color: 'var(--text-secondary)' }}>Loading model stats...</div>
        ) : (
          <ModelTable data={models} />
        )}
      </div>
    </div>
  );
}