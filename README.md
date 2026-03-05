# Autonomous DevOps Intelligence Jarvis

A self-learning DevOps intelligence system that manages, tests, patches, and evolves your entire infrastructure stack.

## Overview

This project implements a Jarvis-style DevOps intelligence system with:
- SystemScan agent that runs first on every startup to create an immutable SystemProfile
- Self-learning test loop that gets harder to fool every cycle
- Agents for monitoring, testing, patching, deploying, security auditing, and learning
- Memory systems for incident RCA and solution library

## Architecture


STARTUP SEQUENCE:
┌─────────────────────────────────────┐
│  SystemScan → SystemProfile         │
└─────────────────────────────────────┘
        ↓
Voice / Chat Input
        ↓
Planner LLM → Agent Controller
        ↓
┌──────────┬──────────┬──────────┬──────────┬──────────┬──────────┐
│  Monitor │   Test   │  Patch   │  Deploy  │ Security │  Learn   │
│  Agent   │  Agent   │  Agent   │  Agent   │  Agent   │  Agent   │
└──────────┴──────────┴──────────┴──────────┴──────────┴──────────┘


## Features

- **SystemScan**: Complete host inventory scan (OS, CPU, RAM, GPU, disk, processes, packages, Docker, Kubernetes, models)
- **Self-learning Loop**: Every failure teaches the system something new
- **Test Cycles**: 8-stage automated test cycle with STABLE gate (5 consecutive passes)
- **Memory Systems**: ChromaDB for incident RCA and solution library
- **Multi-agent Architecture**: Monitor, Test, Patch, Deploy, Security, Learn agents

## Quick Start

1. Install dependencies:
   bash
   pip install -r requirements.txt
   

2. Run the system:
   bash
   python src/main.py
   

3. Access endpoints:
   - `GET /api/system/profile` - Get current SystemProfile
   - `POST /api/test/cycle/run` - Trigger full test cycle
   - `GET /health` - Health check endpoint

## SystemScan Process

The SystemScan agent runs first on every startup and scans for:
- OS info, hardware specs, disk usage
- Network connections and listening services
- Running processes and installed packages
- Docker images and containers
- Kubernetes pods (if available)
- GGUF model files in standard cache locations
- Available inference frameworks (Ollama, llama.cpp, LM Studio, vLLM)

## Test Cycle

Each test cycle runs 8 stages:
1. Smoke: Service reachability
2. Unit: pytest with coverage ≥ 80%
3. Integration: Service-to-service API contract tests
4. Load: Locust load test (100 concurrent users, 60 seconds)
5. Chaos: Fault injection using chaos-toolkit
6. Security: CVE scanning, SAST, secret detection
7. Regression: Previous STABLE cycle tests
8. Performance: Baseline comparison

## Memory Systems

- **Incident Store**: ChromaDB for storing and retrieving incident details
- **Solution Library**: Stores reusable solution patterns with vector similarity search

## Agents

- **Monitor Agent**: Continuous service health, log anomaly detection
- **Test Agent**: Full automated test cycle orchestrator
- **Patch Agent**: Generates fixes using LLM and applies them
- **Deploy Agent**: Validates artifacts before deployment (STABLE gate)
- **Security Agent**: CVE scanning, secret detection, exposure audit
- **Learn Agent**: Extracts patterns from incidents and stores in solution library

## Self-learning Loop

Every test cycle result is processed by the Learn Agent:
1. Extract failure details and root cause
2. Embed signature and search memory for similar past failures
3. If found, reuse existing solution (with confidence tracking)
4. After successful patch, store new pattern in solution library
5. Memory decay: unused solutions lose confidence over time
6. Memory reinforcement: reused solutions gain confidence

## Requirements

- Python 3.10+
- Docker (for running inference servers)
- GPU with CUDA support (recommended for LLM inference)

## License

MIT