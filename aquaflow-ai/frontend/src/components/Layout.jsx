import { NavLink } from "react-router-dom";
import { LayoutDashboard, Radio, AlertTriangle, Bell } from "lucide-react";
import styles from "./Layout.module.css";

const NAV = [
  { to: "/dashboard", icon: LayoutDashboard, label: "Dashboard" },
  { to: "/sensors",   icon: Radio,           label: "Sensors"   },
  { to: "/anomalies", icon: AlertTriangle,   label: "Anomalies" },
  { to: "/alerts",    icon: Bell,            label: "Alerts"    },
];

export default function Layout({ children }) {
  return (
    <div className={styles.shell}>
      <aside className={styles.sidebar}>
        <div className={styles.logo}>
          <span className={styles.drop}>💧</span>
          <div>
            <div className={styles.logoName}>AquaFlow</div>
            <div className={styles.logoSub}>AI Monitor</div>
          </div>
        </div>

        <nav className={styles.nav}>
          {NAV.map(({ to, icon: Icon, label }) => (
            <NavLink
              key={to}
              to={to}
              className={({ isActive }) =>
                `${styles.navItem} ${isActive ? styles.active : ""}`
              }
            >
              <Icon size={18} />
              <span>{label}</span>
            </NavLink>
          ))}
        </nav>

        <div className={styles.sidebarFooter}>
          <span className={styles.pulse} />
          <span>Live monitoring</span>
        </div>
      </aside>

      <main className={styles.main}>{children}</main>
    </div>
  );
}
