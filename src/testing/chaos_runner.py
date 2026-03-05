import subprocess
import asyncio

def run_chaos_tests() -> dict:
    """
    Run chaos injection tests.
    """
    print("Running chaos tests...")
    try:
        result = subprocess.run(["chaos", "run", "chaos_experiment.yaml"],
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