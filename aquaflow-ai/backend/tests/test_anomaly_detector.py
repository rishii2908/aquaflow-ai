"""
Tests for AquaFlow AI anomaly detection engine.
"""

import pytest
from backend.models.anomaly_detector import AnomalyDetector


@pytest.fixture
def detector():
    return AnomalyDetector()


def test_normal_reading(detector):
    result = detector.predict(flow_rate=120.0, pressure=4.5, delta_pressure=0.1)
    assert result.is_anomaly is False
    assert result.score == 0.0


def test_high_pressure_triggers_anomaly(detector):
    result = detector.predict(flow_rate=120.0, pressure=9.5, delta_pressure=0.0)
    assert result.is_anomaly is True
    assert result.anomaly_type in ("pressure_high", "pipe_burst_risk")
    assert result.severity in ("high", "critical")


def test_low_pressure_triggers_anomaly(detector):
    result = detector.predict(flow_rate=80.0, pressure=0.8, delta_pressure=0.0)
    assert result.is_anomaly is True
    assert result.anomaly_type == "pressure_low"


def test_zero_flow_with_normal_pressure(detector):
    result = detector.predict(flow_rate=0.0, pressure=4.0, delta_pressure=0.0)
    assert result.is_anomaly is True
    assert result.anomaly_type == "leak_suspected"


def test_sudden_pressure_drop(detector):
    result = detector.predict(flow_rate=100.0, pressure=3.5, delta_pressure=-2.5)
    assert result.is_anomaly is True
    assert result.anomaly_type == "flow_drop"


def test_severity_levels(detector):
    # Critical: way above max
    r = detector.predict(flow_rate=100.0, pressure=12.0, delta_pressure=0.0)
    assert r.severity == "critical"

    # Medium-ish: just above max
    r2 = detector.predict(flow_rate=100.0, pressure=8.5, delta_pressure=0.0)
    assert r2.is_anomaly is True
