import asyncio
import json
from src.bootstrap.system_profile import SystemProfile
from src.services.llama import call_llm
from src.memory.incident_store import IncidentStore
from src.memory.solution_library import SolutionLibrary

class PatchAgent:
    """
    Generates fixes for test failures and applies them.
    """

    @staticmethod
    async def generate_fix_and_patch(cycle_id: str, results: list):
        """
        Generate a fix based on failure details and apply it.
        """
        print("Generating fix for failed test cycle...")

        # Extract failure details
        failed_stages = [r for r in results if not r["passed"]]
        if not failed_stages:
            return

        last_failed_stage = failed_stages[-1]
        error_details = last_failed_stage.get("error", "Unknown error")
        stage_name = last_failed_stage["name"]

        # Get system profile
        profile = SystemProfile.read()

        # Query memory for similar past failures
        memory_results = IncidentStore.search_similar_incidents(error_details)

        # Generate fix using LLM
        prompt = f"""
A test cycle has failed.

Current failure: stage={stage_name}, error={error_details}.
System context (from SystemProfile): {profile}

If a memory solution exists with confidence > 0.80: adapt it.
If not: generate new fix.

Return JSON:
{{
  "fix_description": "string",
  "fix_type": "code|config|dependency|infra",
  "files_to_change": [
    {{
      "path": "string",
      "change_description": "string",
      "new_content": "string"
    }}
  ],
  "memory_solution_used": "string|null",
  "confidence": 0-1,
  "test_to_validate": "string",
  "potential_side_effects": ["string"]
}}
"""

        response = call_llm(prompt, temperature=0.2)
        print(f"Generated fix: {response}")

        # Parse and apply fix
        try:
            fix_data = json.loads(response)
            await PatchAgent.apply_fix(fix_data)
        except Exception as e:
            print(f"Error applying fix: {e}")

    @staticmethod
    async def apply_fix(fix_data: dict):
        """
        Apply the generated fix to files.
        """
        for file_change in fix_data.get("files_to_change", []):
            try:
                with open(file_change["path"], "w") as f:
                    f.write(file_change["new_content"])
                print(f"Applied fix to {file_change['path']}")
            except Exception as e:
                print(f"Error applying fix to {file_change['path']}: {e}")