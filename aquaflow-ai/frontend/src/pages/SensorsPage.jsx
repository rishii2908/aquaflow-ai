import { usePoll } from "../hooks/usePoll";
import { api } from "../utils/api";
import { Radio, CheckCircle, XCircle } from "lucide-react";
import styles from "./SensorsPage.module.css";

export default function SensorsPage() {
  const { data: sensors, loading } = usePoll(api.getSensors, 15000);

  return (
    <div className={styles.page}>
      <div className={styles.header}>
        <h1 className={styles.title}>Sensor Nodes</h1>
        <p className={styles.subtitle}>All registered pipeline sensors across zones</p>
      </div>

      {loading && <p className={styles.loading}>Loading sensors…</p>}

      <div className={styles.grid}>
        {(sensors ?? []).map((s) => (
          <div key={s.id} className={styles.card}>
            <div className={styles.cardTop}>
              <span className={styles.sensorId}>{s.id}</span>
              {s.is_active
                ? <CheckCircle size={16} color="var(--green)" />
                : <XCircle size={16} color="var(--red)" />}
            </div>
            <div className={styles.sensorName}>{s.name}</div>
            <div className={styles.zone}>
              <Radio size={12} /> Zone {s.zone}
            </div>
            <div className={styles.coords}>
              {s.latitude.toFixed(4)}, {s.longitude.toFixed(4)}
            </div>
          </div>
        ))}

        {!loading && sensors?.length === 0 && (
          <p className={styles.empty}>
            No sensors registered. Run <code>scripts/simulate_sensors.py</code> to seed data.
          </p>
        )}
      </div>
    </div>
  );
}
