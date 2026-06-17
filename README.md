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

```
## Part 5: Railway Cloud Deployment

Evidence:
*Screenshots 5.1:Railway Dashboard Showing Both Services Deployed
![railway dashboard](screenshots/5.1-railway-dashboard-showing-both-services-deployed.png)


*Screenshots 5.2:Railway deployment logs (clean, no errors)
![railway deployment logs](screenshots/5.2.1-railway-deployment-logs-frontend.png)

*Screenshots 5.2:Railway deployment logs (clean, no errors)
![railway deployment logs](screenshots/5.2.2-railway-deployment-logs-backend.png)

*Screenshots 5.3：Live app accessible at https://campus-ride-frontend.up.railway.app (URL in browser)
![live app accesible](screenshots/5.3-live-app-accessible-at-railway-url-browser.png)

*Screenshots 5.4：Successful login/signup on live Railway deployment
![successful login/signup](screenshots/5.4-successful-signup-on-live-railway-deployment.png)



Live Deployment URL:
Frontend (User Interface):  https://campus-ride-frontend.up.railway.app/
(Please use this link to access the EcoRide web application and test the login/signup features.)

Backend (API Documentation): https://campus-ride-backend.up.railway.app/docs
(The backend API is documented and testable via Swagger UI at the /docs endpoint.)


```
DS Concepts Answers (Part 5)
Q15: Railway is a PaaS (Platform as a Service). Compare PaaS vs IaaS vs SaaS. Where does Supabase fit?
ANSWER:  IaaS (Infrastructure as a Service): Provider manages servers, storage, and networking. You manage OS, runtime, and data.PaaS (Platform as a Service): Provider manages infrastructure, OS, and runtime. You manage only the application code and data (e.g., Railway).SaaS (Software as a Service): Provider manages everything. You use the final application. Supabase: Backend as a Service (BaaS), a specialized PaaS that provides pre-built backend infrastructure (database, auth, API) so you only build the frontend.


Q16: Why does CORS exist? Explain what happens without the Railway domain in allow_origins and which OSI layer CORS operates at.
ANSWER: A browser security feature to prevent malicious websites from making unauthorized requests to other domains using a user's active session. Missing Railway domain in allow_origins: The browser's preflight (OPTIONS) request fails. The browser blocks the frontend from reading the backend's response, triggering a CORS error.

Q17: Railway automatically provisions HTTPS. Explain the TLS handshake and why plain HTTP is insufficient for distributed auth systems.
ANSWER: It transmits data in plaintext. Passwords and auth tokens can be easily intercepted via packet sniffing.
TLS Handshake:
Client Hello: Browser sends supported encryption algorithms.
Server Hello & Certificate: Server responds with chosen algorithm and its public key certificate.
Verification: Browser verifies the certificate's authenticity.
Key Exchange: Browser encrypts a "premaster secret" using the server's public key and sends it.
Session Keys: Both generate identical symmetric session keys from the secret.
Encrypted Connection: All subsequent HTTP traffic is encrypted using these symmetric keys.
```
## Part 6: Network Analysis with Wireshark

Evidence:
*Screenshots 6.1: TCP 3-way handshake — 3 packets with SYN/SYN-ACK/ACK flags visible
![TCP 3-Way](screenshots/6.1-TCP-3way-handshake.png)

*Screenshots 6.2 HTTP GET — ALL layers expanded (Frame/Ethernet/IP/TCP/HTTP) with annotations
![http get](screenshots/6.2.1-http-get.png)

*Screenshots 6.2 HTTP GET — ALL layers expanded (Frame/Ethernet/IP/TCP/HTTP) with annotations
![http get](screenshots/6.2.2-http-get.png)

*Screenshots 6.2 HTTP GET — ALL layers expanded (Frame/Ethernet/IP/TCP/HTTP) with annotations
![http get](screenshots/6.2.3-http-get.png)

*Screenshots 6.3: HTTP POST — JSON payload visible in packet
![http post](screenshots/6.3-http-post-json-payload.png)

*Screenshots 6.4: TCP 4-way close — FIN/ACK sequence
![tcp 4-way close](screenshots/6.4-TCP-4-way-close.png)

*Screenshots 6.5: Docker container traffic showing 172.18.x.x IPs
![docker container traffic](screenshots/6.5.1-docker-container-traffic-showing-172.18.0.2.png)

*Screenshots 6.5: Docker container traffic showing 172.18.x.x IPs
![docker container traffic](screenshots/6.5.2-docker-container-traffic-showing-172.18.0.2.png)

*Screenshots 6.6: TLS/HTTPS Analysis (Railway Production)
![tls/https](screenshots/6.6-TLS-analysis.png)

```
Exercise 6.1
ANSWER: In this exercise, the Wireshark capture clearly shows the first three packets (Packet No. 1, 2, and 3) establishing a connection between the client and the server (127.0.0.1:8000). This occurs at OSI Layer 4 (Transport Layer). I observed the standard TCP 3-way handshake sequence:
1. Client sends a [SYN] packet to the server.
2. Server replies with a [SYN, ACK] packet.
3. Client acknowledges with an [ACK] packet.
Distributed Systems Concept:
This illustrates the concept of Reliable Communication. In a distributed system, nodes must guarantee that the communication channel is established and both parties are ready before sending actual application data. The TCP handshake ensures this reliability and synchronization across the network


