import json
import os
from pathlib import Path

class SystemProfile:
    """
    Manages the system profile that is written once at startup.
    All agents read this before acting.
    """
    PROFILE_PATH = os.path.expanduser("~/.jarvis/system_profile.json")

    @staticmethod
    def write(profile: dict):
        """
        Write system profile to disk.
        """
        os.makedirs(os.path.dirname(SystemProfile.PROFILE_PATH), exist_ok=True)
        with open(SystemProfile.PROFILE_PATH, 'w') as f:
            json.dump(profile, f, indent=2)

    @staticmethod
    def read() -> dict:
        """
        Read system profile from disk.
        """
        try:
            with open(SystemProfile.PROFILE_PATH, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {}

    @staticmethod
    def get(key: str, default=None):
        """
        Get a specific key from the system profile.
        """
        profile = SystemProfile.read()
        return profile.get(key, default)