"""
MONITORING MODULE
- Data drift detection using Population Stability Index (PSI)
- Prediction drift monitoring
- Alert generation
- Production-safe (no heavy dependencies)
"""

import pandas as pd
import numpy as np
import json
import time
from pathlib import Path
from typing import Dict, List
from dataclasses import dataclass, asdict
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


# ─── PSI Calculation ─────────────────────────────────────────────────────────
def calculate_psi(expected: np.ndarray, actual: np.ndarray, buckets: int = 10) -> float:
    """
    Population Stability Index.
    PSI < 0.10 → No drift
    0.10–0.25 → Moderate drift
    > 0.25 → Significant drift
    """

    def _bucketize(arr, bins):
        counts, _ = np.histogram(arr, bins=bins)
        counts = np.clip(counts, 1e-6, None)  # avoid log(0)
        return counts / counts.sum()

    if len(expected) == 0 or len(actual) == 0:
        return 0.0

    _, bins = np.histogram(expected, bins=buckets)
    bins[0], bins[-1] = -np.inf, np.inf

    p_expected = _bucketize(expected, bins)
    p_actual = _bucketize(actual, bins)

    psi = np.sum((p_actual - p_expected) * np.log(p_actual / p_expected))
    return round(float(psi), 4)


# ─── Alert Dataclass ─────────────────────────────────────────────────────────
@dataclass
class DriftAlert:
    timestamp: str
    feature: str
    psi_score: float
    severity: str  # INFO / WARNING / CRITICAL
    message: str


# ─── Monitor Class ───────────────────────────────────────────────────────────
class ModelMonitor:

    PSI_THRESHOLDS = {
        "INFO": 0.0,
        "WARNING": 0.10,
        "CRITICAL": 0.25,
    }

    def __init__(self, reference_df: pd.DataFrame, output_dir: str = "monitoring"):
        self.reference_df = reference_df
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.alerts: List[DriftAlert] = []

    def _severity(self, psi: float) -> str:
        if psi >= self.PSI_THRESHOLDS["CRITICAL"]:
            return "CRITICAL"
        elif psi >= self.PSI_THRESHOLDS["WARNING"]:
            return "WARNING"
        return "INFO"

    # ─── Feature Drift ────────────────────────────────────────────────────────
    def check_feature_drift(
        self,
        production_df: pd.DataFrame,
        numeric_cols: List[str],
    ) -> Dict[str, float]:

        results = {}

        for col in numeric_cols:
            if col not in self.reference_df.columns or col not in production_df.columns:
                continue

            ref = self.reference_df[col].dropna().values
            prod = production_df[col].dropna().values

            if len(ref) < 10 or len(prod) < 10:
                continue

            psi = calculate_psi(ref, prod)
            severity = self._severity(psi)
            results[col] = psi

            if severity != "INFO":
                message = f"{col} drift detected: PSI={psi:.3f}"

                alert = DriftAlert(
                    timestamp=time.strftime("%Y-%m-%dT%H:%M:%S"),
                    feature=col,
                    psi_score=psi,
                    severity=severity,
                    message=message,
                )

                self.alerts.append(alert)
                logger.warning(f"[{severity}] {message}")

        return results

    # ─── Prediction Drift ─────────────────────────────────────────────────────
    def check_prediction_drift(
        self,
        ref_probas: np.ndarray,
        prod_probas: np.ndarray,
    ) -> float:

        psi = calculate_psi(ref_probas, prod_probas)
        severity = self._severity(psi)

        logger.info(f"Prediction drift PSI={psi:.3f} [{severity}]")

        if severity != "INFO":
            message = f"Prediction score drift: PSI={psi:.3f}"

            self.alerts.append(
                DriftAlert(
                    timestamp=time.strftime("%Y-%m-%dT%H:%M:%S"),
                    feature="PREDICTION",
                    psi_score=psi,
                    severity=severity,
                    message=message,
                )
            )

        return psi

    # ─── Performance Drift ────────────────────────────────────────────────────
    def check_performance_degradation(
        self,
        y_true,
        y_pred,
        baseline_f1: float = 0.70,
        threshold: float = 0.05,
    ) -> bool:

        from sklearn.metrics import f1_score

        current_f1 = f1_score(y_true, y_pred)
        degraded = current_f1 < (baseline_f1 - threshold)

        if degraded:
            message = f"F1 degraded: {current_f1:.3f} (baseline={baseline_f1})"

            self.alerts.append(
                DriftAlert(
                    timestamp=time.strftime("%Y-%m-%dT%H:%M:%S"),
                    feature="PERFORMANCE",
                    psi_score=0.0,
                    severity="CRITICAL",
                    message=message,
                )
            )

            logger.critical(
                f"Model performance degradation! F1={current_f1:.3f}"
            )

        return degraded

    # ─── Save Report ──────────────────────────────────────────────────────────
    def save_report(self) -> str:

        report = {
            "generated_at": time.strftime("%Y-%m-%dT%H:%M:%S"),
            "total_alerts": len(self.alerts),
            "critical": sum(1 for a in self.alerts if a.severity == "CRITICAL"),
            "warnings": sum(1 for a in self.alerts if a.severity == "WARNING"),
            "alerts": [asdict(a) for a in self.alerts],
        }

        path = self.output_dir / f"report_{int(time.time())}.json"

        with open(path, "w") as f:
            json.dump(report, f, indent=2)

        logger.info(f"Monitoring report saved: {path}")
        return str(path)

    # ─── Alert Stub ───────────────────────────────────────────────────────────
    def send_alert(self, alert: DriftAlert) -> None:
        logger.info(f"[ALERT STUB] Would send: {alert.message}")