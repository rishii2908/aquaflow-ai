"""
Generate sample_readings.csv with 30 days of synthetic sensor data.
Includes injected anomaly events for model training and demo.

Usage:
    python scripts/generate_sample_data.py
"""

import csv
import random
from datetime import datetime, timedelta
import os

SENSORS = ["S-001", "S-002", "S-003", "S-004"]
START = datetime(2025, 1, 1, 0, 0, 0)
DAYS = 30
INTERVAL_MINUTES = 5

ANOMALY_WINDOWS = [
    (datetime(2025, 1, 5, 14, 0), datetime(2025, 1, 5, 15, 30), "S-001", "pressure_high"),
    (datetime(2025, 1, 10, 3, 0), datetime(2025, 1, 10, 4, 0), "S-002", "leak_suspected"),
    (datetime(2025, 1, 18, 9, 0), datetime(2025, 1, 18, 10, 0), "S-003", "pressure_low"),
    (datetime(2025, 1, 25, 17, 0), datetime(2025, 1, 25, 18, 30), "S-004", "pipe_burst_risk"),
]


def in_anomaly_window(ts, sensor_id):
    for start, end, sid, atype in ANOMALY_WINDOWS:
        if sid == sensor_id and start <= ts <= end:
            return atype
    return None


rows = []
current = START
end = START + timedelta(days=DAYS)

while current < end:
    for sensor_id in SENSORS:
        atype = in_anomaly_window(current, sensor_id)
        if atype == "pressure_high":
            pressure = round(random.uniform(8.5, 10.5), 2)
            flow_rate = round(random.uniform(180, 250), 2)
        elif atype == "leak_suspected":
            pressure = round(random.uniform(3.0, 4.5), 2)
            flow_rate = round(random.uniform(0, 10), 2)
        elif atype == "pressure_low":
            pressure = round(random.uniform(0.3, 1.2), 2)
            flow_rate = round(random.uniform(20, 60), 2)
        elif atype == "pipe_burst_risk":
            pressure = round(random.uniform(9.5, 12.0), 2)
            flow_rate = round(random.uniform(200, 300), 2)
        else:
            pressure = round(random.uniform(2.5, 7.0), 2)
            flow_rate = round(random.uniform(80, 200), 2)

        rows.append({
            "sensor_id": sensor_id,
            "timestamp": current.isoformat(),
            "flow_rate": flow_rate,
            "pressure": pressure,
            "temperature": round(random.uniform(18, 28), 2),
            "anomaly_type": atype or "",
        })
    current += timedelta(minutes=INTERVAL_MINUTES)

out_path = os.path.join(os.path.dirname(__file__), "../data/sample_readings.csv")
os.makedirs(os.path.dirname(out_path), exist_ok=True)

with open(out_path, "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=["sensor_id", "timestamp", "flow_rate", "pressure", "temperature", "anomaly_type"])
    writer.writeheader()
    writer.writerows(rows)

print(f"Generated {len(rows):,} rows → {out_path}")
