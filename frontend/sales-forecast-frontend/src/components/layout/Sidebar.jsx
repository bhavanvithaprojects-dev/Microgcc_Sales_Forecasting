import { Link, useLocation } from "react-router-dom";

export default function Sidebar() {
  const location = useLocation();

  const menu = [
    { name: "Dashboard", path: "/" },
    { name: "Forecast", path: "/forecast" },
    { name: "Models", path: "/models" },
    { name: "States", path: "/states" },
  ];

  return (
    <div className="w-64 bg-gray-900 text-white min-h-screen p-6 shadow-xl flex flex-col">

      {/* Logo */}
      <div className="mb-10">
        <h1 className="text-2xl font-bold flex items-center gap-2">
          📊 Forecast
        </h1>
      </div>

      {/* Navigation */}
      <nav className="space-y-3">
        {menu.map((item) => (
          <Link
            key={item.path}
            to={item.path}
            className={`block px-4 py-3 rounded-xl transition-all ${
              location.pathname === item.path
                ? "bg-blue-500 text-white shadow-md"
                : "hover:bg-gray-700 text-gray-300"
            }`}
          >
            {item.name}
          </Link>
        ))}
      </nav>

      {/* Footer */}
      <div className="mt-auto text-sm text-gray-400 pt-10">
        © 2026 Forecast System
      </div>

    </div>
  );
}