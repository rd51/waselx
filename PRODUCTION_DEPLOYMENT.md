# WaselX Production Deployment Guide

## Overview

WaselX is a **Delivery Network Optimization Platform** deployed as a containerized Flask application. This guide covers production deployment across Docker Compose, Docker Swarm, and Kubernetes.

**System Components:**
- 15 network nodes (7 hubs, 8 distribution centers)
- 24 bidirectional routes with multiple metrics (distance, time, cost)
- REST API with 8 endpoints
- Interactive web dashboard (HTML/CSS/JavaScript)
- Algorithms: Dijkstra, Floyd-Warshall, MST (Kruskal's, Prim's), BFS/DFS, Sorting, Searching

---

## 1. Docker Compose (Single Host)

### Quick Start (Development)
```bash
cd "d:\Downloads\S.P. Jain\DSA\Group Final Project"
docker compose up -d
# Access: http://localhost:5000
```

### Production Deployment (with hardening)

**Files:**
- `docker-compose.yml` - Base configuration (hardened, no `version` key)
- `.env.prod` - Environment variables (from `.env.prod.template`)
- `Dockerfile` - Multi-stage Python 3.11-slim build
- `requirements-docker.txt` - Dependencies (Flask, matplotlib, plotly, etc.)

**Setup:**
```bash
# 1. Copy template to production env file
cp .env.prod.template .env.prod

# 2. Edit .env.prod with your values
# - Set FLASK_ENV=production
# - Generate SECRET_KEY: openssl rand -base64 32
# - Configure ALLOWED_ORIGINS for your domain

# 3. Create data/output directories
mkdir -p data outputs logs

# 4. Start services
docker compose up -d --wait

# 5. Verify health
curl http://localhost:5000/health
docker compose ps
```

**Features:**
- Restart policy: `unless-stopped`
- Resource limits: 2 CPU / 512MB RAM (app)
- Health checks every 30s with 40s startup grace period
- Volume mounts: `/app/data`, `/app/outputs`, `/app/logs`
- Logging: JSON format, 10MB max per file, 3 file retention

**Scale horizontally with reverse proxy:**
```bash
# Optional: nginx reverse proxy with HTTPS
docker compose -f docker-compose.yml -f docker-compose.prod.yml up -d
```

This adds:
- nginx on ports 80 → 443 (HTTP → HTTPS redirect)
- Rate limiting (10 req/s general, 50 req/s API)
- Gzip compression
- Cache zones (static: 100m, API: 50m)
- Security headers (HSTS, CSP, X-Frame-Options)

---

## 2. Docker Registry (Push & Release)

### Prerequisites
- Docker account (docker.io) OR private registry (e.g., ECR, GCR, Harbor)

### Push to Registry

**Option A: Bash (Linux/macOS)**
```bash
chmod +x deploy-registry.sh
./deploy-registry.sh docker.io/yourusername 1.0.0
```

**Option B: PowerShell (Windows)**
```powershell
.\deploy-registry.ps1 -Registry "docker.io/yourusername" -Version "1.0.0"
```

**Manual:**
```bash
# Tag image
docker tag waselx:latest docker.io/yourusername/waselx:1.0.0
docker tag waselx:latest docker.io/yourusername/waselx:latest

# Login
docker login docker.io

# Push
docker push docker.io/yourusername/waselx:1.0.0
docker push docker.io/yourusername/waselx:latest
```

### Deployment File
After push, a `deploy.yml` is generated with the registry image reference:
```bash
docker compose -f deploy.yml up -d
```

---

## 3. Kubernetes (Cloud / Multi-Node)

### Prerequisites
```bash
# Install kubectl
brew install kubectl    # macOS
choco install kubernetes-cli  # Windows
# Or download from: https://kubernetes.io/docs/tasks/tools/

# Configure cluster access
kubectl config use-context your-cluster-name
kubectl cluster-info
```

### Deploy to Kubernetes

