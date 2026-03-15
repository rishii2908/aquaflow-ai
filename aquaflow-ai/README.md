# 💧 AquaFlow AI

> Intelligent water pipeline monitoring with real-time anomaly detection and predictive maintenance.

![Python](https://img.shields.io/badge/Python-3.10+-blue?style=flat-square)
![FastAPI](https://img.shields.io/badge/FastAPI-0.110-green?style=flat-square)
![React](https://img.shields.io/badge/React-18-61DAFB?style=flat-square)
![License](https://img.shields.io/badge/License-MIT-yellow?style=flat-square)

---

## 🌊 Problem

Urban water distribution systems lose **30–40% of treated water** due to undetected leaks, aging pipelines, and manual inspection delays. Around **60% of pipeline failures** are caused by pressure fluctuations — pipe bursts from excess pressure, irregular supply from low pressure.

**AquaFlow AI** uses sensor telemetry, real-time monitoring, and ML-based anomaly detection to catch failures *before* they happen.

---

## ✅ Expected Outcomes

| Metric | Improvement |
|---|---|
| Water Leakage Reduction | 25–35% |
| Pressure Variation Stability | ~40% |
| Pumping Energy Savings | 15–25% |

---

## 🏗️ Architecture

```
aquaflow-ai/
├── backend/               # FastAPI server
│   ├── models/            # ML anomaly detection models
│   ├── routes/            # API endpoints
│   ├── services/          # Business logic (sensor ingestion, alerting)
│   └── utils/             # Helpers (logging, config)
├── frontend/              # React dashboard
│   └── src/
│       ├── components/    # UI components
│       ├── pages/         # Dashboard, Alerts, Reports
│       └── hooks/         # Custom React hooks
├── data/                  # Sample sensor datasets
├── docs/                  # Architecture diagrams, API docs
└── scripts/               # Setup, simulation, seed scripts
```

---

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- Node.js 18+
- (Optional) Docker & Docker Compose

### 1. Clone the repo
```bash
git clone https://github.com/your-org/aquaflow-ai.git
cd aquaflow-ai
```

### 2. Backend setup
```bash
cd backend
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload
```
Backend runs at: `http://localhost:8000`  
API docs at: `http://localhost:8000/docs`

### 3. Frontend setup
```bash
cd frontend
npm install
npm run dev
```
Dashboard runs at: `http://localhost:5173`

### 4. Run sensor simulation
```bash
python scripts/simulate_sensors.py
```

### Docker (all-in-one)
```bash
docker-compose up --build
```

---

## 🔌 API Overview

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/sensors` | List all sensor nodes |
| GET | `/api/sensors/{id}/readings` | Latest readings for a sensor |
| POST | `/api/sensors/{id}/readings` | Ingest new sensor data |
| GET | `/api/anomalies` | All detected anomalies |
| GET | `/api/alerts` | Active operator alerts |
| POST | `/api/alerts/{id}/acknowledge` | Acknowledge an alert |
| GET | `/api/reports/summary` | System health summary |

---

## 🤖 ML Model

The anomaly detection engine (`backend/models/anomaly_detector.py`) uses:

- **Isolation Forest** — unsupervised outlier detection on pressure/flow time series
- **Z-Score thresholding** — fast rolling window detection for sudden spikes
- **LSTM (optional)** — sequence model for temporal pattern anomalies

Features used per reading:
- `flow_rate` (L/min)
- `pressure` (bar)
- `delta_pressure` (change vs last reading)
- `hour_of_day`, `day_of_week` (temporal context)

---

## 📊 Dashboard Features

- **Live sensor map** — zone-level status with color-coded health indicators
- **Pressure & flow charts** — real-time time series per sensor node
- **Anomaly feed** — ranked list of detected anomalies with severity scores
- **Alert management** — acknowledge, escalate, and resolve alerts
- **Reports** — daily/weekly summaries, leak event history

---

## 🧪 Testing

```bash
# Backend tests
cd backend
pytest tests/ -v

# Frontend tests
cd frontend
npm run test
```

---

## 📁 Sample Data

`data/sample_readings.csv` — 30 days of synthetic sensor readings with injected anomaly events for model training and demo purposes.

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Commit changes: `git commit -m "feat: add your feature"`
4. Push and open a Pull Request

Please follow [Conventional Commits](https://www.conventionalcommits.org/).

---

## 📄 License

MIT © 2025 AquaFlow AI Team
