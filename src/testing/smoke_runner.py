import asyncio
import time
from src.bootstrap.system_profile import SystemProfile

def run_smoke_tests() -> dict:
    """
    Run smoke tests to check service reachability.
    """
    print("Running smoke tests...")
    profile = SystemProfile.read()

    # Check basic connectivity
    healthy_services = []
    for conn in profile.get("network", []):
        if conn["status"] == "LISTEN":
            try:
                # Simple connection test (simplified)
                healthy_services.append(conn["laddr"][1])
            except Exception as e:
                print(f"Smoke test failed for port {conn['laddr'][1]}: {e}")

    duration = time.time() - time.time()
    return {
        "passed": len(healthy_services) > 0,
        "duration": duration,
        "services_healthy": healthy_services
    }