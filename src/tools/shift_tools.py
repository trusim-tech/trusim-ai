import httpx
from src.config import settings

BACKEND_URL = settings.backend_url


def get_current_shifts() -> dict:
    """Get all shifts currently in progress. Returns list of active shifts with worker names, sites, clock-in times, and status."""
    try:
        response = httpx.get(
            f"{BACKEND_URL}/api/shifts",
            params={"status": "in_progress"},
            timeout=5.0,
        )
        response.raise_for_status()
        return response.json()
    except Exception:
        return {
            "shifts": [
                {
                    "id": "SH-001",
                    "worker_name": "Juan Garcia Lopez",
                    "worker_id": "W-101",
                    "site": "Obra Central Madrid",
                    "clock_in": "2026-03-03T07:02:14",
                    "scheduled_start": "2026-03-03T07:00:00",
                    "status": "in_progress",
                    "verification": "sim_verified",
                    "phone": "+34612345001",
                },
                {
                    "id": "SH-002",
                    "worker_name": "Maria Santos Ruiz",
                    "worker_id": "W-102",
                    "site": "Obra Central Madrid",
                    "clock_in": "2026-03-03T06:58:30",
                    "scheduled_start": "2026-03-03T07:00:00",
                    "status": "in_progress",
                    "verification": "sim_verified",
                    "phone": "+34612345002",
                },
                {
                    "id": "SH-003",
                    "worker_name": "Pedro Lopez Fernandez",
                    "worker_id": "W-103",
                    "site": "Proyecto Norte Barcelona",
                    "clock_in": "2026-03-03T07:15:42",
                    "scheduled_start": "2026-03-03T07:00:00",
                    "status": "in_progress",
                    "verification": "sim_verified",
                    "late_minutes": 15,
                    "phone": "+34612345003",
                },
                {
                    "id": "SH-004",
                    "worker_name": "Ana Rodriguez Martinez",
                    "worker_id": "W-104",
                    "site": "Proyecto Norte Barcelona",
                    "clock_in": "2026-03-03T07:01:05",
                    "scheduled_start": "2026-03-03T07:00:00",
                    "status": "in_progress",
                    "verification": "sim_verified",
                    "phone": "+34612345004",
                },
                {
                    "id": "SH-005",
                    "worker_name": "Carlos Ruiz Hernandez",
                    "worker_id": "W-105",
                    "site": "Almacen Sur Valencia",
                    "clock_in": "2026-03-03T08:00:22",
                    "scheduled_start": "2026-03-03T08:00:00",
                    "status": "in_progress",
                    "verification": "pending",
                    "phone": "+34612345005",
                },
            ],
            "total": 5,
            "source": "mock",
        }


def get_shift_summary(start_date: str, end_date: str) -> dict:
    """Get aggregated shift statistics for a date range. Returns total hours, on-time rate, attendance summary."""
    try:
        response = httpx.get(
            f"{BACKEND_URL}/api/shifts/summary",
            params={"start_date": start_date, "end_date": end_date},
            timeout=5.0,
        )
        response.raise_for_status()
        return response.json()
    except Exception:
        return {
            "period": {"start": start_date, "end": end_date},
            "total_shifts": 187,
            "total_hours_worked": 1496.5,
            "average_hours_per_shift": 8.0,
            "on_time_rate": 0.89,
            "late_arrivals": 21,
            "early_departures": 8,
            "attendance_rate": 0.94,
            "verified_by_sim": 0.97,
            "sites": {
                "Obra Central Madrid": {"shifts": 78, "hours": 624.0},
                "Proyecto Norte Barcelona": {"shifts": 62, "hours": 496.0},
                "Almacen Sur Valencia": {"shifts": 47, "hours": 376.5},
            },
            "source": "mock",
        }


def get_worker_shifts(worker_name: str) -> dict:
    """Get all shifts for a specific worker by name. Returns their shift history with clock-in/out times and verification status."""
    try:
        response = httpx.get(
            f"{BACKEND_URL}/api/shifts",
            params={"worker_name": worker_name},
            timeout=5.0,
        )
        response.raise_for_status()
        return response.json()
    except Exception:
        return {
            "worker_name": worker_name,
            "shifts": [
                {
                    "id": "SH-201",
                    "date": "2026-03-03",
                    "site": "Obra Central Madrid",
                    "clock_in": "2026-03-03T07:02:14",
                    "clock_out": None,
                    "status": "in_progress",
                    "verification": "sim_verified",
                    "hours_worked": None,
                },
                {
                    "id": "SH-187",
                    "date": "2026-03-02",
                    "site": "Obra Central Madrid",
                    "clock_in": "2026-03-02T07:00:45",
                    "clock_out": "2026-03-02T15:05:12",
                    "status": "completed",
                    "verification": "sim_verified",
                    "hours_worked": 8.07,
                },
                {
                    "id": "SH-173",
                    "date": "2026-03-01",
                    "site": "Obra Central Madrid",
                    "clock_in": "2026-03-01T07:12:30",
                    "clock_out": "2026-03-01T15:00:00",
                    "status": "completed",
                    "verification": "sim_verified",
                    "hours_worked": 7.79,
                    "late_minutes": 12,
                },
                {
                    "id": "SH-158",
                    "date": "2026-02-28",
                    "site": "Obra Central Madrid",
                    "clock_in": "2026-02-28T06:58:00",
                    "clock_out": "2026-02-28T15:02:00",
                    "status": "completed",
                    "verification": "sim_verified",
                    "hours_worked": 8.07,
                },
                {
                    "id": "SH-142",
                    "date": "2026-02-27",
                    "site": "Obra Central Madrid",
                    "clock_in": "2026-02-27T07:01:00",
                    "clock_out": "2026-02-27T15:00:30",
                    "status": "completed",
                    "verification": "sim_verified",
                    "hours_worked": 7.99,
                },
            ],
            "total_shifts": 5,
            "total_hours": 31.92,
            "average_hours": 7.98,
            "on_time_rate": 0.80,
            "source": "mock",
        }
