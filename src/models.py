from pydantic import BaseModel
from typing import List, Dict, Optional
import time

class SystemProfile(BaseModel):
    os: str
    platform: str
    cpu_count: int
    memory: Dict[str, int]
    disk: List[Dict]
    network: List[Dict]
    processes: List[Dict]
    packages: List[Dict]
    docker_images: List[Dict]
    docker_containers: List[Dict]
    kubernetes_pods: List[Dict]
    gguf_models: List[Dict]
    frameworks: Dict[str, bool]


class TestCycle(BaseModel):
    id: str
    start_time: float
    end_time: Optional[float] = None
    results: List[Dict]
    passed: bool


class Incident(BaseModel):
    id: str
    description: str
    root_cause: str
    fix_applied: str
    timestamp: float
    cycles_to_stable: int
    memory_used: bool
    effectiveness: float


class Solution(BaseModel):
    pattern_name: str
    failure_signature: str
    root_cause_class: str
    solution_template: str
    applicability_conditions: List[str]
    confidence: float
    tags: List[str]
    created_at: float


class Deployment(BaseModel):
    id: str
    cycle_id: str
    timestamp: float
    status: str
    artifacts_deployed: List[str]


class SecurityFinding(BaseModel):
    id: str
    type: str  # cve, secret, exposure
    severity: str
    description: str
    affected_component: str
    timestamp: float