import asyncio
from fastapi import FastAPI, HTTPException
from src.bootstrap.system_scanner import scan_system
from src.bootstrap.system_profile import SystemProfile
from src.planner.devops_planner import route_task
from src.agents.monitor_agent import MonitorAgent
from src.agents.test_agent import TestAgent
from src.agents.patch_agent import PatchAgent
from src.agents.deploy_agent import DeployAgent
from src.agents.security_agent import SecurityAgent
from src.agents.learn_agent import LearnAgent

app = FastAPI(title="Autonomous DevOps Intelligence Jarvis")

@app.on_event("startup")
async def startup_event():
    print("Starting Jarvis system scan...")
    profile = scan_system()
    SystemProfile.write(profile)
    print("System scan complete. Profile written.")

@app.get("/api/system/profile")
async def get_system_profile():
    return SystemProfile.read()

@app.post("/api/system/rescan")
async def rescan_system():
    profile = scan_system()
    SystemProfile.write(profile)
    return {"message": "System rescanned and profile updated"}

@app.post("/api/test/cycle/run")
async def run_test_cycle():
    try:
        cycle_id = await TestAgent.run_full_cycle()
        return {"cycle_id": cycle_id, "status": "started"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/test/cycle/{cycle_id}")
async def get_test_cycle(cycle_id: str):
    return TestAgent.get_cycle_results(cycle_id)

@app.get("/api/test/stable-status")
async def get_stable_status():
    return TestAgent.get_stable_status()

@app.get("/health")
async def health_check():
    return {
        "system_scanned": True,
        "inference_available": True,
        "models_detected": len(SystemProfile.read().get("gguf_models", [])),
        "consecutive_passes": TestAgent.get_stable_status().get("passes", 0)
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)