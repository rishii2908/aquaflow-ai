import { usePoll } from "../hooks/usePoll";
import { api } from "../utils/api";
import SeverityBadge from "../components/SeverityBadge";
import { format, parseISO } from "date-fns";
import styles from "./AnomaliesPage.module.css";

const TYPE_LABELS = {
  pressure_high:   "Pressure High",
  pressure_low:    "Pressure Low",
  flow_spike:      "Flow Spike",
  flow_drop:       "Flow Drop",
  leak_suspected:  "Leak Suspected",
  pipe_burst_risk: "Pipe Burst Risk",
};

export default function AnomaliesPage() {
  const { data: anomalies, loading } = usePoll(() => api.getAnomalies({ limit: 50 }), 8000);

  return (
    <div className={styles.page}>
      <div className={styles.header}>
        <h1 className={styles.title}>Anomaly Log</h1>
        <p className={styles.subtitle}>All detected anomalies, newest first</p>
      </div>

      {loading && <p className={styles.loading}>Loading…</p>}

      <div className={styles.tableCard}>
        <table className={styles.table}>
          <thead>
            <tr>
              <th>#</th>
              <th>Sensor</th>
              <th>Type</th>
              <th>Severity</th>
              <th>Score</th>
              <th>Description</th>
              <th>Detected</th>
            </tr>
          </thead>
          <tbody>
            {(anomalies ?? []).map((a) => (
              <tr key={a.id}>
                <td className={styles.id}>{a.id}</td>
                <td><code>{a.sensor_id}</code></td>
                <td>{TYPE_LABELS[a.anomaly_type] ?? a.anomaly_type}</td>
                <td><SeverityBadge severity={a.severity} /></td>
                <td>
                  <div className={styles.scoreBar}>
                    <div className={styles.scoreFill} style={{ width: `${a.score * 100}%`, background: a.score > 0.75 ? "var(--red)" : a.score > 0.5 ? "var(--orange)" : "var(--yellow)" }} />
                    <span>{(a.score * 100).toFixed(0)}%</span>
                  </div>
                </td>
                <td className={styles.desc}>{a.description}</td>
                <td className={styles.time}>{format(parseISO(a.detected_at), "MMM d, HH:mm:ss")}</td>
              </tr>
            ))}
          </tbody>
        </table>
        {!loading && anomalies?.length === 0 && (
          <p className={styles.empty}>No anomalies on record yet.</p>
        )}
      </div>
    </div>
  );
}
