import httpx
from src.config import settings

BACKEND_URL = settings.backend_url


def get_anomalies(start_date: str, end_date: str) -> dict:
    """Get detected anomalies and fraud alerts within a date range. Includes SIM swaps, buddy punching, and location spoofing."""
    try:
        response = httpx.get(
            f"{BACKEND_URL}/api/anomalies",
            params={"start_date": start_date, "end_date": end_date},
            timeout=5.0,
        )
        response.raise_for_status()
        return response.json()
    except Exception:
        return {
            "period": {"start": start_date, "end": end_date},
            "anomalies": [
                {
                    "id": "AN-001",
                    "type": "sim_swap",
                    "severity": "high",
                    "worker_name": "Roberto Sanchez Diaz",
                    "worker_id": "W-108",
                    "detected_at": "2026-03-03T07:20:05",
                    "site": "Obra Central Madrid",
                    "description": "SIM swap detectado en las ultimas 48 horas. La tarjeta SIM fue cambiada el 2026-03-02 a las 22:15.",
                    "status": "open",
                    "phone": "+34612345008",
                    "nokia_api_response": {
                        "swapped": True,
                        "swap_date": "2026-03-02T22:15:00Z",
                    },
                },
                {
                    "id": "AN-002",
                    "type": "location_spoofing",
                    "severity": "high",
                    "worker_name": "Isabel Romero Perez",
                    "worker_id": "W-111",
                    "detected_at": "2026-03-03T07:05:10",
                    "site": "Proyecto Norte Barcelona",
                    "description": "Ubicacion del dispositivo no coincide con el sitio de trabajo. Dispositivo detectado a 15km del sitio.",
                    "status": "open",
                    "phone": "+34612345011",
                    "nokia_api_response": {
                        "verification_result": "FALSE",
                        "device_location": {
                            "latitude": 41.4036,
                            "longitude": 2.1744,
                        },
                        "expected_location": {
                            "latitude": 41.5200,
                            "longitude": 2.1100,
                        },
                        "distance_km": 15.2,
                    },
                },
                {
                    "id": "AN-003",
                    "type": "buddy_punching",
                    "severity": "medium",
                    "worker_name": "Pablo Herrera Vega",
                    "worker_id": "W-112",
                    "detected_at": "2026-03-02T07:02:30",
                    "site": "Almacen Sur Valencia",
                    "description": "El dispositivo que ficho no corresponde al registrado para este trabajador. Posible fichaje por companero.",
                    "status": "investigating",
                    "phone": "+34612345012",
                    "nokia_api_response": {
                        "device_swap_detected": True,
                        "registered_imei": "350000000000001",
                        "detected_imei": "350000000000099",
                    },
                },
                {
                    "id": "AN-004",
                    "type": "unusual_pattern",
                    "severity": "low",
                    "worker_name": "Pedro Lopez Fernandez",
                    "worker_id": "W-103",
                    "detected_at": "2026-03-03T07:15:42",
                    "site": "Proyecto Norte Barcelona",
                    "description": "Patron de llegadas tardias recurrentes. 3 de los ultimos 5 turnos con retraso superior a 10 minutos.",
                    "status": "open",
                    "phone": "+34612345003",
                },
            ],
            "total": 4,
            "by_severity": {"high": 2, "medium": 1, "low": 1},
            "by_type": {
                "sim_swap": 1,
                "location_spoofing": 1,
                "buddy_punching": 1,
                "unusual_pattern": 1,
            },
            "source": "mock",
        }


def get_fraud_alerts() -> dict:
    """Get all active unresolved fraud alerts requiring immediate attention."""
    try:
        response = httpx.get(
            f"{BACKEND_URL}/api/alerts/fraud",
            timeout=5.0,
        )
        response.raise_for_status()
        return response.json()
    except Exception:
        return {
            "alerts": [
                {
                    "id": "FA-001",
                    "type": "sim_swap",
                    "priority": "critical",
                    "worker_name": "Roberto Sanchez Diaz",
                    "worker_id": "W-108",
                    "site": "Obra Central Madrid",
                    "created_at": "2026-03-03T07:20:05",
                    "description": "SIM swap reciente detectado. Verificacion de identidad requerida antes de validar el turno.",
                    "recommended_action": "Solicitar verificacion presencial del trabajador y comprobar documento de identidad.",
                    "status": "unresolved",
                },
                {
                    "id": "FA-002",
                    "type": "location_spoofing",
                    "priority": "critical",
                    "worker_name": "Isabel Romero Perez",
                    "worker_id": "W-111",
                    "site": "Proyecto Norte Barcelona",
                    "created_at": "2026-03-03T07:05:10",
                    "description": "Dispositivo fuera del area de trabajo. Posible falsificacion de ubicacion (GPS spoofing).",
                    "recommended_action": "Contactar al trabajador y verificar su presencia fisica en el sitio.",
                    "status": "unresolved",
                },
                {
                    "id": "FA-003",
                    "type": "buddy_punching",
                    "priority": "high",
                    "worker_name": "Pablo Herrera Vega",
                    "worker_id": "W-112",
                    "site": "Almacen Sur Valencia",
                    "created_at": "2026-03-02T07:02:30",
                    "description": "Dispositivo diferente al registrado utilizado para fichar. Sospecha de fichaje por terceros.",
                    "recommended_action": "Revisar camaras de seguridad del sitio y entrevistar al trabajador.",
                    "status": "investigating",
                },
            ],
            "total": 3,
            "critical_count": 2,
            "high_count": 1,
            "source": "mock",
        }
