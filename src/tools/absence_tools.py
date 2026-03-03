import httpx
from src.config import settings

BACKEND_URL = settings.backend_url


def get_absences(start_date: str, end_date: str) -> dict:
    """Get all recorded absences within a date range. Returns absence type, worker, date, and justification status."""
    try:
        response = httpx.get(
            f"{BACKEND_URL}/api/absences",
            params={"start_date": start_date, "end_date": end_date},
            timeout=5.0,
        )
        response.raise_for_status()
        return response.json()
    except Exception:
        return {
            "period": {"start": start_date, "end": end_date},
            "absences": [
                {
                    "id": "ABS-001",
                    "worker_name": "Luis Martinez Gomez",
                    "worker_id": "W-106",
                    "date": "2026-03-03",
                    "type": "sick_leave",
                    "justified": True,
                    "justification": "Certificado medico presentado",
                    "site": "Obra Central Madrid",
                },
                {
                    "id": "ABS-002",
                    "worker_name": "Elena Fernandez Castro",
                    "worker_id": "W-107",
                    "date": "2026-03-03",
                    "type": "personal",
                    "justified": True,
                    "justification": "Permiso personal aprobado",
                    "site": "Proyecto Norte Barcelona",
                },
                {
                    "id": "ABS-003",
                    "worker_name": "Roberto Sanchez Diaz",
                    "worker_id": "W-108",
                    "date": "2026-03-03",
                    "type": "no_show",
                    "justified": False,
                    "justification": None,
                    "site": "Almacen Sur Valencia",
                },
                {
                    "id": "ABS-004",
                    "worker_name": "Sofia Moreno Torres",
                    "worker_id": "W-109",
                    "date": "2026-03-02",
                    "type": "sick_leave",
                    "justified": True,
                    "justification": "Baja temporal por gripe",
                    "site": "Obra Central Madrid",
                },
                {
                    "id": "ABS-005",
                    "worker_name": "Roberto Sanchez Diaz",
                    "worker_id": "W-108",
                    "date": "2026-03-01",
                    "type": "no_show",
                    "justified": False,
                    "justification": None,
                    "site": "Almacen Sur Valencia",
                },
                {
                    "id": "ABS-006",
                    "worker_name": "Fernando Navarro Gil",
                    "worker_id": "W-110",
                    "date": "2026-02-28",
                    "type": "vacation",
                    "justified": True,
                    "justification": "Vacaciones programadas",
                    "site": "Proyecto Norte Barcelona",
                },
            ],
            "total": 6,
            "justified_count": 4,
            "unjustified_count": 2,
            "source": "mock",
        }


def get_absence_patterns(worker_name: str) -> dict:
    """Analyze absence patterns for a specific worker. Returns day-of-week frequency, trend, and Bradford Factor score."""
    try:
        response = httpx.get(
            f"{BACKEND_URL}/api/absences/patterns",
            params={"worker_name": worker_name},
            timeout=5.0,
        )
        response.raise_for_status()
        return response.json()
    except Exception:
        return {
            "worker_name": worker_name,
            "total_absences_30d": 4,
            "total_absences_90d": 7,
            "day_of_week_frequency": {
                "lunes": 3,
                "martes": 1,
                "miercoles": 0,
                "jueves": 1,
                "viernes": 2,
                "sabado": 0,
                "domingo": 0,
            },
            "trend": "increasing",
            "trend_description": "Las ausencias han aumentado un 40% en los ultimos 30 dias respecto al periodo anterior",
            "bradford_factor": 48,
            "bradford_interpretation": "Nivel de atencion - patron de ausencias cortas y frecuentes",
            "most_common_type": "no_show",
            "justified_rate": 0.43,
            "consecutive_max": 2,
            "source": "mock",
        }


def get_bradford_scores() -> dict:
    """Get Bradford Factor scores for all workers. Higher scores indicate problematic absence patterns. Returns ranked list."""
    try:
        response = httpx.get(
            f"{BACKEND_URL}/api/absences/bradford",
            timeout=5.0,
        )
        response.raise_for_status()
        return response.json()
    except Exception:
        return {
            "scores": [
                {
                    "worker_name": "Roberto Sanchez Diaz",
                    "worker_id": "W-108",
                    "bradford_score": 200,
                    "absences_30d": 5,
                    "episodes_30d": 4,
                    "risk_level": "high",
                    "trend": "increasing",
                },
                {
                    "worker_name": "Sofia Moreno Torres",
                    "worker_id": "W-109",
                    "bradford_score": 108,
                    "absences_30d": 4,
                    "episodes_30d": 3,
                    "risk_level": "medium",
                    "trend": "stable",
                },
                {
                    "worker_name": "Luis Martinez Gomez",
                    "worker_id": "W-106",
                    "bradford_score": 50,
                    "absences_30d": 2,
                    "episodes_30d": 2,
                    "risk_level": "medium",
                    "trend": "stable",
                },
                {
                    "worker_name": "Fernando Navarro Gil",
                    "worker_id": "W-110",
                    "bradford_score": 16,
                    "absences_30d": 2,
                    "episodes_30d": 1,
                    "risk_level": "low",
                    "trend": "stable",
                },
                {
                    "worker_name": "Elena Fernandez Castro",
                    "worker_id": "W-107",
                    "bradford_score": 9,
                    "absences_30d": 1,
                    "episodes_30d": 1,
                    "risk_level": "low",
                    "trend": "decreasing",
                },
                {
                    "worker_name": "Juan Garcia Lopez",
                    "worker_id": "W-101",
                    "bradford_score": 0,
                    "absences_30d": 0,
                    "episodes_30d": 0,
                    "risk_level": "none",
                    "trend": "stable",
                },
                {
                    "worker_name": "Maria Santos Ruiz",
                    "worker_id": "W-102",
                    "bradford_score": 0,
                    "absences_30d": 0,
                    "episodes_30d": 0,
                    "risk_level": "none",
                    "trend": "stable",
                },
                {
                    "worker_name": "Pedro Lopez Fernandez",
                    "worker_id": "W-103",
                    "bradford_score": 4,
                    "absences_30d": 1,
                    "episodes_30d": 1,
                    "risk_level": "low",
                    "trend": "stable",
                },
                {
                    "worker_name": "Ana Rodriguez Martinez",
                    "worker_id": "W-104",
                    "bradford_score": 0,
                    "absences_30d": 0,
                    "episodes_30d": 0,
                    "risk_level": "none",
                    "trend": "stable",
                },
                {
                    "worker_name": "Carlos Ruiz Hernandez",
                    "worker_id": "W-105",
                    "bradford_score": 4,
                    "absences_30d": 1,
                    "episodes_30d": 1,
                    "risk_level": "low",
                    "trend": "stable",
                },
            ],
            "average_score": 39.1,
            "high_risk_count": 1,
            "medium_risk_count": 2,
            "source": "mock",
        }
