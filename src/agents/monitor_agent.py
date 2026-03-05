import asyncio
import time
from src.bootstrap.system_profile import SystemProfile
from src.services.llama import call_llm

class MonitorAgent:
    """
    Continuous monitoring agent for service health, log anomalies, and metric thresholds.
    """

    @staticmethod
    async def monitor_services():
        """
        Run continuous monitoring of services.
        """
        print("Starting continuous monitoring...")
        while True:
            try:
                # Get system profile
                profile = SystemProfile.read()

                # Check service health
                health_checks = []
                for conn in profile.get("network", []):
                    if conn["status"] == "LISTEN":
                        health_checks.append({
                            "port": conn["laddr"][1],
                            "status": "healthy"
                        })

                # Log anomaly detection (simplified)
                anomalies = []
                for proc in profile.get("processes", []):
                    if proc["memory_info"] and proc["memory_info"][0] > 1e9:  # 1GB threshold
                        anomalies.append({
                            "process": proc["name"],
                            "memory_usage": proc["memory_info"][0]
                        })

                # Send to LLM for analysis
                prompt = f"Analyze these service health checks and anomalies: {health_checks} {anomalies}"
                response = call_llm(prompt, temperature=0.3)
                print(f"Monitor Agent Analysis: {response}")

                await asyncio.sleep(60)  # Check every minute
            except Exception as e:
                print(f"Error in monitor agent: {e}")
                await asyncio.sleep(10)