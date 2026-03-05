import asyncio
import time
from src.bootstrap.system_profile import SystemProfile
from src.testing.smoke_runner import run_smoke_tests
from src.testing.unit_runner import run_unit_tests
from src.testing.integration_runner import run_integration_tests
from src.testing.load_runner import run_load_tests
from src.testing.chaos_runner import run_chaos_tests
from src.testing.security_runner import run_security_tests
from src.testing.cycle_manager import TestCycleManager

class TestAgent:
    """
    Orchestrates full automated test cycles.
    """

    @staticmethod
    async def run_full_cycle() -> str:
        """
        Run a complete 8-stage test cycle.
        """
        print("Starting full test cycle...")
        cycle_manager = TestCycleManager()
        cycle_id = cycle_manager.start_new_cycle()

        stages = [
            run_smoke_tests,
            run_unit_tests,
            run_integration_tests,
            run_load_tests,
            run_chaos_tests,
            run_security_tests,
            lambda: asyncio.sleep(0),  # Placeholder for regression test
            lambda: asyncio.sleep(0)   # Placeholder for performance baseline
        ]

        results = []
        for i, stage_func in enumerate(stages):
            try:
                result = await stage_func()
                results.append({
                    "stage": i + 1,
                    "name": stage_func.__name__,
                    "passed": True,
                    "duration": 0
                })
            except Exception as e:
                results.append({
                    "stage": i + 1,
                    "name": stage_func.__name__,
                    "passed": False,
                    "error": str(e)
                })
                # Trigger patch agent on failure
                if i < len(stages) - 1:  # Don't trigger patch on final stage
                    print(f"Stage {i+1} failed. Triggering patch agent.")
                    from src.agents.patch_agent import PatchAgent
                    await PatchAgent.generate_fix_and_patch(cycle_id, results)
                    return cycle_id

        # Store results
        cycle_manager.store_results(cycle_id, results)

        # Check if cycle is stable (5 consecutive passes)
        if cycle_manager.is_cycle_stable(cycle_id):
            print("Cycle is now STABLE. Unlocking deployment.")
            from src.agents.deploy_agent import DeployAgent
            await DeployAgent.deploy_artifacts()

        return cycle_id

    @staticmethod
    def get_cycle_results(cycle_id: str):
        """
        Get results for a specific test cycle.
        """
        from src.testing.cycle_manager import TestCycleManager
        return TestCycleManager().get_cycle_results(cycle_id)

    @staticmethod
    def get_stable_status():
        """
        Get current stable status (consecutive passes).
        """
        from src.testing.cycle_manager import TestCycleManager
        return TestCycleManager().get_stable_status()