import styles from "./SeverityBadge.module.css";

const MAP = {
  critical: { label: "Critical", color: "red" },
  high:     { label: "High",     color: "orange" },
  medium:   { label: "Medium",   color: "yellow" },
  low:      { label: "Low",      color: "green" },
};

export default function SeverityBadge({ severity }) {
  const { label, color } = MAP[severity] ?? { label: severity, color: "accent" };
  return (
    <span className={styles.badge} data-color={color}>
      {label}
    </span>
  );
}
