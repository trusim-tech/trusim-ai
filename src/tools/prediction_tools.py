import httpx
from src.config import settings

BACKEND_URL = settings.backend_url


def predict_absences(date: str) -> dict:
    """Predict likely absences for a given date based on historical patterns. Returns workers with absence probability."""
    try:
        response = httpx.get(
            f"{BACKEND_URL}/api/predictions/absences",
            params={"date": date},
            timeout=5.0,
        )
        response.raise_for_status()
        return response.json()
    except Exception:
        return {
            "prediction_date": date,
            "model": "historical_pattern_analysis_v1",
            "predictions": [
                {
                    "worker_name": "Roberto Sanchez Diaz",
                    "worker_id": "W-108",
                    "absence_probability": 0.78,
                    "risk_level": "high",
                    "contributing_factors": [
                        "Alta frecuencia de ausencias los lunes (60%)",
                        "Bradford Factor elevado (200)",
                        "Tendencia creciente de ausencias",
                        "Ausencia no justificada el dia anterior",
                    ],
                    "suggested_action": "Contactar preventivamente al trabajador",
                },
                {
                    "worker_name": "Sofia Moreno Torres",
                    "worker_id": "W-109",
                    "absence_probability": 0.45,
                    "risk_level": "medium",
                    "contributing_factors": [
                        "Baja medica reciente por gripe",
                        "Patron de ausencias consecutivas tras baja",
                        "Bradford Factor moderado (108)",
                    ],
                    "suggested_action": "Monitorizar asistencia",
                },
                {
                    "worker_name": "Pedro Lopez Fernandez",
                    "worker_id": "W-103",
                    "absence_probability": 0.22,
                    "risk_level": "low",
                    "contributing_factors": [
                        "Patron de llegadas tardias recurrente",
                        "Historico de 1 ausencia viernes cada 3 semanas",
                    ],
                    "suggested_action": "Sin accion requerida",
                },
                {
                    "worker_name": "Luis Martinez Gomez",
                    "worker_id": "W-106",
                    "absence_probability": 0.15,
                    "risk_level": "low",
                    "contributing_factors": [
                        "Baja medica actual puede extenderse",
                    ],
                    "suggested_action": "Verificar estado de baja medica",
                },
            ],
            "expected_absent_count": 1.6,
            "recommended_backup_workers": 2,
            "source": "mock",
        }


def get_risk_scores() -> dict:
    """Get risk assessment scores for all workers based on absence patterns, verification failures, and anomalies."""
    try:
        response = httpx.get(
            f"{BACKEND_URL}/api/predictions/risk",
            timeout=5.0,
        )
        response.raise_for_status()
        return response.json()
    except Exception:
        return {
            "risk_scores": [
                {
                    "worker_name": "Roberto Sanchez Diaz",
                    "worker_id": "W-108",
                    "overall_risk": 0.85,
                    "risk_level": "critical",
                    "components": {
                        "absence_risk": 0.90,
                        "verification_risk": 0.80,
                        "anomaly_risk": 0.85,
                        "punctuality_risk": 0.70,
                    },
                    "flags": [
                        "SIM swap detectado",
                        "Bradford Factor > 150",
                        "Multiples ausencias no justificadas",
                    ],
                },
                {
                    "worker_name": "Isabel Romero Perez",
                    "worker_id": "W-111",
                    "overall_risk": 0.72,
                    "risk_level": "high",
                    "components": {
                        "absence_risk": 0.30,
                        "verification_risk": 0.90,
                        "anomaly_risk": 0.95,
                        "punctuality_risk": 0.40,
                    },
                    "flags": [
                        "Location spoofing detectado",
                        "Verificacion de ubicacion fallida",
                    ],
                },
                {
                    "worker_name": "Pablo Herrera Vega",
                    "worker_id": "W-112",
                    "overall_risk": 0.65,
                    "risk_level": "high",
                    "components": {
                        "absence_risk": 0.20,
                        "verification_risk": 0.75,
                        "anomaly_risk": 0.90,
                        "punctuality_risk": 0.50,
                    },
                    "flags": [
                        "Sospecha de buddy punching",
                        "Device swap detectado",
                    ],
                },
                {
                    "worker_name": "Sofia Moreno Torres",
                    "worker_id": "W-109",
                    "overall_risk": 0.48,
                    "risk_level": "medium",
                    "components": {
                        "absence_risk": 0.70,
                        "verification_risk": 0.10,
                        "anomaly_risk": 0.05,
                        "punctuality_risk": 0.30,
                    },
                    "flags": ["Bradford Factor moderado"],
                },
                {
                    "worker_name": "Pedro Lopez Fernandez",
                    "worker_id": "W-103",
                    "overall_risk": 0.35,
                    "risk_level": "medium",
                    "components": {
                        "absence_risk": 0.20,
                        "verification_risk": 0.10,
                        "anomaly_risk": 0.15,
                        "punctuality_risk": 0.80,
                    },
                    "flags": ["Patron de impuntualidad"],
                },
                {
                    "worker_name": "Juan Garcia Lopez",
                    "worker_id": "W-101",
                    "overall_risk": 0.05,
                    "risk_level": "low",
                    "components": {
                        "absence_risk": 0.05,
                        "verification_risk": 0.02,
                        "anomaly_risk": 0.00,
                        "punctuality_risk": 0.10,
                    },
                    "flags": [],
                },
                {
                    "worker_name": "Maria Santos Ruiz",
                    "worker_id": "W-102",
                    "overall_risk": 0.03,
                    "risk_level": "low",
                    "components": {
                        "absence_risk": 0.02,
                        "verification_risk": 0.02,
                        "anomaly_risk": 0.00,
                        "punctuality_risk": 0.05,
                    },
                    "flags": [],
                },
                {
                    "worker_name": "Ana Rodriguez Martinez",
                    "worker_id": "W-104",
                    "overall_risk": 0.04,
                    "risk_level": "low",
                    "components": {
                        "absence_risk": 0.03,
                        "verification_risk": 0.02,
                        "anomaly_risk": 0.00,
                        "punctuality_risk": 0.08,
                    },
                    "flags": [],
                },
            ],
            "summary": {
                "critical_risk_count": 1,
                "high_risk_count": 2,
                "medium_risk_count": 2,
                "low_risk_count": 3,
                "average_risk": 0.40,
            },
            "source": "mock",
        }
