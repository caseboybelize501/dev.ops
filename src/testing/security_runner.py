import subprocess
import asyncio

def run_security_tests() -> dict:
    """
    Run security scans (CVE, SAST, secrets).
    """
    print("Running security tests...")
    try:
        # Run trivy on all images
        result_trivy = subprocess.run(["trivy", "image", "--severity", "CRITICAL,HIGH", "--format", "json"],
                                      capture_output=True, text=True)
        
        # Run semgrep for SAST
        result_semgrep = subprocess.run(["semgrep", "--config=auto", "--format=json"],
                                        capture_output=True, text=True)
        
        # Run truffleHog for secrets
        result_trufflehog = subprocess.run(["trufflehog", "filesystem", "."],
                                           capture_output=True, text=True)

        if result_trivy.returncode == 0 and result_semgrep.returncode == 0:
            return {
                "passed": True,
                "duration": 0,
                "output": f"Trivy: {result_trivy.stdout} Semgrep: {result_semgrep.stdout} TruffleHog: {result_trufflehog.stdout}"
            }
        else:
            return {
                "passed": False,
                "duration": 0,
                "error": f"Trivy error: {result_trivy.stderr}, Semgrep error: {result_semgrep.stderr}"
            }
    except Exception as e:
        return {
            "passed": False,
            "duration": 0,
            "error": str(e)
        }