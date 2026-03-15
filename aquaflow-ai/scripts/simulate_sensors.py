"""
AquaFlow AI — Sensor Simulator
Simulates real-time sensor data and POSTs it to the backend.

Usage:
    python scripts/simulate_sensors.py [--host http://localhost:8000] [--interval 2]
"""

import argparse
import asyncio
import random
import httpx
from datetime import datetime

SENSOR_NODES = [
    {"id": "S-001", "name": "Zone A - Main Inlet", "zone": "A", "latitude": 12.9716, "longitude": 77.5946},
    {"id": "S-002", "name": "Zone B - Residential", "zone": "B", "latitude": 12.9800, "longitude": 77.6000},
    {"id": "S-003", "name": "Zone C - Industrial", "zone": "C", "latitude": 12.9600, "longitude": 77.5800},
    {"id": "S-004", "name": "Zone D - Hospital", "zone": "D", "latitude": 12.9750, "longitude": 77.6100},
]

ANOMALY_SCENARIOS = [
    {"pressure": 9.8, "flow_rate": 210, "label": "pressure_burst"},
    {"pressure": 0.6, "flow_rate": 30, "label": "pressure_low"},
    {"pressure": 4.0, "flow_rate": 0, "label": "leak_suspected"},
    {"pressure": 2.0, "flow_rate": 5, "label": "combined_low"},
]


def generate_reading(inject_anomaly: bool = False):
    if inject_anomaly:
        scenario = random.choice(ANOMALY_SCENARIOS)
        return {
            "flow_rate": float(scenario["flow_rate"] + random.uniform(-5, 5)),
            "pressure": float(scenario["pressure"] + random.uniform(-0.1, 0.1)),
            "temperature": round(random.uniform(18, 28), 2),
            "timestamp": datetime.utcnow().isoformat(),
        }
    return {
        "flow_rate": round(random.uniform(80, 200), 2),
        "pressure": round(random.uniform(2.5, 7.0), 2),
        "temperature": round(random.uniform(18, 28), 2),
        "timestamp": datetime.utcnow().isoformat(),
    }


async def seed_sensors(client: httpx.AsyncClient, base: str):
    for s in SENSOR_NODES:
        try:
            r = await client.post(f"{base}/api/sensors/", json=s)
            if r.status_code == 201:
                print(f"[SEED] Created sensor {s['id']}")
            elif r.status_code == 409:
                print(f"[SEED] Sensor {s['id']} already exists")
        except Exception as e:
            print(f"[SEED] Error: {e}")


async def run(base: str, interval: float):
    async with httpx.AsyncClient(timeout=10) as client:
        await seed_sensors(client, base)
        print(f"\n[SIM] Streaming sensor data to {base} every {interval}s... (Ctrl+C to stop)\n")
        tick = 0
        while True:
            for sensor in SENSOR_NODES:
                inject = (tick % 20 == 0) and (random.random() < 0.3)
                reading = generate_reading(inject_anomaly=inject)
                try:
                    r = await client.post(f"{base}/api/sensors/{sensor['id']}/readings", json=reading)
                    data = r.json()
                    anomaly_flag = "⚠️  ANOMALY" if data.get("anomaly_detected") else "✅ OK"
                    print(
                        f"[{sensor['id']}] P={reading['pressure']} bar  F={reading['flow_rate']} L/min  {anomaly_flag}"
                        + (f"  [{data.get('anomaly_type')} / {data.get('severity')}]" if data.get("anomaly_detected") else "")
                    )
                except Exception as e:
                    print(f"[{sensor['id']}] POST failed: {e}")
            tick += 1
            await asyncio.sleep(interval)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", default="http://localhost:8000")
    parser.add_argument("--interval", type=float, default=2.0)
    args = parser.parse_args()
    asyncio.run(run(args.host, args.interval))
