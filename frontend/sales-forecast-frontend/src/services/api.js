const BASE_URL = "http://localhost:8000";

export const fetchStates = async () => {
  const response = await fetch(`${BASE_URL}/states`);
  const data = await response.json();
  return data.states;
};

export const fetchDashboardData = async (state = "All States", date = "") => {
  const url = new URL(`${BASE_URL}/dashboard`);
  url.searchParams.append("state", state);
  if (date) url.searchParams.append("date", date);
  
  const response = await fetch(url);
  const data = await response.json();
  return data;
};

export const fetchModelsData = async () => {
  const response = await fetch(`${BASE_URL}/models`);
  const data = await response.json();
  return data.models;
};

export const fetchCompareStates = async (state1, state2) => {
  const response = await fetch(`${BASE_URL}/compare-states?state1=${state1}&state2=${state2}`);
  const data = await response.json();
  return data;
};
