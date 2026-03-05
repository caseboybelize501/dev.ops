import platform
import psutil
import subprocess
import os
import json
from src.bootstrap.gguf_detector import scan_gguf_models
from src.bootstrap.framework_detector import detect_frameworks
from src.bootstrap.dedup_registry import DedupRegistry


def scan_system():
    """
    Scans the entire system for:
    - OS info
    - Hardware specs
    - Disk usage
    - Network connections
    - Running processes
    - Installed packages
    - Docker images and containers
    - Kubernetes pods (if available)
    - GGUF models
    """
    profile = {
        "os": platform.system(),
        "platform": platform.platform(),
        "cpu_count": psutil.cpu_count(logical=True),
        "memory": {
            "total": psutil.virtual_memory().total,
            "available": psutil.virtual_memory().available,
            "percent": psutil.virtual_memory().percent
        },
        "disk": [],
        "network": [],
        "processes": [],
        "packages": [],
        "docker_images": [],
        "docker_containers": [],
        "kubernetes_pods": [],
        "gguf_models": [],
        "frameworks": {}
    }

    # Scan disk partitions
    for partition in psutil.disk_partitions(all=True):
        try:
            usage = psutil.disk_usage(partition.mountpoint)
            profile["disk"].append({
                "device": partition.device,
                "mountpoint": partition.mountpoint,
                "fstype": partition.fstype,
                "total": usage.total,
                "used": usage.used,
                "free": usage.free,
                "percent": usage.percent
            })
        except Exception as e:
            print(f"Error scanning disk {partition.mountpoint}: {e}")

    # Scan network connections
    for conn in psutil.net_connections(kind='inet'):
        try:
            profile["network"].append({
                "fd": conn.fd,
                "family": str(conn.family),
                "type": str(conn.type),
                "laddr": str(conn.laddr),
                "raddr": str(conn.raddr),
                "status": conn.status
            })
        except Exception as e:
            print(f"Error scanning network connection: {e}")

    # Scan running processes
    for proc in psutil.process_iter(['pid', 'name', 'username', 'memory_info', 'cpu_percent']):
        try:
            profile["processes"].append(proc.info)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass

    # Scan installed packages
    try:
        result = subprocess.run(["pip", "list", "--format=json"], capture_output=True, text=True)
        if result.returncode == 0:
            profile["packages"] = json.loads(result.stdout)
    except Exception as e:
        print(f"Error scanning packages: {e}")

    # Scan Docker images and containers
    try:
        result_images = subprocess.run(["docker", "images", "--format=json"], capture_output=True, text=True)
        if result_images.returncode == 0:
            profile["docker_images"] = json.loads(result_images.stdout)

        result_containers = subprocess.run(["docker", "ps", "--format=json"], capture_output=True, text=True)
        if result_containers.returncode == 0:
            profile["docker_containers"] = json.loads(result_containers.stdout)
    except Exception as e:
        print(f"Error scanning Docker: {e}")

    # Scan Kubernetes pods (if kubectl available)
    try:
        result_pods = subprocess.run(["kubectl", "get", "pods", "--all-namespaces", "-o", "json"], capture_output=True, text=True)
        if result_pods.returncode == 0:
            profile["kubernetes_pods"] = json.loads(result_pods.stdout)["items"]
    except Exception as e:
        print(f"Error scanning Kubernetes: {e}")

    # Scan GGUF models
    profile["gguf_models"] = scan_gguf_models()

    # Detect frameworks
    profile["frameworks"] = detect_frameworks()

    return profile