import hashlib
import os
from typing import Dict, List

class DedupRegistry:
    """
    Registry to track model files by hash and deduplicate across filesystem.
    """
    def __init__(self):
        self.registry = {}

    def add_model(self, path: str, size_gb: float, base_model: str, quantization: str, server: str):
        """
        Add a model to the registry with its hash.
        """
        try:
            with open(path, 'rb') as f:
                file_hash = hashlib.sha256(f.read()).hexdigest()

            self.registry[file_hash] = {
                "path": path,
                "size_gb": size_gb,
                "base_model": base_model,
                "quantization": quantization,
                "server": server
            }
        except Exception as e:
            print(f"Error adding model to registry: {e}")

    def find_duplicates(self, path: str) -> List[Dict]:
        """
        Find duplicates for a given file path.
        """
        try:
            with open(path, 'rb') as f:
                file_hash = hashlib.sha256(f.read()).hexdigest()

            duplicates = []
            for hash_key, info in self.registry.items():
                if hash_key == file_hash:
                    continue  # Skip the original file itself
                duplicates.append(info)
            return duplicates
        except Exception as e:
            print(f"Error finding duplicates: {e}")
            return []

    def get_model_info(self, path: str) -> Dict:
        """
        Get model info by path.
        """
        try:
            with open(path, 'rb') as f:
                file_hash = hashlib.sha256(f.read()).hexdigest()
            return self.registry.get(file_hash)
        except Exception as e:
            print(f"Error getting model info: {e}")
            return {}

    def is_model_loaded(self, path: str) -> bool:
        """
        Check if a model is already loaded in any inference server.
        """
        try:
            with open(path, 'rb') as f:
                file_hash = hashlib.sha256(f.read()).hexdigest()
            return file_hash in self.registry
        except Exception as e:
            print(f"Error checking if model is loaded: {e}")
            return False