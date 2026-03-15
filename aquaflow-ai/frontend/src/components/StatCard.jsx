import styles from "./StatCard.module.css";

export default function StatCard({ label, value, unit, icon: Icon, color = "accent", trend }) {
  return (
    <div className={styles.card}>
      <div className={styles.top}>
        <span className={styles.label}>{label}</span>
        {Icon && (
          <span className={styles.icon} data-color={color}>
            <Icon size={16} />
          </span>
        )}
      </div>
      <div className={styles.value} data-color={color}>
        {value ?? "—"}
        {unit && <span className={styles.unit}>{unit}</span>}
      </div>
      {trend && <div className={styles.trend}>{trend}</div>}
    </div>
  );
}
