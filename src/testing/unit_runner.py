import subprocess
import asyncio

def run_unit_tests() -> dict:
    """
    Run unit tests using pytest.
    """
    print("Running unit tests...")
    try:
        result = subprocess.run(["pytest", "--cov=src", "--cov-report=xml", "tests/unit/"],
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