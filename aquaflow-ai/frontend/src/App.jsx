import { Routes, Route, Navigate } from "react-router-dom";
import Layout from "./components/Layout";
import DashboardPage from "./pages/DashboardPage";
import SensorsPage from "./pages/SensorsPage";
import AlertsPage from "./pages/AlertsPage";
import AnomaliesPage from "./pages/AnomaliesPage";

export default function App() {
  return (
    <Layout>
      <Routes>
        <Route path="/" element={<Navigate to="/dashboard" replace />} />
        <Route path="/dashboard" element={<DashboardPage />} />
        <Route path="/sensors" element={<SensorsPage />} />
        <Route path="/anomalies" element={<AnomaliesPage />} />
        <Route path="/alerts" element={<AlertsPage />} />
      </Routes>
    </Layout>
  );
}
