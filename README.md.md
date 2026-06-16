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

## Part 1: Local Development Setup
**Prerequisites:** Git, Node.js 18+, Python 3.11+, Docker Desktop 4.25+, kubectl 1.28+

### Step-by-Step Setup

**Step 1.1 — Clone the repository**
```bash
git clone https://github.com/weihan-lab/campus-ride-system.git
cd dist_sys_app && ls -la


```

**Step 1.2 - Backend setup (FastAPI)**
```bash
cd backend 
python -m venv .venv 
source .venv/bin/activate
pip install -r requirements.txt 
python server.py

```
**Step 1.3 - Frontend setup (Next.js on port 3000)**
```bash
cd frontend 
npm install 
npm run dev

```
Evidence (Screenshots)

*Screenshots 1.1: FastAPI Swagger UI at http://127.0.0.1:8000/docs 
![FastAPI Swagger UI](screenshots/1.1-fastapi-swagger.png)

*Screenshot 1.2: Campus Ride Login Page at http://127.0.0.1:3000
![Campus Ride Login Page](screenshots/1.2-campus-ride-login.png)

*Screenshot 1.3: Both Terminals Running (backend + frontend )
![Both Terminals Running](screenshots/1.3-both-terminals-running-backend-and-frontend.png)

```
**DS Concepts Answers (Part 1)**

Q1:What is a 3-tier architecture? Identify which tier each service (Next.js, FastAPI, PostgreSQL) belongs to.

Answer: A 3-tier architecture is a software design pattern that divides an application into three logical and physical computing tiers. In our system:

Presentation Tier: Next.js — Handles the user interface and interactions.

Application Tier: FastAPI — Contains the core business logic and API routing.

Data Tier: PostgreSQL (Supabase) — Manages secure data storage and retrieval.

Q2:Why does the backend use asyncpg instead of the standard psycopg2 driver? What advantage does async provide in a distributed context?

Answer: FastAPI is built on an asynchronous event loop. Standard psycopg2 is synchronous and blocks the loop while waiting for database responses. asyncpg is fully asynchronous. In a distributed context, this non-blocking I/O allows the server to handle thousands of concurrent requests efficiently; while waiting for database queries to return, the server can process other users' requests, maximizing throughput and minimizing latency.

```
## Part 2: Supabase: Authentication as a Service 
*Note: Supabase provides Authentication-as-a-Service (BaaS). This demonstrates the 'Single Responsibility Principle' in distributed systems — our services focus on business logic while auth is delegated to a specialist service.*

### Step-by-Step Setup

**Step 2.1 — Create Supabase project and get credentials**
```
1. Sign up at [Supabase](https://supabase.com/) and create a new project named: `campus-ride-305630`.

2. Select the region closest to Malaysia (Singapore) to reduce latency.

3. Go to Project Settings → API → Copy the `Project URL` and `anon public key`.
```

