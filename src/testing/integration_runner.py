import subprocess
import asyncio

def run_integration_tests() -> dict:
    """
    Run integration tests between services.
    """
    print("Running integration tests...")
    try:
        result = subprocess.run(["pytest", "tests/integration/"], capture_output=True, text=True)
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