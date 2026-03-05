import requests
import json
from src.bootstrap.system_profile import SystemProfile
from typing import Dict, List

def route_task(task_type: str, context: dict = None) -> str:
    """
    Route tasks to appropriate agents based on system profile and task type.
    """
    profile = SystemProfile.read()

    # Determine which agent should handle the task
    if task_type == "monitor":
        return "MonitorAgent"
    elif task_type == "test":
        return "TestAgent"
    elif task_type == "patch":
        return "PatchAgent"
    elif task_type == "deploy":
        return "DeployAgent"
    elif task_type == "security":
        return "SecurityAgent"
    elif task_type == "learn":
        return "LearnAgent"

    # Default fallback to TestAgent for unknown tasks
    return "TestAgent"


def generate_llm_prompt(task: str, context: dict) -> str:
    """
    Generate prompt for LLM planner.
    """
    system_profile = SystemProfile.read()

    prompt = f"""
You are a DevOps intelligence agent. You have access to the following system information:

System Profile:
- OS: {system_profile.get('os', 'unknown')}
- CPU Count: {system_profile.get('cpu_count', 0)}
- Memory: {system_profile.get('memory', {}).get('total', 0)} bytes total
- Frameworks Available: {list(system_profile.get('frameworks', {}).keys())}
- GGUF Models Detected: {len(system_profile.get('gguf_models', []))}

Task: {task}
Context: {context}

Based on this information, determine the best course of action.
Return a JSON object with:
1. agent_name (string): The name of the agent to route to
2. reasoning (string): Brief explanation of why this agent is chosen
3. parameters (dict): Any parameters needed by the agent
"""

    return prompt