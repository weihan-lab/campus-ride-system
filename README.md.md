# Campus Ride - Distributed Systems Project
Welcome to the Campus Ride! This repository contains the complete implementation, deployment, and documentation for our distributed systems project, connecting student drivers with passengers.

---

# 1. System Architecture
Below is the 3-tier architecture and infrastructure layout of our distributed system.

```text
                  +-------------------+
                  |   Railway Cloud   |
                  |  (Live Hosting)   |
                  +---------+---------+
                            |
                  +---------v---------+
                  |    Kubernetes     |
                  |  (Orchestration)  |
                  +---------+---------+
                            |
         +------------------+------------------+
         |                                     |
+--------v--------+                   +--------v--------+
|  Frontend Tier  |                   |  Backend Tier   |
| (Node.js/React) | <=== REST API ===>|    (FastAPI)    |
+--------+--------+                   +--------+--------+
         |                                     |
         +------------------+------------------+
                            |
                  +---------v---------+
                  |   Database Tier   |
                  |    (Supabase)     |
                  |  PostgreSQL + RLS |
                  +-------------------+

```
# 2. Prerequisites & Tools 
Ensure you have the following tools installed before setting up the project locally.

| Tool | Version | Purpose | Installation Link |
|------|---------|---------|-------------------|
| **Python** | 3.10+ | Backend Runtime | [Download](https://www.python.org/downloads/) |
| **Node.js** | 18.x+ | Frontend Runtime | [Download](https://nodejs.org/en/download) |
| **Docker** | Latest | Containerization | [Download](https://www.docker.com/products/docker-desktop/) |
| **Minikube / kubectl** | Latest | K8s Local Cluster | [Download](https://minikube.sigs.k8s.io/docs/start/) |
| **Wireshark** | Latest | Network Analysis | [Download](https://www.wireshark.org/) |


---
# 3.Step-by-Step Instructions

Part 1: Local Setup

    1. Clone the repository: git clone https