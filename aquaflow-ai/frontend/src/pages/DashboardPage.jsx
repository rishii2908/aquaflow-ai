import { usePoll } from "../hooks/usePoll";
import { api } from "../utils/api";
import StatCard from "../components/StatCard";
import SeverityBadge from "../components/SeverityBadge";
import {
  LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer, CartesianGrid
} from "recharts";
import { Activity, Droplets, AlertTriangle, Bell, Zap } from "lucide-react";
import { format, parseISO } from "date-fns";
import styles from "./DashboardPage.module.css";

function useMockChartData() {
  // Returns synthetic 24-pt time series for demo purposes when API not yet wired
  const now = Date.now();
  return Array.from({ length: 24 }, (_, i) => ({
    time: format(new Date(now - (23 - i) * 5 * 60 * 1000), "HH:mm"),
    pressure: +(3 + Math.sin(i / 3) * 1.5 + Math.random() * 0.4).toFixed(2),
    flow: +(120 + Math.cos(i / 4) * 30 + Math.random() * 10).toFixed(1),
  }));
}

export default function DashboardPage() {
  const { data: summary } = usePoll(api.getSummary, 10000);
  const { data: alerts } = usePoll(() => api.getAlerts(true), 8000);
  const { data: anomalies } = usePoll(() => api.getAnomalies({ limit: 5 }), 8000);
  const chartData = useMockChartData();

  return (
    <div className={styles.page}>
      <div className={styles.header}>
        <div>
          <h1 className={styles.title}>System Overview</h1>
          <p className={styles.subtitle}>Real-time water distribution monitoring</p>
        </div>
        <div className={styles.liveChip}>
          <span className={styles.dot} />
          Live
        </div>
      </div>

      {/* KPI row */}
      <div className={styles.statsGrid}>
        <StatCard
          label="Active Sensors"
          value={summary?.active_sensors ?? "—"}
          icon={Activity}
          color="accent"
          trend={`of ${summary?.total_sensors ?? "?"} total`}
        />
        <StatCard
          label="Readings (24h)"
          value={summary?.readings_last_24h?.toLocaleString() ?? "—"}
          icon={Droplets}
          color="green"
        />
        <StatCard
          label="Anomalies (24h)"
          value={summary?.anomalies_last_24h ?? "—"}
          icon={AlertTriangle}
          color={summary?.anomalies_last_24h > 5 ? "orange" : "yellow"}
        />
        <StatCard
          label="Open Alerts"
          value={summary?.open_alerts ?? "—"}
          icon={Bell}
          color={summary?.critical_alerts > 0 ? "red" : "yellow"}
          trend={summary?.critical_alerts > 0 ? `${summary.critical_alerts} critical` : "none critical"}
        />
        <StatCard
          label="Energy Savings Est."
          value="~20"
          unit="%"
          icon={Zap}
          color="green"
          trend="vs. baseline (predictive mode)"
        />
      </div>

      {/* Charts */}
      <div className={styles.chartsRow}>
        <div className={styles.chartCard}>
          <h2 className={styles.cardTitle}>Pressure (bar) — Zone A, last 2h</h2>
          <ResponsiveContainer width="100%" height={200}>
            <LineChart data={chartData}>
              <CartesianGrid strokeDasharray="3 3" stroke="#0e3a5a" />
              <XAxis dataKey="time" tick={{ fill: "#5a8aaa", fontSize: 11 }} />
              <YAxis domain={[0, 10]} tick={{ fill: "#5a8aaa", fontSize: 11 }} />
              <Tooltip
                contentStyle={{ background: "#0a1929", border: "1px solid #0e3a5a", borderRadius: 8 }}
                labelStyle={{ color: "#d4eaf7" }}
              />
              <Line type="monotone" dataKey="pressure" stroke="#00c8ff" strokeWidth={2} dot={false} />
            </LineChart>
          </ResponsiveContainer>
        </div>

        <div className={styles.chartCard}>
          <h2 className={styles.cardTitle}>Flow Rate (L/min) — Zone A, last 2h</h2>
          <ResponsiveContainer width="100%" height={200}>
            <LineChart data={chartData}>
              <CartesianGrid strokeDasharray="3 3" stroke="#0e3a5a" />
              <XAxis dataKey="time" tick={{ fill: "#5a8aaa", fontSize: 11 }} />
              <YAxis tick={{ fill: "#5a8aaa", fontSize: 11 }} />
              <Tooltip
                contentStyle={{ background: "#0a1929", border: "1px solid #0e3a5a", borderRadius: 8 }}
                labelStyle={{ color: "#d4eaf7" }}
              />
              <Line type="monotone" dataKey="flow" stroke="#00e5a0" strokeWidth={2} dot={false} />
            </LineChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Recent anomalies */}
      <div className={styles.tableCard}>
        <h2 className={styles.cardTitle}>Recent Anomalies</h2>
        {anomalies && anomalies.length > 0 ? (
          <table className={styles.table}>
            <thead>
              <tr>
                <th>Sensor</th>
                <th>Type</th>
                <th>Severity</th>
                <th>Score</th>
                <th>Detected</th>
              </tr>
            </thead>
            <tbody>
              {anomalies.map((a) => (
                <tr key={a.id}>
                  <td><code>{a.sensor_id}</code></td>
                  <td>{a.anomaly_type?.replace(/_/g, " ")}</td>
                  <td><SeverityBadge severity={a.severity} /></td>
                  <td>{(a.score * 100).toFixed(0)}%</td>
                  <td>{format(parseISO(a.detected_at), "MMM d, HH:mm")}</td>
                </tr>
              ))}
            </tbody>
          </table>
        ) : (
          <p className={styles.empty}>No anomalies detected yet. Run the sensor simulator to generate data.</p>
        )}
      </div>
    </div>
  );
}
