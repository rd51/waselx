#!/bin/bash
# WaselX Docker Registry Push & Release Script
# Usage: ./deploy-registry.sh <registry-url> <version>
# Example: ./deploy-registry.sh docker.io/yourusername 1.0.0

set -e

REGISTRY=${1:-docker.io/yourusername}
VERSION=${2:-1.0.0}
IMAGE_NAME=waselx
LOCAL_IMAGE="$IMAGE_NAME:latest"
REGISTRY_IMAGE="$REGISTRY/$IMAGE_NAME:$VERSION"
REGISTRY_LATEST="$REGISTRY/$IMAGE_NAME:latest"

echo "==============================================="
echo "WaselX Docker Release & Registry Push"
echo "==============================================="
echo "Local Image:    $LOCAL_IMAGE"
echo "Registry:       $REGISTRY"
echo "Release Tag:    $REGISTRY_IMAGE"
echo "Latest Tag:     $REGISTRY_LATEST"
echo "==============================================="
echo

# Verify image exists locally
if ! docker image inspect "$LOCAL_IMAGE" > /dev/null 2>&1; then
    echo "✗ Image $LOCAL_IMAGE not found. Building..."
    docker compose build
fi

# Tag for registry
echo "Tagging image..."
docker tag "$LOCAL_IMAGE" "$REGISTRY_IMAGE"
docker tag "$LOCAL_IMAGE" "$REGISTRY_LATEST"

# Login to registry (if needed)
read -p "Push to registry? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "Logging in to registry..."
    docker login "$REGISTRY" || true
    
    echo "Pushing $REGISTRY_IMAGE..."
    docker push "$REGISTRY_IMAGE"
    
    echo "Pushing $REGISTRY_LATEST..."
    docker push "$REGISTRY_LATEST"
    
    echo "✓ Images pushed successfully"
else
    echo "⊘ Push cancelled"
fi

# Generate deployment manifest
echo ""
echo "Generating deployment manifest..."
cat > deploy.yml <<EOF
# WaselX Release: $VERSION
# Generated: $(date)
# Registry: $REGISTRY_IMAGE

services:
  waselx-app:
    image: $REGISTRY_IMAGE
    restart: unless-stopped
    ports:
      - "5000:5000"
    environment:
      FLASK_ENV: production
      PYTHONUNBUFFERED: 1
    volumes:
      - ./data:/app/data
      - ./outputs:/app/outputs
      - ./logs:/app/logs
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:5000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
    deploy:
      resources:
        limits:
          cpus: '2'
          memory: 512M
        reservations:
          cpus: '1'
          memory: 256M
EOF

echo "✓ Deployment manifest saved to deploy.yml"
echo ""
echo "Release Summary:"
echo "  - Image:  $REGISTRY_IMAGE"
echo "  - Tag:    $VERSION"
echo "  - Latest: $REGISTRY_LATEST"
echo ""
echo "Next steps:"
echo "  1. Test in staging: docker compose -f deploy.yml up -d"
echo "  2. Verify: curl http://localhost:5000/health"
echo "  3. Deploy to production with your orchestrator"
