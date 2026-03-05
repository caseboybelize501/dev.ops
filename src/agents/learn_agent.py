import asyncio
import json
from src.bootstrap.system_profile import SystemProfile
from src.memory.incident_store import IncidentStore
from src.memory.solution_library import SolutionLibrary
from src.services.llama import call_llm

class LearnAgent:
    """
    Extracts patterns from incidents and stores solutions in the library.
    """

    @staticmethod
    async def extract_pattern_and_store(incident_data: dict):
        """
        Extract a reusable solution pattern from an incident.
        """
        print("Extracting pattern from incident...")

        # Get system profile
        profile = SystemProfile.read()

        # Generate prompt for LLM
        prompt = f"""
Extract a reusable solution pattern from this resolved incident.

Incident: {incident_data.get('description', 'Unknown')}
Root cause: {incident_data.get('root_cause', 'Unknown')}
Fix applied: {incident_data.get('fix_applied', 'Unknown')}
Test cycles to STABLE: {incident_data.get('cycles_to_stable', 0)}
Was a memory solution used? {incident_data.get('memory_used', 'NO')}
Effectiveness: {incident_data.get('effectiveness', 0.0)}

Extract a pattern the system can reuse.
Return JSON:
{{
  "pattern_name": "string",
  "failure_signature": "string (embeddable description)",
  "root_cause_class": "dependency|config|logic|resource|network|security",
  "solution_template": "string (generalizable, not just this instance)",
  "applicability_conditions": ["string"],
  "confidence": 0-1,
  "tags": ["string"]
}}
"""

        response = call_llm(prompt, temperature=0.4)
        print(f"Extracted pattern: {response}")

        try:
            pattern_data = json.loads(response)
            SolutionLibrary.store_pattern(pattern_data)
            print("Pattern stored in solution library.")
        except Exception as e:
            print(f"Error storing pattern: {e}")