Exercise 6.2
ANSWER: In this exercise, I captured an HTTP GET request to the /api/v1/students/ endpoint. By expanding the packet details, I observed the data encapsulation process across multiple OSI layers:
Layer 7 (Application Layer): The HTTP protocol defines the GET method, endpoint path, and headers (like User-Agent and Host).
Layer 4 (Transport Layer): The TCP protocol shows the Source Port (60309) and Destination Port (8000), managing the end-to-end delivery.
Layer 3 (Network Layer): The IPv4 protocol shows the Source IP and Destination IP (both 127.0.0.1 for local loopback testing), handling the logical routing.
Layer 2 (Data Link Layer): Represented by the Null/Loopback frame details.
Distributed Systems Concept:
This illustrates the concepts of Encapsulation and Protocol Abstraction. In a distributed cloud-native architecture, developers only need to design the Application Layer (Layer 7 REST API). The underlying OSI layers automatically encapsulate this JSON/HTTP request into packets and route it to the correct microservice or backend container, abstracting the complex networking details away from the application logic.

Exercise 6.3
ANSWER: In this exercise, the Wireshark capture demonstrates an HTTP POST request carrying data. By examining the packet, I observed the payload at OSI Layer 6 (Presentation Layer). The capture clearly shows the HTTP payload expanded to reveal the JavaScript Object Notation (JSON) data. The raw object {"name":"Ali","matric_id":"S001",...} was successfully serialized and transmitted over the network to the /api/v1/students/ endpoint.
Distributed Systems Concept:
This illustrates the concept of Data Serialization and Interoperability. In distributed systems, different components or microservices might be written in different programming languages. They need a universal, standardized format (like JSON) at the Presentation Layer to serialize complex data structures into a stream of bytes for transmission, ensuring that the receiving server can correctly parse and understand the payload.

Exercise 6.4
ANSWER: In this capture for Exercise 6.4, I observed the connection termination process at OSI Layer 4 (Transport Layer). The Wireshark packet list clearly shows the standard TCP 4-way teardown sequence (Packets 12 to 15). By expanding the TCP protocol details, I verified the presence of the FIN and ACK flags. The sequence occurs as follows:
1. ​Client initiates termination with a [FIN, ACK].
2. ​Server acknowledges it with an [ACK].
3. ​The server sends its own [FIN, ACK] to close its side.
4. ​Client sends a final [ACK].
​Distributed Systems Concept:
This sequence illustrates the concept of Graceful Teardown and Resource Management. In distributed systems, computing nodes and servers have limited resources (such as memory and open ports). A graceful 4-way termination ensures that both the client and the backend server have completely finished transmitting data before safely closing the connection and releasing network resources, preventing memory leaks and orphaned connections.

