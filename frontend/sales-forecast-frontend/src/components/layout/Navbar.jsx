import { Link, useLocation } from "react-router-dom";

export default function Navbar() {
  const location = useLocation();

  const menu = [
    { name: "Dashboard", path: "/" },
    { name: "Forecast", path: "/forecast" },
    { name: "Models", path: "/models" },
    { name: "States", path: "/states" },
  ];

  return (
    <nav className="navbar">
      <Link to="/" className="nav-logo" id="main-logo">
        📊 <span>SALES FORECAST</span>
      </Link>

      <div className="nav-links">
        {menu.map((item) => (
          <Link
            key={item.path}
            to={item.path}
            className={`nav-link ${location.pathname === item.path ? "active" : ""}`}
          >
            {item.name}
          </Link>
        ))}
      </div>

      <div style={{ color: 'var(--text-secondary)', fontSize: '0.8rem', fontWeight: 500 }}>
        © 2026 Forecast System
      </div>
    </nav>
  );
}
