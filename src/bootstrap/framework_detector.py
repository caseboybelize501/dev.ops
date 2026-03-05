import subprocess
import requests
import json
from typing import Dict, List

def detect_frameworks() -> Dict:
    """
    Detect available inference frameworks and their health status.
    """
    frameworks = {
        "ollama": False,
        "llama_cpp": False,
        "lmstudio": False,
        "vllm": False,
        "gpu_info": {},
        "recommended_path": None
    }

    # Check Ollama
    try:
        response = requests.get("http://localhost:11434/health", timeout=5)
        if response.status_code == 200:
            frameworks["ollama"] = True
    except Exception as e:
        pass

    # Check llama.cpp
    try:
        response = requests.get("http://localhost:8000/health", timeout=5)
        if response.status_code == 200:
            frameworks["llama_cpp"] = True
    except Exception as e:
        pass

    # Check LM Studio
    try:
        response = requests.get("http://localhost:1234/v1/models", timeout=5)
        if response.status_code == 200:
            frameworks["lmstudio"] = True
    except Exception as e:
        pass

    # Check vLLM
    try:
        response = requests.get("http://localhost:8080/v1/models", timeout=5)
        if response.status_code == 200:
            frameworks["vllm"] = True
    except Exception as e:
        pass

    # Get GPU info
    try:
        result = subprocess.run(["nvidia-smi", "--query-gpu=name,memory.total,memory.free,memory.used", "--format=csv"],
                                capture_output=True, text=True)
        if result.returncode == 0:
            lines = result.stdout.strip().split('\n')[1:]  # Skip header
            frameworks["gpu_info"] = [line.split(',') for line in lines]
    except Exception as e:
        pass

    # Recommend path based on availability and GPU
    if frameworks["vllm"]:
        frameworks["recommended_path"] = "vllm"
    elif frameworks["ollama"]:
        frameworks["recommended_path"] = "ollama"
    elif frameworks["llama_cpp"]:
        frameworks["recommended_path"] = "llama_cpp"
    elif frameworks["lmstudio"]:
        frameworks["recommended_path"] = "lmstudio"

    return frameworks