# AquaFlow AI — System Architecture

## Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                        AquaFlow AI System                        │
└─────────────────────────────────────────────────────────────────┘

  Pipeline Sensors (IoT)
       │  flow_rate, pressure, temperature
       ▼
  ┌──────────────┐     POST /api/sensors/{id}/readings
  │  Sensor Edge  │ ─────────────────────────────────────►
  │   Devices     │                                        │
  └──────────────┘                                        ▼
                                              ┌─────────────────────┐
                                              │   FastAPI Backend    │
                                              │                      │
                                              │  ┌────────────────┐  │
                                              │  │ Ingestion Svc  │  │
                                              │  └───────┬────────┘  │
                                              │          │            │
                                              │  ┌───────▼────────┐  │
                                              │  │ Anomaly Engine │  │
                                              │  │                │  │
                                              │  │ • Z-Score rules│  │
                                              │  │ • Isolation    │  │
                                              │  │   Forest (ML)  │  │
                                              │  └───────┬────────┘  │
                                              │          │            │
                                              │  ┌───────▼────────┐  │
                                              │  │   SQLite DB    │  │
                                              │  │                │  │
                                              │  │ sensors        │  │
                                              │  │ readings       │  │
                                              │  │ anomalies      │  │
                                              │  │ alerts         │  │
                                              │  └────────────────┘  │
                                              └──────────┬───────────┘
                                                         │  REST API
                                                         ▼
                                              ┌─────────────────────┐
                                              │   React Dashboard    │
                                              │                      │
                                              │  • Live KPI cards    │
                                              │  • Pressure/flow     │
                                              │    time series       │
                                              │  • Anomaly log       │
                                              │  • Alert management  │
                                              └─────────────────────┘
```

## Data Flow

1. **Sensor Ingestion** — Sensors POST readings every N seconds to `/api/sensors/{id}/readings`
2. **Anomaly Detection** — Each reading is immediately evaluated:
   - Rule engine (Z-Score thresholds) for instant detection of extreme values
   - Isolation Forest ML model for multivariate pattern anomalies
3. **Alert Generation** — Medium/High/Critical anomalies auto-generate operator alerts
4. **Dashboard Polling** — Frontend polls API every 5–10s for live updates

## ML Model Details

| Component | Detail |
|---|---|
| Algorithm | Isolation Forest (sklearn) |
| Features | flow_rate, pressure, delta_pressure, hour_of_day, day_of_week |
| Contamination | 5% (tunable via retraining) |
| Fallback | Rule-based Z-Score thresholds (always active) |
| Persistence | joblib pickle (backend/models/*.pkl) |

## API Endpoints

```
GET    /api/sensors/                          List all sensors
POST   /api/sensors/                          Register sensor
GET    /api/sensors/{id}                      Get sensor details
GET    /api/sensors/{id}/readings?limit=N     Get recent readings
POST   /api/sensors/{id}/readings             Ingest new reading → triggers detection

GET    /api/anomalies/?sensor_id=&severity=   Query anomalies
GET    /api/alerts/?unacknowledged_only=true  Query alerts
POST   /api/alerts/{id}/acknowledge           Acknowledge alert

GET    /api/reports/summary                   24h system health summary
```

## Deployment

- **Dev**: SQLite + uvicorn + Vite dev server
- **Production**: Replace SQLite with PostgreSQL, serve frontend via Nginx, use gunicorn/uvicorn workers
- **Scaling**: Sensor ingestion can be fronted by an MQTT broker or Kafka topic for high-volume deployments
