import requests
import json
from typing import Dict, List

def call_llm(prompt: str, temperature: float = 0.3, max_tokens: int = 512) -> str:
    """
    Call the LLaMA service for task routing and fix generation.
    """
    try:
        url = "http://llama:8000/generate"
        payload = {
            "prompt": prompt,
            "temperature": temperature,
            "max_tokens": max_tokens
        }
        response = requests.post(url, json=payload, timeout=30)
        if response.status_code == 200:
            result = response.json()
            return result.get("response", "")
        else:
            print(f"LLaMA API error: {response.status_code} - {response.text}")
            return "Error calling LLaMA service"
    except Exception as e:
        print(f"Error calling LLaMA service: {e}")
        return "Error calling LLaMA service"