Exercise 6.5
ANSWER: During the deployment, I successfully verified the containerized networking by assigning static IP addresses within a shared virtual bridge (172.18.0.0/16 subnet).
​Technical Limitation Note: As I am running Docker on a Windows/WSL2 environment, internal container-to-container traffic (on port 5432) remains encapsulated within the Linux kernel bridge (docker0), which is not observable from the Windows host network adapters. However, the connectivity was definitively validated via the successful end-to-end routing of the HTTP request to the database execution layer, as evidenced by the specific SQL exceptions returned from the backend.
​Distributed Systems Concept:
This illustrates Network Virtualization and Service Discovery. Containers operate within an isolated virtual network where they discover each other via internal DNS rather than hardcoded IPs. This architectural decoupling allows for horizontal scalability, as the network topology remains consistent regardless of the underlying host environment.

Exercise 6.6
ANSWER: In this exercise, I analyzed the production traffic to the Railway server. At OSI Layer 6/7 (Presentation and Application Layers), the capture demonstrates a successful TLSv1.3 handshake.
1.​The client sends a Client Hello containing the SNI (campus-ride-system-production-0520.up.railway.app).
2. ​The server responds with a Server Hello to establish cryptographic keys.
3. ​Following the handshake, all HTTP traffic is encapsulated as Application Data. The actual JSON payload and HTTP headers are entirely encrypted and invisible to network packet analyzers.
​Distributed Systems Concept:
This illustrates the critical concept of Secure Communication and Confidentiality. In distributed systems, especially those using stateless authentication like Supabase JWTs, tokens are transmitted with every request. Without TLS encryption, anyone intercepting the traffic (man-in-the-middle) could easily read the plain HTTP request and steal the JWT to impersonate a user. The TLS handshake establishes a secure, encrypted tunnel, ensuring that sensitive authentication tokens and user data remain strictly confidential over public networks.

```

```
DS Concept (Part 6)
Q18: Why does TCP use a 3-way handshake before data exchange? What would happen without it in a distributed system?
​ANSWER: TCP uses a 3-way handshake (SYN, SYN-ACK, ACK) to ensure both the client and server are ready and to synchronize initial sequence numbers.Without it: In a distributed system, without this synchronization, we would face two main issues:
​Unreliable State: The client might send data before the server has allocated memory or opened a port, causing packet loss.
​Ambiguity: Old or delayed packets from a previous connection could be confused with current data. The handshake establishes a "fresh" connection state, ensuring data integrity and delivery order.

​Q19: From your HTTP GET capture, list the exact contents of: (a) Layer 3 header, (b) Layer 4 header, (c) Layer 7 payload.
​ANSWER: (Based on your Exercise 6.2 capture):
​(a) Layer 3 (Network Layer) Header: Source IP (127.0.0.1), Destination IP (127.0.0.1), Protocol (TCP/6), and TTL (Time-to-Live).
​(b) Layer 4 (Transport Layer) Header: Source Port (e.g., 60309), Destination Port (8000), and Sequence/Acknowledgment numbers.
​(c) Layer 7 (Application Layer) Payload: The HTTP request line (GET /api/v1/students/ HTTP/1.1), the Host header (127.0.0.1:8000), and User-Agent info.

​Q20: In Exercise 6.5, how does the Docker DNS resolver translate 'postgres' to its container IP? Which distributed systems concept is this?
​ANSWER: Translation: Docker includes an embedded DNS server. When a container (backend) tries to reach a service name (like postgres), the DNS resolver intercepts the request and maps the service name to the specific internal IP address (e.g., 172.18.0.3) currently assigned to that service's container.
​Distributed Systems Concept: This is Service Discovery. In a distributed environment, containers are ephemeral (they start and stop frequently); Service Discovery allows services to locate each other dynamically without hardcoding IP addresses.

​Q21: In Exercise 6.6, you cannot see the HTTP content in HTTPS packets. Explain what the TLS handshake establishes and why this is essential for the Supabase JWT authentication flow.
​ANSWER:​ TLS Handshake: It establishes an encrypted, secure tunnel between the client and server. It involves negotiating cryptographic algorithms, verifying the server’s certificate, and generating shared secret keys used to encrypt all subsequent data.
​Essential for JWT Flow: In a distributed system, a JWT (JSON Web Token) acts as the "identity card" for the user. If this token is sent over plain HTTP, anyone sniffing the network (Man-in-the-Middle) can steal the token and impersonate the user. TLS ensures that the JWT—and the sensitive data inside it—remains encrypted and tamper-proof during transmission, which is non-negotiable for secure authentication.

