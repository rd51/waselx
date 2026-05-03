# WaselX Docker Registry Push & Release (Windows PowerShell)
# Usage: .\deploy-registry.ps1 -Registry "docker.io/yourusername" -Version "1.0.0"

param(
    [string]$Registry = "docker.io/yourusername",
    [string]$Version = "1.0.0"
)

$ImageName = "waselx"
$LocalImage = "$ImageName`:latest"
$RegistryImage = "$Registry/$ImageName`:$Version"
$RegistryLatest = "$Registry/$ImageName`:latest"

Write-Host "===============================================" -ForegroundColor Cyan
Write-Host "WaselX Docker Release & Registry Push" -ForegroundColor Cyan
Write-Host "===============================================" -ForegroundColor Cyan
Write-Host "Local Image:    $LocalImage"
Write-Host "Registry:       $Registry"
Write-Host "Release Tag:    $RegistryImage"
Write-Host "Latest Tag:     $RegistryLatest"
Write-Host "===============================================" -ForegroundColor Cyan
Write-Host ""

# Verify image exists locally
try {
    docker image inspect $LocalImage | Out-Null
    Write-Host "✓ Image found: $LocalImage" -ForegroundColor Green
}
catch {
    Write-Host "✗ Image $LocalImage not found. Building..." -ForegroundColor Yellow
    docker compose build
}

# Tag for registry
Write-Host "Tagging image..." -ForegroundColor Yellow
docker tag $LocalImage $RegistryImage
docker tag $LocalImage $RegistryLatest
Write-Host "✓ Tags created" -ForegroundColor Green

# Prompt for push confirmation
$confirm = Read-Host "Push to registry? (y/n)"
if ($confirm -eq 'y' -or $confirm -eq 'Y') {
    Write-Host "Logging in to registry..." -ForegroundColor Yellow
    docker login $Registry
    
    Write-Host "Pushing $RegistryImage..." -ForegroundColor Yellow
    docker push $RegistryImage
    
    Write-Host "Pushing $RegistryLatest..." -ForegroundColor Yellow
    docker push $RegistryLatest
    
    Write-Host "✓ Images pushed successfully" -ForegroundColor Green
}
else {
    Write-Host "⊘ Push cancelled" -ForegroundColor Yellow
}

# Generate deployment manifest
Write-Host ""
Write-Host "Generating deployment manifest..." -ForegroundColor Yellow

$deployManifest = @"
# WaselX Release: $Version
# Generated: $(Get-Date)
# Registry: $RegistryImage

services:
  waselx-app:
    image: $RegistryImage
    restart: unless-stopped
    ports:
      - "5000:5000"
    environment:
      FLASK_ENV: production
      PYTHONUNBUFFERED: 1
    env_file:
      - .env.prod
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
"@

$deployManifest | Out-File -FilePath "deploy.yml" -Encoding UTF8
Write-Host "✓ Deployment manifest saved to deploy.yml" -ForegroundColor Green

Write-Host ""
Write-Host "Release Summary:" -ForegroundColor Cyan
Write-Host "  - Image:  $RegistryImage"
Write-Host "  - Tag:    $Version"
Write-Host "  - Latest: $RegistryLatest"
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host "  1. Test in staging: docker compose -f deploy.yml up -d" -ForegroundColor White
Write-Host "  2. Verify: curl http://localhost:5000/health" -ForegroundColor White
Write-Host "  3. Deploy to production with your orchestrator" -ForegroundColor White
