import subprocess
import asyncio
from src.bootstrap.system_profile import SystemProfile

class SecurityAgent:
    """
    Performs CVE scanning, secret detection, and network exposure audit.
    """

    @staticmethod
    async def scan_cves():
        """
        Scan for CVEs in Docker images.
        """
        print("Scanning for CVEs...")
        try:
            # Run trivy on all Docker images
            images = SystemProfile.read().get("docker_images", [])
            findings = []
            for image in images:
                image_name = image.get("Repository", "") + ":" + image.get("Tag", "latest")
                result = subprocess.run(["trivy", "image", image_name], capture_output=True, text=True)
                if result.returncode == 0:
                    findings.append({
                        "image": image_name,
                        "cve_results": result.stdout
                    })
            return findings
        except Exception as e:
            print(f"Error scanning CVEs: {e}")
            return []

    @staticmethod
    async def scan_secrets():
        """
        Scan for secrets in code and configuration.
        """
        print("Scanning for secrets...")
        try:
            # Run truffleHog on repository
            result = subprocess.run(["trufflehog", "filesystem", "."], capture_output=True, text=True)
            if result.returncode == 0:
                return result.stdout
            return "No secrets found"
        except Exception as e:
            print(f"Error scanning secrets: {e}")
            return "Error scanning secrets"

    @staticmethod
    async def audit_exposure():
        """
        Audit network exposure.
        """
        print("Auditing network exposure...")
        try:
            # Check open ports and services
            profile = SystemProfile.read()
            exposed_ports = []
            for conn in profile.get("network", []):
                if conn["status"] == "LISTEN":
                    exposed_ports.append(conn)
            return exposed_ports
        except Exception as e:
            print(f"Error auditing exposure: {e}")
            return []