**Files:**
- `k8s-deployment.yaml` - Deployment, Service, HPA, PVCs, NetworkPolicy
- `k8s-ingress.yaml` - Ingress (HTTPS with Let's Encrypt), RBAC, ServiceMonitor
- `K8S_DEPLOYMENT_GUIDE.md` - Detailed K8s walkthrough

**Step 1: Update image URL**
```bash
# Edit k8s-deployment.yaml
# Change: image: docker.io/yourusername/waselx:latest
# To your actual registry image

sed -i 's|docker.io/yourusername/waselx:latest|your.registry/waselx:1.0.0|g' k8s-deployment.yaml
```

**Step 2: Create namespace & deploy**
```bash
kubectl create namespace waselx
kubectl apply -f k8s-deployment.yaml
```

**Step 3: Verify**
```bash
kubectl get pods -n waselx
kubectl get svc -n waselx
kubectl logs -n waselx -l app=waselx -f

# Port forward for testing
kubectl port-forward -n waselx svc/waselx-service 5000:80
# Open http://localhost:5000
```

**Step 4: Setup Ingress (optional)**
```bash
# Install ingress-nginx
helm repo add ingress-nginx https://kubernetes.github.io/ingress-nginx
helm install nginx-ingress ingress-nginx/ingress-nginx \
  --namespace ingress-nginx --create-namespace

# Install cert-manager
kubectl apply -f https://github.com/cert-manager/cert-manager/releases/download/v1.14.0/cert-manager.yaml

# Deploy ingress with HTTPS
kubectl apply -f k8s-ingress.yaml

# Check status
kubectl get ingress -n waselx
```

**Step 5: Monitor & Scale**
```bash
# HPA auto-scales between 3-10 replicas based on CPU/memory
kubectl get hpa -n waselx -w

# Manual scale
kubectl scale deployment/waselx-app --replicas=5 -n waselx

# View events
kubectl describe deployment waselx-app -n waselx
```

### K8s Features
- **HA Setup:** 3 pod replicas, rolling updates, pod affinity
- **Autoscaling:** HPA on CPU (70%) and memory (80%)
- **Security:** Network policies, RBAC, non-root user (1000), read-only filesystem (app)
- **Persistence:** PVCs for data (10Gi), outputs (5Gi)
- **Monitoring:** ServiceMonitor for Prometheus, liveness/readiness probes
- **Resilience:** Pod disruption budget (min 2), 30s termination grace period

---

## 4. Environment Variables

**Key Configuration (.env.prod):**

| Variable | Default | Purpose |
|----------|---------|---------|
| `FLASK_ENV` | production | App environment |
| `FLASK_DEBUG` | 0 | Debug mode (disable in production) |
| `SECRET_KEY` | (required) | Session signing key (min 32 chars) |
| `LOG_LEVEL` | INFO | Logging verbosity |
| `ALLOWED_ORIGINS` | localhost:5000 | CORS allowed origins |
| `WORKERS` | 4 | uWSGI worker processes |
| `REDIS_URL` | (optional) | Redis cache backend |
| `SENTRY_DSN` | (optional) | Error tracking URL |

---

## 5. Monitoring & Health Checks

### Health Endpoint
```bash
curl http://localhost:5000/health
# Response: {"status": "healthy", "timestamp": "2026-05-03T09:00:00"}
```

### API Endpoints
- `GET /api/simulator-status` - Network state, blocked edges, connectivity
- `POST /api/shortest-path` - Find optimal route (distance/time/cost)
- `POST /api/compare-paths` - Compare all criteria for a route pair
- `GET /api/mst` - Minimum spanning tree metrics
- `GET /api/sorting-benchmark` - Sorting algorithm performance
- `GET /api/search-benchmark` - Search algorithm comparison
- `POST /api/road-closure` - Simulate edge blocking/restoration

### Logs
```bash
# Docker Compose
docker compose logs -f waselx-app

# Kubernetes
kubectl logs -n waselx -l app=waselx -f
kubectl logs -n waselx pod/waselx-app-xyz --tail=200

# Check specific pod
kubectl describe pod -n waselx waselx-app-xyz
```

### Performance Metrics
```bash
# Docker resource usage
docker stats waselx-simulator

# Kubernetes metrics (requires metrics-server)
kubectl top pods -n waselx
kubectl top nodes
```

---

## 6. Troubleshooting

### Container won't start
```bash
docker compose logs waselx-app
# Check: Python imports, Flask syntax, port availability
```

### Health check failing
```bash
# Test endpoint directly
curl -v http://localhost:5000/health

# Check logs for startup errors
docker compose logs --tail=50
```

### High memory usage
```bash
# Adjust limits in docker-compose.yml or k8s-deployment.yaml
# Increase log rotation: max-size: "5m" (from "10m")
# Reduce cache sizes in nginx.conf
```

### API timeout (504 Gateway Timeout)
```bash
# Increase proxy_read_timeout in nginx.conf
# Or reduce HPA scale-up time in k8s-deployment.yaml
```

---

## 7. Backup & Recovery

### Docker Compose
```bash
# Backup data volumes
docker run --rm -v data:/source -v $(pwd):/backup \
  alpine tar czf /backup/data-backup.tar.gz -C /source .

# Restore
docker run --rm -v data:/target -v $(pwd):/backup \
  alpine tar xzf /backup/data-backup.tar.gz -C /target
```

### Kubernetes
```bash
# Backup PVC
kubectl cp waselx/waselx-app-xyz:/app/data ./data-backup

# Restore
kubectl cp ./data-backup waselx/waselx-app-xyz:/app/data
```

---

## 8. Security Checklist

- [ ] Change `SECRET_KEY` to a strong random value
- [ ] Set `FLASK_DEBUG=0` in production
- [ ] Use HTTPS (nginx proxy or K8s ingress)
- [ ] Configure `ALLOWED_ORIGINS` to your domain only
- [ ] Enable network policies (K8s) or firewall rules
- [ ] Run container as non-root user
- [ ] Implement rate limiting (enabled by default)
- [ ] Regular dependency updates (`pip list --outdated`)
- [ ] Enable logging and monitoring
- [ ] Use secrets management (Kubernetes secrets, Vault)
- [ ] Implement CI/CD pipeline with image scanning
- [ ] Regular backups of persistent data

---

## 9. Scaling Strategy

### Horizontal (add replicas)
```bash
# Docker Compose: Add multiple services
# services:
#   waselx-app-1: ...
#   waselx-app-2: ...
# + reverse proxy (nginx)

# Kubernetes: HPA auto-scales 3-10 replicas
# Or: kubectl scale deployment/waselx-app --replicas=10
```

### Vertical (increase resources)
```bash
# Docker: Increase limits in compose file
# resources:
#   limits:
#     cpus: '4'
#     memory: 1024M

# Kubernetes: Edit deployment resource requests/limits
# kubectl set resources deployment waselx-app \
#   --limits=cpu=2,memory=512Mi \
#   --requests=cpu=1,memory=256Mi
```

### Caching (Redis)
```bash
# Uncomment in docker-compose.prod.yml
# Then set REDIS_URL in .env.prod
```

---

## 10. Rollback & Updates

### Docker Compose
```bash
# Update image tag in docker-compose.yml
docker compose pull
docker compose up -d

# Rollback to previous version
git checkout HEAD~ docker-compose.yml
docker compose up -d
```

### Kubernetes
```bash
# Update image
kubectl set image deployment/waselx-app \
  waselx=docker.io/yourusername/waselx:1.0.1 -n waselx

# Check rollout
kubectl rollout status deployment/waselx-app -n waselx

# Rollback if needed
kubectl rollout undo deployment/waselx-app -n waselx
kubectl rollout history deployment/waselx-app -n waselx
```

---

## Support & Documentation

- **Dashboard:** http://localhost:5000 (local) or https://yourdomain.com (production)
- **API Docs:** View endpoint details in `app.py`
- **Network Data:** See `data/network.py` for 15 nodes & 24 edges
- **Algorithms:** Implementations in `task_a/`, `task_d/`, `task_e/`

---

**Last Updated:** May 3, 2026  
**Version:** 1.0.0  
**Status:** Production Ready
