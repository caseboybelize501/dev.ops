import time
from typing import Dict, List

class TestCycleManager:
    """
    Manages test cycles and tracks STABLE status.
    """

    def __init__(self):
        self.cycles = {}
        self.stable_count = 0
        self.last_cycle_id = None

    def start_new_cycle(self) -> str:
        """
        Start a new test cycle.
        """
        cycle_id = f"cycle_{int(time.time())}"
        self.cycles[cycle_id] = {
            "id": cycle_id,
            "start_time": time.time(),
            "results": [],
            "passed": False
        }
        self.last_cycle_id = cycle_id
        return cycle_id

    def store_results(self, cycle_id: str, results: list):
        """
        Store test results for a cycle.
        """
        if cycle_id in self.cycles:
            self.cycles[cycle_id]["results"] = results
            self.cycles[cycle_id]["passed"] = all(r["passed"] for r in results)
            self.cycles[cycle_id]["end_time"] = time.time()

    def get_cycle_results(self, cycle_id: str) -> dict:
        """
        Get results for a specific cycle.
        """
        return self.cycles.get(cycle_id, {})

    def is_cycle_stable(self, cycle_id: str) -> bool:
        """
        Check if the cycle is stable (5 consecutive passes).
        """
        # Simplified logic for demo purposes
        if not self.cycles[cycle_id]["passed"]:
            self.stable_count = 0
            return False

        self.stable_count += 1
        return self.stable_count >= 5

    def get_stable_status(self) -> dict:
        """
        Get current stable status.
        """
        return {
            "passes": self.stable_count,
            "last_cycle": self.last_cycle_id
        }

    def get_latest_cycle(self):
        """
        Get the latest cycle data.
        """
        if not self.last_cycle_id:
            return None
        return self.cycles[self.last_cycle_id]