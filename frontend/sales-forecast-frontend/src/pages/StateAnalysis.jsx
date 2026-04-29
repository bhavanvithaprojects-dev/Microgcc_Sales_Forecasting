import { useState, useEffect } from "react";
import MultiLineChart from "../components/charts/MultiLineChart";
import Topbar from "../components/layout/Topbar";
import StateFilter from "../components/filters/StateFilter";
import { fetchCompareStates } from "../services/api";

export default function StateAnalysis() {
  const [state1, setState1] = useState("CA");
  const [state2, setState2] = useState("NY");
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const loadComparison = async () => {
      setLoading(true);
      try {
        const result = await fetchCompareStates(state1, state2);
        setData(result);
      } catch (error) {
        console.error("Failed to fetch comparison data:", error);
      } finally {
        setLoading(false);
      }
    };
    loadComparison();
  }, [state1, state2]);

  return (
    <div className="state-analysis-page">
      <Topbar title="State Comparison" />

      <div className="info-banner">
        Select two states to compare their historical sales performance side-by-side.
      </div>

      <div className="filter-row" style={{ marginBottom: '30px' }}>
        <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
          <label style={{ fontSize: '0.8rem', color: 'var(--text-secondary)' }}>Select State 1</label>
          <StateFilter onChange={setState1} value={state1} hideAllOption={true} />
        </div>
        <div style={{ display: 'flex', alignItems: 'center', paddingTop: '20px', fontWeight: 700, color: 'var(--text-secondary)' }}>
          VS
        </div>
        <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
          <label style={{ fontSize: '0.8rem', color: 'var(--text-secondary)' }}>Select State 2</label>
          <StateFilter onChange={setState2} value={state2} hideAllOption={true} />
        </div>
      </div>

      <div className="card">
        <h2 style={{ fontSize: '1.1rem', fontWeight: 700, marginBottom: '20px', color: '#fff' }}>
          {state1} vs {state2} Performance
        </h2>
        
        {loading ? (
          <div style={{ padding: '40px', textAlign: 'center', color: 'var(--text-secondary)' }}>
            Analyzing comparative trends...
          </div>
        ) : (
          <div className="chart-container">
            <MultiLineChart data={data} state1={state1} state2={state2} />
          </div>
        )}
      </div>
    </div>
  );
}