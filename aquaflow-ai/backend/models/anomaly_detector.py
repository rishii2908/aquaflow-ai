"""
AquaFlow AI — Anomaly Detection Engine

Uses:
  - Z-Score rolling window for fast spike detection
  - Isolation Forest for multivariate unsupervised anomaly detection
"""

import numpy as np
import joblib
import os
from dataclasses import dataclass
from typing import Optional
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler

from backend.utils.config import settings

MODEL_PATH = os.path.join(os.path.dirname(__file__), "isolation_forest.pkl")
SCALER_PATH = os.path.join(os.path.dirname(__file__), "scaler.pkl")


@dataclass
class AnomalyResult:
    is_anomaly: bool
    score: float                    # 0.0 (normal) → 1.0 (critical anomaly)
    anomaly_type: Optional[str]
    severity: Optional[str]
    description: Optional[str]


def _severity_from_score(score: float) -> str:
    if score >= 0.85:
        return "critical"
    if score >= 0.65:
        return "high"
    if score >= 0.40:
        return "medium"
    return "low"


class AnomalyDetector:
    def __init__(self):
        self._model: Optional[IsolationForest] = None
        self._scaler: Optional[StandardScaler] = None
        self._load_or_init()

    def _load_or_init(self):
        if os.path.exists(MODEL_PATH) and os.path.exists(SCALER_PATH):
            self._model = joblib.load(MODEL_PATH)
            self._scaler = joblib.load(SCALER_PATH)
        else:
            # Bootstrap with default model — will be retrained on real data
            self._model = IsolationForest(
                n_estimators=200,
                contamination=0.05,
                random_state=42,
            )
            self._scaler = StandardScaler()

    def train(self, X: np.ndarray):
        """Train on a numpy array of shape (n_samples, n_features)."""
        X_scaled = self._scaler.fit_transform(X)
        self._model.fit(X_scaled)
        joblib.dump(self._model, MODEL_PATH)
        joblib.dump(self._scaler, SCALER_PATH)

    def _zscore_check(
        self,
        flow_rate: float,
        pressure: float,
        delta_pressure: float,
    ) -> AnomalyResult:
        """Fast rule-based checks using configured thresholds."""

        if pressure > settings.PRESSURE_MAX_BAR:
            excess = (pressure - settings.PRESSURE_MAX_BAR) / settings.PRESSURE_MAX_BAR
            score = min(0.5 + excess, 1.0)
            return AnomalyResult(
                is_anomaly=True,
                score=score,
                anomaly_type="pipe_burst_risk" if score > 0.75 else "pressure_high",
                severity=_severity_from_score(score),
                description=f"Pressure {pressure:.2f} bar exceeds safe maximum {settings.PRESSURE_MAX_BAR} bar.",
            )

        if pressure < settings.PRESSURE_MIN_BAR and pressure > 0:
            deficit = (settings.PRESSURE_MIN_BAR - pressure) / settings.PRESSURE_MIN_BAR
            score = min(0.4 + deficit, 1.0)
            return AnomalyResult(
                is_anomaly=True,
                score=score,
                anomaly_type="pressure_low",
                severity=_severity_from_score(score),
                description=f"Pressure {pressure:.2f} bar below minimum {settings.PRESSURE_MIN_BAR} bar. Possible supply irregularity.",
            )

        if flow_rate < 0 or (flow_rate == 0 and pressure > settings.PRESSURE_MIN_BAR):
            return AnomalyResult(
                is_anomaly=True,
                score=0.7,
                anomaly_type="leak_suspected",
                severity="high",
                description="Zero flow detected despite normal pressure. Possible upstream leak or blockage.",
            )

        if abs(delta_pressure) > 2.0:
            score = min(0.4 + abs(delta_pressure) / 10, 1.0)
            return AnomalyResult(
                is_anomaly=True,
                score=score,
                anomaly_type="flow_spike" if delta_pressure > 0 else "flow_drop",
                severity=_severity_from_score(score),
                description=f"Sudden pressure change of {delta_pressure:+.2f} bar detected.",
            )

        return AnomalyResult(is_anomaly=False, score=0.0, anomaly_type=None, severity=None, description=None)

    def predict(
        self,
        flow_rate: float,
        pressure: float,
        delta_pressure: float = 0.0,
        hour_of_day: int = 0,
        day_of_week: int = 0,
    ) -> AnomalyResult:
        # Fast rule-based check first
        rule_result = self._zscore_check(flow_rate, pressure, delta_pressure)
        if rule_result.is_anomaly:
            return rule_result

        # ML-based check
        try:
            features = np.array([[flow_rate, pressure, delta_pressure, hour_of_day, day_of_week]])
            if hasattr(self._scaler, "mean_"):
                features_scaled = self._scaler.transform(features)
                raw_score = self._model.score_samples(features_scaled)[0]
                # score_samples returns negative; more negative = more anomalous
                # Map to 0–1 range: typical scores are in [-0.5, 0.1]
                normalized = max(0.0, min(1.0, (-raw_score - 0.1) / 0.6))
                if normalized > 0.5:
                    return AnomalyResult(
                        is_anomaly=True,
                        score=normalized,
                        anomaly_type="leak_suspected",
                        severity=_severity_from_score(normalized),
                        description=f"ML model flagged abnormal sensor pattern (score: {normalized:.2f}).",
                    )
        except Exception:
            pass  # Model not yet trained — fall through

        return AnomalyResult(is_anomaly=False, score=0.0, anomaly_type=None, severity=None, description=None)


# Singleton
detector = AnomalyDetector()
