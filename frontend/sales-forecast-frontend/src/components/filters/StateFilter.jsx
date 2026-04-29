import { useState, useEffect } from "react";
import { fetchStates } from "../../services/api";

export default function StateFilter({ onChange, value, hideAllOption }) {
  const [states, setStates] = useState([]);

  useEffect(() => {
    const loadStates = async () => {
      try {
        const fetchedStates = await fetchStates();
        setStates(fetchedStates);
      } catch (error) {
        console.error("Failed to fetch states:", error);
      }
    };
    loadStates();
  }, []);

  return (
    <select
      className="filter-select"
      value={value}
      onChange={(e) => onChange && onChange(e.target.value)}
    >
      {!hideAllOption && <option value="All States">All States</option>}
      {states.map((state) => (
        <option key={state} value={state}>
          {state}
        </option>
      ))}
    </select>
  );
}