```
## 🏗️ 5. Kubernetes Manifest Files
The production-grade Kubernetes orchestration infrastructure is completely declared within the `/k8s` folder. The components cooperate to maintain microservice availability, declare isolation boundaries, and automate scalability under stress:

| Manifest File | Target API Resources | Operational Description & Distributed Role |
| :--- | :--- | :--- |
| **`configmap.yaml`** | `v1/ConfigMap` | Centralizes non-sensitive global environment variables (`NEXT_PUBLIC_API_URL`, `NODE_ENV`). Allows runtime configuration updates decoupling from container images. |
| **`secret.yaml`** | `v1/Secret` | Encrypts and injects sensitive production credentials (`SUPABASE_URL`, `SUPABASE_ANON_KEY`, `DATABASE_URL`) via base64 encoding to maintain system perimeter security. |
| **`postgres.yaml`** | `apps/v1/Deployment`<br>`v1/Service` | Deploys a dedicated SQL database pod tied to an internal `ClusterIP` service. Ensures only the application runtime layer can tap data nodes. |
| **`backend.yaml`** | `apps/v1/Deployment`<br>`v1/Service` | Ordinates high-availability FastAPI pod replicas (min 2). Configures explicit `livenessProbe` and `readinessProbe` paths on `/health` to execute systemic self-healing. |
| **`frontend.yaml`** | `apps/v1/Deployment`<br>`v1/Service` | Exposes the Next.js frontend pod endpoints via standard internal service layers, ensuring uniform cluster-wide availability tracking. |
| **`ingress.yaml`** | `networking.k8s.io/v1/Ingress` | Acts as the core Layer 7 reverse proxy/load balancer. Strips incoming traffic to route edge `/` paths to the UI and `/api/v1` traffic cleanly to backend routing clusters. |
| **`hpa.yaml`** | `autoscaling/v1/HorizontalPodAutoscaler` | Enforces automated runtime infrastructure scaling. Monitors real-time pod metrics to scale API workers from 2 to 10 pods when CPU load scales past 70%. |

---

## 🔬 6. Wireshark Filter Reference Table
Deep packet inspection (DPI) and explicit packet auditing are executed through network analysis interfaces to track active states across the OSI protocol layers. The following telemetry filters were established to run system tracing:

| Wireshark Display Filter | Relevant OSI Layer | Captured Intercept Scope & Distributed System Context |
| :--- | :--- | :--- |
| **`tcp.port == 8000`** | Layer 4 (Transport) | Isolates all low-level ingress/egress raw TCP streams hitting our FastAPI backend. Used to diagnose sequence verification, timing bounds, and port maps. |
| **`http.request.method == "POST"`** | Layer 7 (Application) | Traps inbound student/driver registration and login payloads. Validates how objects are formatted and parsed under Layer 6 JSON text serialization. |
| **`tls.handshake.type == 1`** | Layer 7 (Application) / Security | Isolates standard TLS `Client Hello` payloads. Verifies that authorization traffic out to Supabase BaaS or Railway clouds is strictly encrypted and safe from MITM eavesdropping. |
| **`ip.addr == 127.0.0.1`** | Layer 3 (Network) | Evaluates internal loopback node-to-node packets. Used to capture TCP 3-way handshakes, 4-way connection closes, and structural timing delays. |
## Part 7: Load Testing & Horizontal Scaling

Evidence:

*Screenshots 7.1: Artillery test running — showing requests/sec and response times
![Artillery test running](screenshots/7.1.1-artillery-test-running-showing-requests-sec.png)

*Screenshots 7.2 & 7.3: Railway dashboard CPU graph during the load test (showing spike)  K8s HPA scaling (optional if testing locally with metrics-server)

![railway dashboard ](screenshots/7.2，7.3-railway-dashboard-cpu-graph-during-the%20load-test.png)

```
DS Concept

