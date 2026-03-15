"""
AquaFlow AI — Train Isolation Forest on sample_readings.csv

Usage:
    python scripts/train_model.py [--data data/sample_readings.csv]
"""

import argparse
import os
import sys
import numpy as np
import pandas as pd

# Allow running from project root
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.models.anomaly_detector import AnomalyDetector


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", default="data/sample_readings.csv")
    args = parser.parse_args()

    if not os.path.exists(args.data):
        print(f"[ERROR] Data file not found: {args.data}")
        print("Run `python scripts/generate_sample_data.py` first.")
        sys.exit(1)

    print(f"[TRAIN] Loading data from {args.data}...")
    df = pd.read_csv(args.data, parse_dates=["timestamp"])

    # Feature engineering
    df = df.sort_values(["sensor_id", "timestamp"])
    df["delta_pressure"] = df.groupby("sensor_id")["pressure"].diff().fillna(0)
    df["hour_of_day"] = df["timestamp"].dt.hour
    df["day_of_week"] = df["timestamp"].dt.dayofweek

    features = ["flow_rate", "pressure", "delta_pressure", "hour_of_day", "day_of_week"]
    X = df[features].dropna().values

    print(f"[TRAIN] Training on {len(X):,} samples with features: {features}")
    detector = AnomalyDetector()
    detector.train(X)

    print("[TRAIN] ✅ Model trained and saved to backend/models/")
    print(f"         isolation_forest.pkl + scaler.pkl")

    # Quick evaluation on injected anomalies
    anomaly_rows = df[df["anomaly_type"] != ""]
    if len(anomaly_rows) > 0:
        print(f"\n[EVAL] Testing on {len(anomaly_rows)} known anomaly samples...")
        detected = 0
        for _, row in anomaly_rows.iterrows():
            result = detector.predict(
                flow_rate=row["flow_rate"],
                pressure=row["pressure"],
                delta_pressure=row["delta_pressure"],
                hour_of_day=int(row["hour_of_day"]),
                day_of_week=int(row["day_of_week"]),
            )
            if result.is_anomaly:
                detected += 1
        recall = detected / len(anomaly_rows) * 100
        print(f"[EVAL] Recall on injected anomalies: {recall:.1f}% ({detected}/{len(anomaly_rows)})")


if __name__ == "__main__":
    main()
