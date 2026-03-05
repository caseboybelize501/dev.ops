import os
import re
from pathlib import Path


def scan_gguf_models():
    """
    Scan for GGUF model files in standard cache locations.
    """
    model_paths = [
        os.environ.get("HF_HOME", "/home/user/.cache/huggingface"),
        os.path.expanduser("~/.ollama/models"),
        os.path.expanduser("~/.lmstudio/models"),
        "/opt/models",
        os.path.expanduser("~/models"),
        "/models"
    ]

    models = []
    for path in model_paths:
        if not os.path.exists(path):
            continue
        for root, dirs, files in os.walk(path):
            for file in files:
                if file.endswith(('.gguf', '.ggml', '.bin', '.safetensors', '.pt')):
                    full_path = os.path.join(root, file)
                    try:
                        # Parse filename to extract base model and quantization
                        parsed = parse_filename(file)
                        models.append({
                            "path": full_path,
                            "filename": file,
                            "base_model": parsed["base_model"],
                            "quantization": parsed["quantization"],
                            "size": os.path.getsize(full_path)
                        })
                    except Exception as e:
                        print(f"Error parsing model {file}: {e}")
    return models


def parse_filename(filename: str) -> dict:
    """
    Parse GGUF filename to extract base model and quantization.
    """
    # Example patterns:
    # llama3-8b-Q4_K_M.gguf
    # mistral-7b-v0.1-GGUF-Q4_K_M
    # phi-2.Q4_0.bin

    pattern = r"([a-zA-Z0-9\-_]+)(?:[-_](?:v\d+))?(?:[-_](?:Q[0-9_]+|q[0-9_]+))?\.gguf|\.bin|\.pt|\.safetensors"
    match = re.search(pattern, filename)

    if not match:
        return {"base_model": "unknown", "quantization": "unknown"}

    base_model = match.group(1)
    quantization = "unknown"

    # Extract quantization from filename
    quant_pattern = r"Q[0-9_]+|q[0-9_]+"
    quant_match = re.search(quant_pattern, filename)
    if quant_match:
        quantization = quant_match.group()

    return {"base_model": base_model, "quantization": quantization}