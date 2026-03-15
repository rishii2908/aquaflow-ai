import { useState } from "react";
import { usePoll } from "../hooks/usePoll";
import { api } from "../utils/api";
import SeverityBadge from "../components/SeverityBadge";
import { format, parseISO } from "date-fns";
import { CheckCheck } from "lucide-react";
import styles from "./AlertsPage.module.css";

export default function AlertsPage() {
  const [showAll, setShowAll] = useState(false);
  const { data: alerts, loading, refresh } = usePoll(
    () => api.getAlerts(!showAll),
    8000,
    [showAll]
  );

  async function acknowledge(id) {
    const name = prompt("Enter your name to acknowledge this alert:") || "Operator";
    await api.acknowledgeAlert(id, name);
    refresh();
  }

  return (
    <div className={styles.page}>
      <div className={styles.header}>
        <div>
          <h1 className={styles.title}>Alert Management</h1>
          <p className={styles.subtitle}>Operator alerts requiring attention</p>
        </div>
        <label className={styles.toggle}>
          <input
            type="checkbox"
            checked={showAll}
            onChange={(e) => setShowAll(e.target.checked)}
          />
          Show acknowledged
        </label>
      </div>

      {loading && <p className={styles.loading}>Loading…</p>}

      <div className={styles.list}>
        {(alerts ?? []).map((a) => (
          <div key={a.id} className={`${styles.alertRow} ${a.is_acknowledged ? styles.acked : ""}`}>
            <div className={styles.alertLeft}>
              <SeverityBadge severity={a.severity} />
              <code className={styles.sensorId}>{a.sensor_id}</code>
              <span className={styles.message}>{a.message}</span>
            </div>
            <div className={styles.alertRight}>
              <span className={styles.time}>{format(parseISO(a.created_at), "MMM d, HH:mm")}</span>
              {a.is_acknowledged ? (
                <span className={styles.ackedLabel}>
                  <CheckCheck size={13} /> {a.acknowledged_by}
                </span>
              ) : (
                <button className={styles.ackBtn} onClick={() => acknowledge(a.id)}>
                  Acknowledge
                </button>
              )}
            </div>
          </div>
        ))}

        {!loading && alerts?.length === 0 && (
          <p className={styles.empty}>
            {showAll ? "No alerts on record." : "🎉 No open alerts — all clear!"}
          </p>
        )}
      </div>
    </div>
  );
}