**Step 2.2 — Configure frontend `.env.local`**
```
Create a `.env.local` file in the `frontend/` directory and add the credentials:```env
NEXT_PUBLIC_SUPABASE_URL=[https://znebxwbpdqryhhxjyjfs.supabase.co](https://znebxwbpdqryhhxjyjfs.supabase.co)
NEXT_PUBLIC_SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InpuZWJ4d2JwZHFyeWhoeGp5amZzIiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODA3MTY5ODYsImV4cCI6MjA5NjI5Mjk4Nn0.x4AuoUGz3iVPmGlvjQ4JXmYbNuOTKaZFjkOfzhbjnSE
```
**Step 2.3  — Apply database schema (SQL Editor)**
```
-- Run file: supabase/migrations/001_university_ride.sql
-- This creates the profiles table, positions table, and auth triggers.
```

Evidence (Screenshots)

*Screenshots 2.1: Supabase Project Dashboard Showing Project URL and Region
![Supabase Project Dashboard](screenshots/2.1-supabase-project-dashboard-showing-project-url-and%20region.png)

Screenshot 2.2: SQL Editor After Running Migration (showing profiles & positions tables)
![SQL Editor After Running migration](screenshots/2.2-sql-editor-after-running-migration-.png)

Screenshot 2.3: Successful Sign-up at http://127.0.0.1:3000 (user visible in Auth → Users)
![Successful Sign-up ](screenshots/2.3-successful-sign-up.png)

```
DS Concepts Answers (Part 2)
Q3: What is Row-Level Security (RLS)? How do Supabase RLS policies enforce multi-tenant data isolation?

Answer: Row-Level Security (RLS) is a PostgreSQL feature that restricts database access at the individual row level rather than just the table level. In a distributed architecture like Supabase, RLS enforces multi-tenant isolation by checking the user's authentication context (JWT) before executing a query. For example, a policy can dictate that a user can only SELECT or UPDATE a row if the row's user_id strictly matches their own auth.uid(). This ensures users cannot access or modify each other's data, maintaining security at the database layer.

Q4: Supabase uses JWT (JSON Web Tokens) for authentication. What are the three parts of a JWT and what does each contain?

Answer: A JWT consists of three parts separated by dots (xxxxx.yyyyy.zzzzz):

Header: Contains metadata about the token, specifically the token type (JWT) and the cryptographic signing algorithm used (e.g., HS256 or RS256).

Payload (Claims): Contains the actual data (claims) being transmitted, such as the user's ID (sub), role, and token expiration time (exp).

Signature: A cryptographic hash created by encoding the header and payload with a secret key. This is used by the server to verify that the token has not been tampered with in transit.

Q5: Why is selecting a geographically close Supabase region a distributed systems decision? What OSI layer is affected?

Answer: Selecting a close region (e.g., Singapore) is a crucial distributed systems decision because physical distance directly dictates propagation delay. Shorter distances reduce the Round Trip Time (RTT) for API calls, resulting in lower latency and a faster user experience. This primarily affects Layer 1 (Physical Layer) of the OSI model, as it involves the actual physical distance light or electrical signals must travel over fiber optic cables, and secondarily Layer 3 (Network Layer), as closer proximity usually means fewer router hops.

```

## Part 3: Docker Containerisation
*Note: Containers solve the "works on my machine" problem. Each service becomes an isolated, reproducible unit — essential for distributed deployment across different nodes.*

### Step-by-Step Setup

**Step 3.1 — Create `backend/Dockerfile`**
Create a `Dockerfile` inside the `backend/` directory:
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

**Step 3.2 — Create frontend/Dockerfile (Multi-stage build)**
```
FROM node:20-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build

FROM node:20-alpine AS runner
COPY --from=builder /app/.next ./.next
CMD ["npm", "start"]
```

**Step 3.3 — Build and run with Docker Compose**
```
docker-compose build
docker-compose up -d
docker-compose logs -f
docker ps
```

Evidence (Screenshots)

*Screenshots 3.1: docker ps Showing Frontend, Backend, and Postgres All UP
![docker ps ](screenshots/3.1-docker-ps-showing-campus-frontend-campus-backend-campus-postgres-all-UP.png)

*Screenshot 3.2: docker-compose Logs Showing Clean Startup (no errors)
![docker compose ](screenshots/3.2-docker-compose-logs-showing-clean-startup.png)

*Screenshot 3.3: Application Accessible at http://127.0.0.1:3000 While Running in Containers
![Application Accessible ](screenshots/3.3-application-accessible.png)

```
DS Concepts Answers (Part 3)
Q6: What is Docker layer caching? Why does the Dockerfile copy requirements.txt before the rest of the source code?

Answer: Docker builds images in distinct layers. If a layer and its preceding layers haven't changed, Docker reuses a cached version to save time. By copying requirements.txt and running pip install before copying the rest of the application code, we cache the heavy dependency installation. If a developer only changes a Python code file, Docker reuses the cached dependency layer and only rebuilds the final code layer, making rebuilds extremely fast.

Q7: What is a multi-stage Docker build? What advantage does it provide for the production frontend image?

Answer: A multi-stage build uses multiple FROM statements in a single Dockerfile. The first stage (builder) contains all the heavy tools and node modules required to compile the Next.js app. The second stage (runner) starts with a fresh, minimal base image and only copies over the final compiled artifacts (the .next folder). Advantage: This drastically reduces the final production image size, leading to faster deployment times, lower network transfer costs, and a significantly smaller security attack surface.

Q8: In docker-compose.yml, the backend uses 'postgres' (not 'localhost') as the DB hostname. Explain how Docker DNS service discovery enables this.

Answer: In a Docker Compose network, containers cannot rely on localhost to talk to each other (since localhost inside a container refers to the container itself, not the host machine). To solve this, Docker provides an internal DNS service. It automatically maps the service names defined in docker-compose.yml (like postgres or backend) to their dynamic internal container IP addresses. This provides seamless Service Discovery—the backend just connects to the hostname postgres, and Docker's DNS reliably resolves it to the correct database container.

Q9: What does the depends_on + healthcheck condition achieve in the compose file? Map this to a distributed systems concept.

Answer: depends_on ensures containers start in a specific order, but adding a healthcheck ensures the dependent container waits until the upstream service is not just started, but actually fully booted and ready to accept connections (e.g., waiting for PostgreSQL to finish initializing). In distributed systems, this maps directly to Startup Synchronization and Fault Tolerance—it prevents race conditions and cascading failures where the backend crashes repeatedly because its database dependency isn't fully initialized yet.
```

## Part 4: Kubernetes Orchestration
*Note: Kubernetes provides container orchestration: automatic pod scheduling, self-healing, load balancing, and horizontal scaling. This represents the core infrastructure of our distributed system.*

### Step-by-Step Setup
**Step 4.1 — Verify Kubernetes Cluster**
```
Ensure Kubernetes is running via Docker Desktop or Minikube:
```bash
kubectl cluster-info
kubectl get nodes
```

**Step 4.2 — Understanding the Manifests (k8s/ folder)**
```
configmap.yaml & secret.yaml — Configuration and secure credential injection.

postgres.yaml — Database Deployment + internal ClusterIP Service.

backend.yaml — FastAPI Deployment (2 replicas) + Service + Health Probes.

frontend.yaml — Next.js Deployment (2 replicas) + Service.

ingress.yaml — NGINX routing (/ to frontend, /api to backend).

hpa.yaml — Horizontal Pod Autoscaler (scales based on CPU load).
```

**Step 4.3 — Deploy the Cluster**
```
kubectl apply -f k8s/
kubectl get pods -w
kubectl get services
kubectl describe deployment campus-backend
```

**Step 4.4 — Apply Horizontal Pod Autoscaler (HPA)**
```
kubectl apply -f k8s/hpa.yaml
kubectl get hpa -w
```

Evidence (Screenshots)

*Screenshots 4.1: kubectl get pods — all pods STATUS = Running
![kubectl get podes](screenshots/4.1-kubectl-get-pods-all-pods-status-running.png)

*Screenshot 4.2: kubectl get services — ClusterIP services running
![kubectl get services](screenshots/4.2-kubectl-get-services.png)

*Screenshot 4.3: kubectl get hpa — HPA configured with targets
![kubectl get hpa](screenshots/4.3-kubectl-get-hpa.png)

*Screenshot 4.4: kubectl describe deployment campus-backend (showing replicas, probes)
![kubectl describe deployment](screenshots/4.4-%20kubectl-describe-deployment-campus-backend.png)

*Screenshot 4.5: App accessible via port-forward on localhost:3000
![App accessible via port-forward](screenshots/4.5-app-accessible-via-port-forward-on-localhost.png)

```
DS Concepts Answers (Part 4)
Q10: What is the difference between a K8s Deployment and a Pod? Why do we use Deployments?

Answer: A Pod is the smallest execution unit in K8s, usually encapsulating a single container. A Deployment is a higher-level controller that manages Pods. We use Deployments because Pods are ephemeral (they die and are not automatically restarted). A Deployment ensures a specified number of Pod replicas are always running (Self-Healing) and facilitates zero-downtime rolling updates and rollbacks.

Q11: Why is the PostgreSQL Service type ClusterIP (internal only) while the Ingress is external? What security principle does this enforce?

Answer: Exposing a database to the public internet is a massive security risk. Using ClusterIP ensures the database is strictly accessible only from within the Kubernetes internal network (by the backend pods). The Ingress acts as the single external gateway. This enforces the Principle of Least Privilege and creates a Network Demilitarized Zone (DMZ), keeping the Data Tier completely isolated from external threats.

Q12: Explain liveness vs readiness probes. What happens to traffic routing when the readiness probe fails?

Answer: A Liveness Probe checks if the application is running; if it fails, K8s kills and restarts the Pod (Self-Healing). A Readiness Probe checks if the app is ready to accept user traffic (e.g., connected to the DB). If a Readiness Probe fails, K8s does not kill the pod, but it removes the Pod's IP from the Service load balancer, completely halting traffic routing to that specific Pod until it recovers.

Q13: What is the role of a K8s Secret vs a ConfigMap? Why can't all config use ConfigMap?

Answer: A ConfigMap stores non-confidential data in plain text (e.g., NODE_ENV, backend port). A Secret is designed to store sensitive data like database passwords and API keys. While Secrets are base64 encoded (not encrypted by default in standard etcd), they integrate with K8s Role-Based Access Control (RBAC), ensuring that only authorized pods and users can mount or view the sensitive credentials. Putting API keys in a ConfigMap would expose them to anyone with read access to the cluster configuration.

Q14: The HPA scales from 2→10 pods based on CPU. Relate this to the distributed systems concept of Horizontal Scaling and explain why it is preferable to Vertical Scaling for stateless services.

Answer: HPA scaling from 2 to 10 pods is Horizontal Scaling (Scaling Out)—adding more machines/nodes to the cluster to handle load. Vertical Scaling (Scaling Up) means adding more CPU/RAM to a single machine. For stateless services (like our FastAPI backend), Horizontal Scaling is far superior because it eliminates single points of failure, allows for mathematically infinite scalability, and is more cost-effective (using many cheaper, smaller pods rather than renting a massive, expensive supercomputer).