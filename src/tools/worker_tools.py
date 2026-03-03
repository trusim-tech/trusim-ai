import httpx
from src.config import settings

BACKEND_URL = settings.backend_url


def get_worker_status(worker_name: str) -> dict:
    """Get current status of a worker including verification details, current shift, and any active alerts."""
    try:
        response = httpx.get(
            f"{BACKEND_URL}/api/workers/status",
            params={"worker_name": worker_name},
            timeout=5.0,
        )
        response.raise_for_status()
        return response.json()
    except Exception:
        return {
            "worker_name": worker_name,
            "worker_id": "W-101",
            "phone": "+34612345001",
            "team": "Equipo Construccion A",
            "site": "Obra Central Madrid",
            "current_status": "on_shift",
            "current_shift": {
                "id": "SH-001",
                "clock_in": "2026-03-03T07:02:14",
                "scheduled_end": "2026-03-03T15:00:00",
                "hours_elapsed": 4.5,
            },
            "verification": {
                "status": "verified",
                "method": "sim_verification",
                "last_verified": "2026-03-03T07:02:14",
                "sim_swap_check": "passed",
                "location_check": "passed",
                "device_status": "reachable",
            },
            "alerts": [],
            "stats_30d": {
                "shifts_completed": 22,
                "total_hours": 176.5,
                "on_time_rate": 0.95,
                "absence_count": 0,
                "bradford_score": 0,
            },
            "source": "mock",
        }


def get_team_overview(team_name: str) -> dict:
    """Get overview of a team including worker count, on-shift count, absence rate, and average verification score."""
    try:
        response = httpx.get(
            f"{BACKEND_URL}/api/teams/overview",
            params={"team_name": team_name},
            timeout=5.0,
        )
        response.raise_for_status()
        return response.json()
    except Exception:
        return {
            "team_name": team_name,
            "site": "Obra Central Madrid",
            "total_workers": 8,
            "on_shift": 6,
            "absent_today": 1,
            "day_off": 1,
            "workers": [
                {
                    "name": "Juan Garcia Lopez",
                    "status": "on_shift",
                    "verification": "sim_verified",
                    "clock_in": "07:02",
                },
                {
                    "name": "Maria Santos Ruiz",
                    "status": "on_shift",
                    "verification": "sim_verified",
                    "clock_in": "06:58",
                },
                {
                    "name": "Pedro Lopez Fernandez",
                    "status": "on_shift",
                    "verification": "sim_verified",
                    "clock_in": "07:15",
                    "late": True,
                },
                {
                    "name": "Ana Rodriguez Martinez",
                    "status": "on_shift",
                    "verification": "sim_verified",
                    "clock_in": "07:01",
                },
                {
                    "name": "Luis Martinez Gomez",
                    "status": "absent",
                    "absence_type": "sick_leave",
                    "justified": True,
                },
                {
                    "name": "Sofia Moreno Torres",
                    "status": "on_shift",
                    "verification": "sim_verified",
                    "clock_in": "07:00",
                },
                {
                    "name": "Roberto Sanchez Diaz",
                    "status": "on_shift",
                    "verification": "pending",
                    "clock_in": "07:20",
                    "late": True,
                },
                {
                    "name": "Fernando Navarro Gil",
                    "status": "day_off",
                    "verification": None,
                },
            ],
            "metrics": {
                "attendance_rate": 0.875,
                "on_time_rate": 0.83,
                "verification_rate": 0.86,
                "average_bradford_score": 12.3,
                "total_hours_today": 37.5,
            },
            "source": "mock",
        }


def get_unverified_workers() -> dict:
    """Get list of workers who haven't completed verification or have expired verification status."""
    try:
        response = httpx.get(
            f"{BACKEND_URL}/api/workers/unverified",
            timeout=5.0,
        )
        response.raise_for_status()
        return response.json()
    except Exception:
        return {
            "unverified_workers": [
                {
                    "worker_name": "Carlos Ruiz Hernandez",
                    "worker_id": "W-105",
                    "phone": "+34612345005",
                    "site": "Almacen Sur Valencia",
                    "reason": "verification_pending",
                    "clock_in": "2026-03-03T08:00:22",
                    "time_since_clock_in_minutes": 45,
                    "last_sim_check": None,
                },
                {
                    "worker_name": "Roberto Sanchez Diaz",
                    "worker_id": "W-108",
                    "phone": "+34612345008",
                    "site": "Obra Central Madrid",
                    "reason": "sim_check_failed",
                    "clock_in": "2026-03-03T07:20:00",
                    "time_since_clock_in_minutes": 85,
                    "last_sim_check": "2026-03-03T07:20:05",
                    "failure_reason": "SIM swap detectado en las ultimas 48 horas",
                },
                {
                    "worker_name": "Isabel Romero Perez",
                    "worker_id": "W-111",
                    "phone": "+34612345011",
                    "site": "Proyecto Norte Barcelona",
                    "reason": "location_mismatch",
                    "clock_in": "2026-03-03T07:05:00",
                    "time_since_clock_in_minutes": 100,
                    "last_sim_check": "2026-03-03T07:05:10",
                    "failure_reason": "Ubicacion del dispositivo fuera del radio del sitio de trabajo",
                },
            ],
            "total": 3,
            "critical": 2,
            "pending": 1,
            "source": "mock",
        }