Q22: From your Artillery results, record average response time at 10 req/s vs 50 req/s. What does the difference tell you about the system's throughput limits?
ANSWER: Data: According to the finalized Artillery summary report, the system recorded a baseline mean response time of 268.0 ms (median: 228.2 ms) at 10 req/s during Phase 1. When the load expanded by 500% to 50 req/s in Phase 2, the cumulative mean response time unexpectedly optimized to 209.3 ms (median: 202.4 ms).
Throughput Limits Analysis: Exactly 6,600 out of 6,600 requests successfully returned HTTP 200 OK with zero failures (vusers.failed: 0). The fact that response times remained entirely stable (and even slightly decreased due to container runtime warming/connection reuse) under peak stress proves that the system's actual throughput limit is far higher than 50 req/s. The asynchronous Uvicorn/FastAPI pipeline handled the concurrent network I/O effortlessly, without encountering any CPU throttling or worker thread starvation.


Q23: Railway scales by adding container replicas (horizontal). How does the K8s load balancer distribute requests between replicas? Does the Campus Ride backend need to be stateful or stateless for this to work correctly?
ANSWER: The Kubernetes load balancer uses a Round-Robin algorithm to distribute sequential incoming Layer 7 HTTP requests evenly among all healthy container replicas.  State Requirement: The backend must be stateless. Because Round-Robin routes consecutive requests from the same user to different replicas, a stateful backend would lose session data. Being stateless allows any replica to handle any request, offloading data persistence to Supabase/PostgreSQL.

