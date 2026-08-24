# PhaseBench: Benchmark for Structural Inefficiency in Multi-Agent Systems

A reproducible agent-based model (ABM) demonstrating a phase transition in collective intelligence caused by changes in social topology (egalitarian vs. hierarchical structures).

[![DOI](https://zenodo.org/badge/1336669135.svg)](https://doi.org/10.5281/zenodo.21988314)
[![Python](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## 🧠 TL;DR (Executive Summary)
Modern LLM orchestrators suffer from "Cognitive Obesity": as the number of agents ($N$) grows, coordination costs rise non-linearly due to rigid RBAC hierarchies. This repository provides a benchmark to measure this degradation before it impacts OPEX. We show that adding more GPU does not solve protocol inefficiency.

## 📊 Problem Statement
In flat (egalitarian) multi-agent systems, average cognitive ability scales with resource availability. However, introducing a single point of authority ("Alpha" node / Hard RBAC) creates a structural bottleneck. Our simulation demonstrates an instant drop in group performance (~30% reduction in $Avg\_Cog$) even when total system resources remain constant.

## 🛠 Tech Stack & Architecture
*   **Language:** Python >= 3.9
*   **Core Dependencies:** `numpy`, `dataclasses`
*   **Methodology:** Agent-Based Modeling (ABM) utilizing immutable dataclasses (`@dataclass(frozen=True)`) and stochastic processes.
*   **Reproducibility:** Fixed random seeds (`seed=42`) ensure deterministic results across runs.

## ⚡ Quick Start (Standalone)
Clone the repository and install dependencies:
```bash
git clone https://github.com/YOUR_USERNAME/agent_sim_ref.git
cd agent_sim_ref
pip install -r requirements.txt
```
Run the baseline simulation:
```bash
python agent_sim_ref.py
```
The script will generate outputs/simulation_log.json


## 🐳 Production Run (Dockerized)

For enterprise-grade reproducibility, use the provided Docker environment.

### Шаг 1: Create Dockerfile

Create in the root project folder file `Dockerfile` (without extension) with following text:

```dockerfile
# Official Python
FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends gcc && \
    rm -rf /var/lib/apt/lists/*

# Setup working directory in the container
WORKDIR /app

# Copy files and dependencies into the image 
COPY requirements.txt .
COPY agent_sim_ref.py .

# Setup Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Command to start the container 
CMD ["python", "./agent_sim_ref.py"]
```

### Шаг 2: Building and launching image

1. Open the terminal in the project folder and run the commands:
    ```bash
    docker build -t phasebench .
    ```
(Dot at the end is required).

2. Launching the container:
To ensure that the results are saved on your computer and do not disappear when the container is stopped, you need to attach a volume (folder):
    ```bash
    docker run --rm -v "$(pwd)/outputs":/app/outputs phasebench
    ```


## 📈 Key Metrics

The simulator tracks the following variables over generations:
avg_cog: Mean cognitive ability of the population.
mode: Social regime (Egalitarianism or Hierarchy).
resource_penalty: Computational cost imposed on high-capacity nodes.


## 📄 Citation

If you use this benchmark in your research or industrial testing, please cite this project using the DOI badge above.

## 🤝 Industrial Application

This ABM serves as a stress-test (Digital Twin) for corporate AI platforms. It predicts efficiency loss during organizational restructuring without requiring access to sensitive PII data.
