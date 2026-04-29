import { BrowserRouter, Routes, Route } from "react-router-dom";
import Navbar from "./components/layout/Navbar";
import Dashboard from "./pages/Dashboard";
import Forecast from "./pages/Forecast";
import Models from "./pages/Models";
import StateAnalysis from "./pages/StateAnalysis";

export default function App() {
  return (
    <BrowserRouter>
      <div className="app-container">
        <Navbar />

        <main className="main-container">
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/forecast" element={<Forecast />} />
            <Route path="/models" element={<Models />} />
            <Route path="/states" element={<StateAnalysis />} />
          </Routes>
        </main>
      </div>
    </BrowserRouter>
  );
}