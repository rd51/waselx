# WaselX Kubernetes Deployment Guide

## Prerequisites

```bash
# 1. Install kubectl
# 2. Configure kubeconfig to point to your cluster
# 3. Verify cluster access
kubectl cluster-info
kubectl get nodes
```

## Image Preparation

Push your image to a registry accessible from the cluster:

```bash
# Example: Docker Hub
docker tag waselx:latest docker.io/yourusername/waselx:1.0.0
docker push docker.io/yourusername/waselx:1.0.0

# Update k8s-deployment.yaml with your image URL
sed -i 's|docker.io/yourusername/waselx:latest|docker.io/yourusername/waselx:1.0.0|g' k8s-deployment.yaml
```

## Deploy to Kubernetes

### 1. Create Namespace
```bash
kubectl create namespace waselx
```

### 2. Apply Secrets (update values first!)
```bash
# Edit k8s-deployment.yaml and set real SECRET_KEY and passwords
kubectl apply -f k8s-deployment.yaml
```

### 3. Verify Deployment
```bash
# Check if pods are running
kubectl get pods -n waselx
kubectl get svc -n waselx

# View logs
kubectl logs -n waselx -l app=waselx -f

# Port forward for local testing
kubectl port-forward -n waselx svc/waselx-service 5000:80
# Open http://localhost:5000
```

### 4. Setup Ingress (optional, requires ingress-nginx)

```bash
# Install NGINX Ingress Controller
helm repo add ingress-nginx https://kubernetes.github.io/ingress-nginx
helm install nginx-ingress ingress-nginx/ingress-nginx --namespace ingress-nginx --create-namespace

# Install cert-manager for Let's Encrypt
kubectl apply -f https://github.com/cert-manager/cert-manager/releases/download/v1.14.0/cert-manager.yaml

# Deploy ingress
kubectl apply -f k8s-ingress.yaml

# Check ingress status
kubectl get ingress -n waselx
```

## Update Image

When you have a new image:

```bash
# Update the image in the deployment
kubectl set image deployment/waselx-app waselx=docker.io/yourusername/waselx:1.0.1 -n waselx

# Check rollout status
kubectl rollout status deployment/waselx-app -n waselx

# Rollback if needed
kubectl rollout undo deployment/waselx-app -n waselx
```

## Scale Deployment

```bash
# Manual scaling
kubectl scale deployment/waselx-app --replicas=5 -n waselx

# HPA will automatically scale based on CPU/memory
# Monitor HPA status
kubectl get hpa -n waselx -w
```

## Monitoring

### Logs
```bash
# All pods
kubectl logs -n waselx -l app=waselx --tail=100 -f

# Specific pod
kubectl logs -n waselx waselx-app-abc123-xyz789
```

### Shell Access
```bash
# Get a shell in a pod
kubectl exec -it -n waselx pod/waselx-app-abc123-xyz789 -- /bin/bash
```

### Health Check
```bash
# Port forward and test
kubectl port-forward -n waselx svc/waselx-service 5000:80
curl http://localhost:5000/health
```

## Cleanup

```bash
# Delete deployment
kubectl delete deployment waselx-app -n waselx

# Delete all resources in namespace
kubectl delete namespace waselx

# Delete cluster issuer (if using cert-manager)
kubectl delete clusterissuer letsencrypt-prod
```

## Troubleshooting

### Pod won't start
```bash
kubectl describe pod -n waselx waselx-app-abc123-xyz789
kubectl logs -n waselx waselx-app-abc123-xyz789
```

### Image pull errors
```bash
# Check image pull secrets
kubectl get secrets -n waselx
kubectl describe pod -n waselx waselx-app-abc123-xyz789 | grep -i image
```

### Service not accessible
```bash
kubectl get svc -n waselx
kubectl port-forward -n waselx svc/waselx-service 5000:80
curl -v http://localhost:5000/
```

### HPA not scaling
```bash
kubectl get hpa -n waselx
kubectl describe hpa -n waselx waselx-hpa
# Check metrics: kubectl get --raw /apis/custom.metrics.k8s.io/v1beta1
```

## Production Checklist

- [ ] Update image URL in `k8s-deployment.yaml`
- [ ] Set real SECRET_KEY in `waselx-secrets`
- [ ] Configure persistent volumes for your cloud provider
- [ ] Update ALLOWED_ORIGINS in ConfigMap
- [ ] Setup monitoring/logging (e.g., Prometheus, ELK)
- [ ] Configure backups for PersistentVolumes
- [ ] Setup ingress with TLS certificates
- [ ] Configure resource quotas and limits
- [ ] Setup pod disruption budgets
- [ ] Enable network policies for security
- [ ] Test disaster recovery procedures
- [ ] Document cluster access procedures
