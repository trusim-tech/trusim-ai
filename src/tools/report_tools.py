import httpx
from src.config import settings

BACKEND_URL = settings.backend_url


def generate_daily_report(date: str) -> dict:
    """Generate a daily workforce report including attendance rate, hours worked, anomalies detected, and absences."""
    try:
        response = httpx.get(
            f"{BACKEND_URL}/api/reports/daily",
            params={"date": date},
            timeout=5.0,
        )
        response.raise_for_status()
        return response.json()
    except Exception:
        return {
            "report_date": date,
            "generated_at": "2026-03-03T15:30:00",
            "summary": {
                "total_workers_scheduled": 25,
                "workers_present": 22,
                "workers_absent": 3,
                "attendance_rate": 0.88,
                "total_hours_worked": 172.5,
                "average_hours_per_worker": 7.84,
                "on_time_arrivals": 18,
                "late_arrivals": 4,
                "on_time_rate": 0.82,
            },
            "verification": {
                "sim_verified": 20,
                "verification_pending": 1,
                "verification_failed": 1,
                "verification_rate": 0.91,
            },
            "absences": [
                {
                    "worker_name": "Luis Martinez Gomez",
                    "type": "sick_leave",
                    "justified": True,
                },
                {
                    "worker_name": "Elena Fernandez Castro",
                    "type": "personal",
                    "justified": True,
                },
                {
                    "worker_name": "Roberto Sanchez Diaz",
                    "type": "no_show",
                    "justified": False,
                },
            ],
            "anomalies_detected": 4,
            "anomalies_summary": {
                "sim_swap": 1,
                "location_spoofing": 1,
                "buddy_punching": 1,
                "unusual_pattern": 1,
            },
            "sites": [
                {
                    "name": "Obra Central Madrid",
                    "workers": 10,
                    "present": 9,
                    "hours": 70.5,
                    "anomalies": 1,
                },
                {
                    "name": "Proyecto Norte Barcelona",
                    "workers": 9,
                    "present": 8,
                    "hours": 62.0,
                    "anomalies": 2,
                },
                {
                    "name": "Almacen Sur Valencia",
                    "workers": 6,
                    "present": 5,
                    "hours": 40.0,
                    "anomalies": 1,
                },
            ],
            "source": "mock",
        }


def generate_payroll_report(start_date: str, end_date: str) -> dict:
    """Generate payroll data for a date range including per-worker hours, overtime, and verified percentage."""
    try:
        response = httpx.get(
            f"{BACKEND_URL}/api/reports/payroll",
            params={"start_date": start_date, "end_date": end_date},
            timeout=5.0,
        )
        response.raise_for_status()
        return response.json()
    except Exception:
        return {
            "period": {"start": start_date, "end": end_date},
            "generated_at": "2026-03-03T15:30:00",
            "workers": [
                {
                    "worker_name": "Juan Garcia Lopez",
                    "worker_id": "W-101",
                    "regular_hours": 160.0,
                    "overtime_hours": 8.5,
                    "total_hours": 168.5,
                    "days_worked": 20,
                    "absences": 0,
                    "verified_percentage": 100.0,
                    "on_time_rate": 0.95,
                },
                {
                    "worker_name": "Maria Santos Ruiz",
                    "worker_id": "W-102",
                    "regular_hours": 160.0,
                    "overtime_hours": 4.0,
                    "total_hours": 164.0,
                    "days_worked": 20,
                    "absences": 0,
                    "verified_percentage": 100.0,
                    "on_time_rate": 1.0,
                },
                {
                    "worker_name": "Pedro Lopez Fernandez",
                    "worker_id": "W-103",
                    "regular_hours": 152.0,
                    "overtime_hours": 0.0,
                    "total_hours": 152.0,
                    "days_worked": 19,
                    "absences": 1,
                    "verified_percentage": 100.0,
                    "on_time_rate": 0.74,
                },
                {
                    "worker_name": "Ana Rodriguez Martinez",
                    "worker_id": "W-104",
                    "regular_hours": 160.0,
                    "overtime_hours": 12.0,
                    "total_hours": 172.0,
                    "days_worked": 20,
                    "absences": 0,
                    "verified_percentage": 100.0,
                    "on_time_rate": 0.95,
                },
                {
                    "worker_name": "Carlos Ruiz Hernandez",
                    "worker_id": "W-105",
                    "regular_hours": 152.0,
                    "overtime_hours": 2.0,
                    "total_hours": 154.0,
                    "days_worked": 19,
                    "absences": 1,
                    "verified_percentage": 95.0,
                    "on_time_rate": 0.89,
                },
                {
                    "worker_name": "Luis Martinez Gomez",
                    "worker_id": "W-106",
                    "regular_hours": 144.0,
                    "overtime_hours": 0.0,
                    "total_hours": 144.0,
                    "days_worked": 18,
                    "absences": 2,
                    "verified_percentage": 100.0,
                    "on_time_rate": 0.89,
                },
                {
                    "worker_name": "Elena Fernandez Castro",
                    "worker_id": "W-107",
                    "regular_hours": 152.0,
                    "overtime_hours": 0.0,
                    "total_hours": 152.0,
                    "days_worked": 19,
                    "absences": 1,
                    "verified_percentage": 100.0,
                    "on_time_rate": 0.95,
                },
                {
                    "worker_name": "Roberto Sanchez Diaz",
                    "worker_id": "W-108",
                    "regular_hours": 120.0,
                    "overtime_hours": 0.0,
                    "total_hours": 120.0,
                    "days_worked": 15,
                    "absences": 5,
                    "verified_percentage": 80.0,
                    "on_time_rate": 0.67,
                },
                {
                    "worker_name": "Sofia Moreno Torres",
                    "worker_id": "W-109",
                    "regular_hours": 128.0,
                    "overtime_hours": 0.0,
                    "total_hours": 128.0,
                    "days_worked": 16,
                    "absences": 4,
                    "verified_percentage": 100.0,
                    "on_time_rate": 0.88,
                },
                {
                    "worker_name": "Fernando Navarro Gil",
                    "worker_id": "W-110",
                    "regular_hours": 144.0,
                    "overtime_hours": 6.0,
                    "total_hours": 150.0,
                    "days_worked": 18,
                    "absences": 2,
                    "verified_percentage": 100.0,
                    "on_time_rate": 0.94,
                },
            ],
            "totals": {
                "total_regular_hours": 1472.0,
                "total_overtime_hours": 32.5,
                "total_hours": 1504.5,
                "total_absences": 16,
                "average_verified_percentage": 97.5,
                "average_on_time_rate": 0.89,
            },
            "source": "mock",
        }