```

---
# 4. Environment Variables Reference Table 
To run this project locally or deploy it to the cloud, need to configure the following variables.


| Variable Name | Service | Description | Where to get |
|------|---------|---------|-------------------|
| NEXT_PUBLIC_SUPABASE_URL | Frontend | The API URL for connecting to the Supabase database. | Supabase Dashboard > Project Settings > API |
| NEXT_PUBLIC_SUPABASE_ANON_KEY | Frontend | The anonymous key for client-side Supabase access. |Supabase Dashboard > Project Settings > API|
| NEXT_PUBLIC_SUPABASE_PUBLISHABLE_KEY | Frontend | The publishable key for public database operations. | Supabase Dashboard > Project Settings > API |
| NEXT_PUBLIC_API_URL | Frontend | The base URL for the backend FastAPI service.| Railway Backend Service > Settings > Public Networking |
| DATABASE_URL | Backend | Connection string for the PostgreSQL database (Asyncpg). | Supabase Dashboard > Project Settings > Database |
|PORT | Backend | The port number the backend application listens on.| Automatically assigned by Railway (Default: 8080) |

---

# 5. Kubernetes Manifest Files
The production-grade Kubernetes orchestration infrastructure is completely declared within the `/k8s` folder. The components cooperate to maintain microservice availability, declare isolation boundaries, and automate scalability under stress:

| Manifest File | Target API Resources | Operational Description & Distributed Role |
| :--- | :--- | :--- |
| **`configmap.yaml`** | `v1/ConfigMap` | Centralizes non-sensitive global environment variables (`NEXT_PUBLIC_API_URL`, `NODE_ENV`). Allows runtime configuration updates decoupling from container images. |
| **`secret.yaml`** | `v1/Secret` | Encrypts and injects sensitive production credentials (`SUPABASE_URL`, `SUPABASE_ANON_KEY`, `DATABASE_URL`) via base64 encoding to maintain system perimeter security. |
| **`postgres.yaml`** | `apps/v1/Deployment`<br>`v1/Service` | Deploys a dedicated SQL database pod tied to an internal `ClusterIP` service. Ensures only the application runtime layer can tap data nodes. |
| **`backend.yaml`** | `apps/v1/Deployment`<br>`v1/Service` | Ordinates high-availability FastAPI pod replicas (min 2). Configures explicit `livenessProbe` and `readinessProbe` paths on `/health` to execute systemic self-healing. |
| **`frontend.yaml`** | `apps/v1/Deployment`<br>`v1/Service` | Exposes the Next.js frontend pod endpoints via standard internal service layers, ensuring uniform cluster-wide availability tracking. |
| **`ingress.yaml`** | `networking.k8s.io/v1/Ingress` | Acts as the core Layer 7 reverse proxy/load balancer. Strips incoming traffic to route edge `/` paths to the UI and `/api/v1` traffic cleanly to backend routing clusters. |
| **`hpa.yaml`** | `autoscaling/v1/HorizontalPodAutoscaler` | Enforces automated runtime infrastructure scaling. Monitors real-time pod metrics to scale API workers from 2 to 10 pods when CPU load scales past 70%. |

---

# 6. Wireshark Filter Reference Table
Deep packet inspection (DPI) and explicit packet auditing are executed through network analysis interfaces to track active states across the OSI protocol layers. The following telemetry filters were established to run system tracing:

| Wireshark Display Filter | Relevant OSI Layer | Captured Intercept Scope & Distributed System Context |
| :--- | :--- | :--- |
| **`tcp.port == 8000`** | Layer 4 (Transport) | Isolates all low-level ingress/egress raw TCP streams hitting our FastAPI backend. Used to diagnose sequence verification, timing bounds, and port maps. |
| **`http.request.method == "POST"`** | Layer 7 (Application) | Traps inbound student/driver registration and login payloads. Validates how objects are formatted and parsed under Layer 6 JSON text serialization. |
| **`tls.handshake.type == 1`** | Layer 7 (Application) / Security | Isolates standard TLS `Client Hello` payloads. Verifies that authorization traffic out to Supabase BaaS or Railway clouds is strictly encrypted and safe from MITM eavesdropping. |
| **`ip.addr == 127.0.0.1`** | Layer 3 (Network) | Evaluates internal loopback node-to-node packets. Used to capture TCP 3-way handshakes, 4-way connection closes, and structural timing delays. |


---
# 7. Live Deployment & Endpoints


The system is fully deployed on Railway cloud infrastucture.

   -Frontend (User Interface): https://campus-ride-frontend.up.railway.app

   -Backend APU Documentation (Swagger UI): https://campus-ride-backend.up.railway.app/docs

Key API Endpoints

    -POST /api/v1/students/ - Register a new student account.

    -GET /api/v1/drivers/ - Retrieve a list of available drivers.

    -POST /api/v1/rides/ - Create a new ride request.
---

# 8.Troubleshooting
During the development and cloud deployment phases, we encountered and resolved several technical challenges:

| Issue | Root Cause | Solution| 
|------|---------|---------|
| Frontend fails to read Supabase keys in production (Missing .env.local) | Next.js requires NEXT_PUBLIC_ variables at build-time. Since .env.local is git-ignored, Docker builds on Railway fail to access these keys if they are only provided at runtime. | We updated the frontend/Dockerfile to include ARG and ENV instructions (e.g., ARG NEXT_PUBLIC_API_URL) right before the RUN npm run build command, allowing Docker to fetch variables from Railway during the build process. | 
| Backend Deployment Error: "Application failed to respond" on Railway| The FastAPI server was defaulting to localhost (127.0.0.1), making it inaccessible from the external Railway network. | We modified the Railway custom start command to bind the host to 0.0.0.0 globally: python -m uvicorn app.main:app --host 0.0.0.0 --port 8080. | 
| Frontend blocked by CORS policy when fetching API | The frontend and backend are hosted on different domains. The backend's security configuration rejected incoming cross-origin HTTP requests from the frontend URL. | We updated the allow_origins array in the backend's main.py CORS middleware to explicitly include the live frontend domain: https://campus-ride-frontend.up.railway.app. | 

---
# 9. Team Member Contributions
|Name | Matric No. | Role & Contributions| 
|------|---------|---------|
| TAN WEI HAN | 305630 |  Lead Developer / Cloud Architect: Setup Railway deployments, configured Dockerfiles for CI/CD, resolved CORS and build-time variable issues, and implemented core API routes. | 
| YAP YEW JOE | 306128 |  Frontend Developer: Designed the Next.js UI components, integrated Supabase authentication, and connected frontend forms to backend REST APIs.|
| KHO ZHI KUAN | 304724 | Database & Networking: Configured Supabase PostgreSQL schema, managed Kubernetes manifests, and performed network traffic analysis using Wireshark.|
