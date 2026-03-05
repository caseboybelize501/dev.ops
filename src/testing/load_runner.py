import subprocess
import asyncio

def run_load_tests() -> dict:
    """
    Run load tests using Locust.
    """
    print("Running load tests...")
    try:
        result = subprocess.run(["locust", "--headless", "-t", "60s", "-r", "100"],
                                capture_output=True, text=True)
        if result.returncode == 0:
            return {
                "passed": True,
                "duration": 0,
                "output": result.stdout
            }
        else:
            return {
                "passed": False,
                "duration": 0,
                "error": result.stderr
            }
    except Exception as e:
        return {
            "passed": False,
            "duration": 0,
            "error": str(e)
        }