import httpx
from src.config import settings

NOKIA_API_BASE = "https://network-as-code.p-eu.rapidapi.com"
NOKIA_API_HOST = "network-as-code.nokia.rapidapi.com"


def _nokia_headers() -> dict:
    """Build headers for Nokia Network as Code API requests."""
    return {
        "x-rapidapi-key": settings.nokia_api_key,
        "x-rapidapi-host": NOKIA_API_HOST,
        "Content-Type": "application/json",
    }


def check_sim_swap(phone_number: str) -> dict:
    """Check if a SIM swap has occurred recently for a phone number using Nokia Network as Code API. This helps detect identity fraud."""
    if settings.nokia_api_key:
        try:
            response = httpx.post(
                f"{NOKIA_API_BASE}/passthrough/camara/v1/sim-swap/sim-swap/v0/check",
                headers=_nokia_headers(),
                json={"phoneNumber": phone_number, "maxAge": 240},
                timeout=10.0,
            )
            response.raise_for_status()
            data = response.json()
            return {
                "phone_number": phone_number,
                "swapped": data.get("swapped", False),
                "check_timestamp": "2026-03-03T12:00:00Z",
                "api_source": "nokia_network_as_code",
                "raw_response": data,
            }
        except Exception as e:
            pass  # Fall through to mock data

    # Mock data for demo
    mock_results = {
        "+34612345008": {
            "phone_number": phone_number,
            "swapped": True,
            "swap_date": "2026-03-02T22:15:00Z",
            "check_timestamp": "2026-03-03T07:20:05Z",
            "alert": "SIM swap detectado en las ultimas 48 horas",
            "risk_level": "high",
            "recommended_action": "Verificar identidad del trabajador presencialmente",
            "api_source": "mock",
        },
        "+34612345011": {
            "phone_number": phone_number,
            "swapped": False,
            "swap_date": None,
            "check_timestamp": "2026-03-03T07:05:10Z",
            "alert": None,
            "risk_level": "none",
            "recommended_action": None,
            "api_source": "mock",
        },
    }

    if phone_number in mock_results:
        return mock_results[phone_number]

    return {
        "phone_number": phone_number,
        "swapped": False,
        "swap_date": None,
        "check_timestamp": "2026-03-03T12:00:00Z",
        "alert": None,
        "risk_level": "none",
        "recommended_action": None,
        "api_source": "mock",
    }


def check_device_status(phone_number: str) -> dict:
    """Check device reachability and connectivity status using Nokia Network as Code API. Verifies the worker's device is online and active."""
    if settings.nokia_api_key:
        try:
            response = httpx.post(
                f"{NOKIA_API_BASE}/device-status/device-reachability-status/v1/retrieve",
                headers={
                    **_nokia_headers(),
                    "x-correlator": "trusim-check-001",
                },
                json={"device": {"phoneNumber": phone_number}},
                timeout=10.0,
            )
            response.raise_for_status()
            data = response.json()
            return {
                "phone_number": phone_number,
                "reachability_status": data.get("reachabilityStatus", "UNKNOWN"),
                "check_timestamp": "2026-03-03T12:00:00Z",
                "api_source": "nokia_network_as_code",
                "raw_response": data,
            }
        except Exception:
            pass  # Fall through to mock data

    # Mock data for demo
    mock_results = {
        "+34612345001": {
            "phone_number": phone_number,
            "reachability_status": "CONNECTED_DATA",
            "connectivity_status": "CONNECTED_DATA",
            "roaming": False,
            "country_name": "Spain",
            "check_timestamp": "2026-03-03T07:02:14Z",
            "api_source": "mock",
        },
        "+34612345005": {
            "phone_number": phone_number,
            "reachability_status": "CONNECTED_SMS",
            "connectivity_status": "CONNECTED_SMS",
            "roaming": False,
            "country_name": "Spain",
            "check_timestamp": "2026-03-03T08:00:22Z",
            "api_source": "mock",
        },
        "+34612345008": {
            "phone_number": phone_number,
            "reachability_status": "CONNECTED_DATA",
            "connectivity_status": "CONNECTED_DATA",
            "roaming": False,
            "country_name": "Spain",
            "check_timestamp": "2026-03-03T07:20:05Z",
            "alert": "Dispositivo activo pero SIM swap reciente detectado",
            "api_source": "mock",
        },
    }

    if phone_number in mock_results:
        return mock_results[phone_number]

    return {
        "phone_number": phone_number,
        "reachability_status": "CONNECTED_DATA",
        "connectivity_status": "CONNECTED_DATA",
        "roaming": False,
        "country_name": "Spain",
        "check_timestamp": "2026-03-03T12:00:00Z",
        "api_source": "mock",
    }


def verify_location(
    phone_number: str, latitude: float, longitude: float, radius: int
) -> dict:
    """Verify if a device is within a specified location radius using Nokia Network as Code API. Used to confirm worker is at the job site."""
    if settings.nokia_api_key:
        try:
            response = httpx.post(
                f"{NOKIA_API_BASE}/location-verification/v1/verify",
                headers=_nokia_headers(),
                json={
                    "device": {"phoneNumber": phone_number},
                    "area": {
                        "areaType": "CIRCLE",
                        "center": {
                            "latitude": latitude,
                            "longitude": longitude,
                        },
                        "radius": radius,
                    },
                },
                timeout=10.0,
            )
            response.raise_for_status()
            data = response.json()
            return {
                "phone_number": phone_number,
                "verification_result": data.get("verificationResult", "UNKNOWN"),
                "expected_location": {
                    "latitude": latitude,
                    "longitude": longitude,
                    "radius_meters": radius,
                },
                "check_timestamp": "2026-03-03T12:00:00Z",
                "api_source": "nokia_network_as_code",
                "raw_response": data,
            }
        except Exception:
            pass  # Fall through to mock data

    # Mock data for demo
    mock_results = {
        "+34612345001": {
            "phone_number": phone_number,
            "verification_result": "TRUE",
            "match_rate": 98,
            "expected_location": {
                "latitude": latitude,
                "longitude": longitude,
                "radius_meters": radius,
            },
            "device_location": {
                "latitude": 40.4168,
                "longitude": -3.7038,
            },
            "distance_from_center_meters": 45,
            "within_radius": True,
            "check_timestamp": "2026-03-03T07:02:14Z",
            "api_source": "mock",
        },
        "+34612345011": {
            "phone_number": phone_number,
            "verification_result": "FALSE",
            "match_rate": 0,
            "expected_location": {
                "latitude": latitude,
                "longitude": longitude,
                "radius_meters": radius,
            },
            "device_location": {
                "latitude": 41.4036,
                "longitude": 2.1744,
            },
            "distance_from_center_meters": 15200,
            "within_radius": False,
            "alert": "Dispositivo fuera del radio esperado. Distancia: 15.2 km",
            "check_timestamp": "2026-03-03T07:05:10Z",
            "api_source": "mock",
        },
    }

    if phone_number in mock_results:
        return mock_results[phone_number]

    return {
        "phone_number": phone_number,
        "verification_result": "TRUE",
        "match_rate": 95,
        "expected_location": {
            "latitude": latitude,
            "longitude": longitude,
            "radius_meters": radius,
        },
        "device_location": {
            "latitude": latitude + 0.0001,
            "longitude": longitude + 0.0001,
        },
        "distance_from_center_meters": 15,
        "within_radius": True,
        "check_timestamp": "2026-03-03T12:00:00Z",
        "api_source": "mock",
    }
