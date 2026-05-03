# 🐳 Docker Deployment Guide - WaselX

## Quick Start

### Prerequisites
- Docker Desktop installed and running
- Port 5000 available on your machine
- 2GB+ RAM allocated to Docker

### Deploy in 2 Commands

```bash
# Navigate to project directory
cd "d:\Downloads\S.P. Jain\DSA\Group Final Project"

# Start the application (builds and runs)
docker-compose up -d
```

**That's it!** Your dashboard will be available at: **http://localhost:5000**

---

## 🎯 What Gets Deployed

### Docker Services
- **waselx-app**: Flask web server running on port 5000

### Components Included
```
✅ WaselX Network (15 nodes, 24 edges)
✅ Dijkstra's Algorithm (live shortest paths)
✅ Floyd-Warshall (all-pairs shortest paths)
✅ MST Algorithms (Kruskal's + Prim's)
✅ Sorting Benchmarks (Bubble, Merge, Quick)
✅ Search Comparison (Linear vs Binary)
✅ Network Visualization (Plotly interactive)
✅ Road Closure Simulator
✅ Real-time metrics dashboard
```

---

## 📊 Dashboard Features

### 1. Network Topology
- Interactive graph showing all 15 nodes
- Blue = Hubs, Orange = Distribution centers
- Clickable nodes and edges
- Geographic layout (Dubai, Sharjah, Abu Dhabi)

### 2. Path Finder
- Find shortest paths between any two nodes
- Three optimization criteria:
  - **Distance**: Shortest km
  - **Time**: Fastest minutes
  - **Cost**: Lowest AED
- Compare all criteria side-by-side
- Visual path highlighting

### 3. Algorithm Analysis
- **Sorting Benchmark**: Performance graph for 3 algorithms
- **Search Comparison**: Linear vs Binary search
- **MST Algorithms**: Kruskal's vs Prim's comparison
- All with real data and metrics

### 4. Network Simulator
- Block roads to simulate closures
- Watch network adapt to disruptions
- Real-time statistics
- Clear all blocks button

---

## 🚀 Advanced Usage

### View Logs
```bash
# Watch real-time logs
docker-compose logs -f waselx-app

# View last 100 lines
docker-compose logs --tail=100 waselx-app
```

### Stop the Server
```bash
docker-compose down
```

### Rebuild the Image
```bash
docker-compose build --no-cache
docker-compose up -d
```

### Access Container Shell
```bash
docker exec -it waselx-simulator bash
```

### View Running Containers
```bash
docker ps
docker stats
```

### Remove Everything
```bash
docker-compose down -v
```

---

## 📈 Performance Metrics

### System Requirements
- **CPU**: 1+ cores
- **Memory**: 512MB minimum (1GB recommended)
- **Disk**: 500MB for image
- **Network**: Port 5000 (TCP)

### Response Times (Expected)
- Network load: < 100ms
- Path calculation: < 50ms
- Graph rendering: < 200ms
- Benchmark: < 500ms

---

## 🔧 Configuration

### Environment Variables
Set in `docker-compose.yml`:

```yaml
FLASK_ENV: production    # Use 'development' for debug mode
PYTHONUNBUFFERED: 1      # Show logs in real-time
```

### Data Persistence
```yaml
volumes:
  - ./data:/app/data          # Network data
  - ./outputs:/app/outputs    # Generated graphs
```

---

## 🎓 API Endpoints (For Integration)

### Health Check
```
GET /health
→ Returns: {status: 'healthy', timestamp: '...'}
```

### Network Overview
```
GET /api/network
→ Returns: nodes, hubs, edges, connectivity status
```

### Shortest Path
```
POST /api/shortest-path
Body: {start: 'H1', end: 'D8', weight: 'distance'}
→ Returns: path, distance, time, cost, graph
```

### Compare Paths
```
POST /api/compare-paths
Body: {start: 'H1', end: 'D8'}
→ Returns: 3 paths (distance/time/cost optimized), graph
```

### MST
```
GET /api/mst
→ Returns: Kruskal's and Prim's algorithms comparison
```

### Sorting Benchmark
```
GET /api/sorting-benchmark
→ Returns: Plotly graph with 3 sorting algorithms
```

### Search Benchmark
```
GET /api/search-benchmark
→ Returns: Linear vs Binary search comparison
```

### Road Closure
```
POST /api/road-closure
Body: {from: 'H1', to: 'H2', action: 'block'}
→ Returns: blocked edge count, confirmation message
```

### Simulator Status
```
GET /api/simulator-status
→ Returns: network stats, blocked edges, version
```

---

## 🐛 Troubleshooting

### Port 5000 Already in Use
```bash
# Find process using port 5000
netstat -ano | findstr :5000

# Kill process (Windows)
taskkill /PID <PID> /F

# Or use different port in docker-compose.yml
ports:
  - "5001:5000"  # Then access at :5001
```

### Container Won't Start
```bash
# Check logs
docker-compose logs waselx-app

# Rebuild from scratch
docker-compose build --no-cache
docker-compose up -d
```

### Memory Issues
```bash
# Check container stats
docker stats waselx-simulator

# Increase Docker memory limit in Docker Desktop settings
# Then restart: docker-compose restart
```

### Graph Not Loading
```bash
# Clear browser cache (Ctrl+Shift+Del)
# Hard refresh (Ctrl+Shift+R)
# Check network tab for errors
```

---

## 📋 File Structure (in Container)

```
/app/
├── app.py                    # Flask application
├── requirements-docker.txt   # Dependencies
├── data/
│   ├── network.py           # Network constants
│   └── __init__.py
├── task_a/                  # Graph algorithms
├── task_b/                  # Trees
├── task_c/                  # Linear structures
├── task_d/                  # Sorting & searching
├── task_e/                  # Simulator
├── utils/                   # Visualization
├── templates/               # HTML templates
│   └── index.html
├── static/                  # CSS & JS
│   ├── style.css
│   └── dashboard.js
└── outputs/                 # Generated files
```

---

## 🔐 Security Notes

### Production Deployment
For production use:

1. **Set DEBUG=False** in app.py
2. **Use HTTPS** with reverse proxy (nginx)
3. **Add authentication** for sensitive endpoints
4. **Rate limiting** on API endpoints
5. **CORS restrictions** (currently allowing all)

### Example Production Setup
```bash
# Use gunicorn instead of Flask dev server
docker run -p 5000:5000 -e FLASK_ENV=production \
  -c "gunicorn -w 4 -b 0.0.0.0:5000 app:app" \
  waselx:latest
```

---

## 📊 Monitoring & Maintenance

### Check Health
```bash
curl http://localhost:5000/health
```

### View Metrics
```bash
# Real-time stats
docker stats waselx-simulator

# Container info
docker inspect waselx-simulator
```

### Backup Data
```bash
# Backup volumes
docker run --rm -v waselx_app-data:/data -v $(pwd):/backup \
  alpine tar czf /backup/data.tar.gz -C /data .
```

### Update Code
```bash
# Pull latest changes
git pull

# Rebuild and redeploy
docker-compose build --no-cache
docker-compose up -d
```

---

## 🚀 Performance Tips

1. **Keep browser tab active** - Flask might pause if tab is inactive
2. **Use Chrome/Edge** - Best Plotly performance
3. **Clear cache periodically** - localStorage in browser
4. **Monitor Docker memory** - Especially on small systems
5. **Close unused tabs** - Browser tabs consume Docker memory

---

## 📞 Support & Issues

### Common Issues Checklist
- ✅ Docker Desktop running?
- ✅ Port 5000 available?
- ✅ Sufficient disk space (500MB+)?
- ✅ Network connectivity OK?
- ✅ Latest Docker version?

### Check System
```bash
# Docker version
docker --version
docker-compose --version

# Available disk space
df -h

# Memory available
docker stats --no-stream
```

---

## 🎯 Next Steps

1. ✅ Open http://localhost:5000 in browser
2. ✅ Explore Network Topology tab
3. ✅ Try Path Finder (H1 → D8)
4. ✅ Compare sorting algorithms
5. ✅ Simulate road closures

**Dashboard should load within 5 seconds!**

---

## 📝 Container Lifecycle

```
Start:        docker-compose up -d
Monitor:      docker-compose logs -f
Stop:         docker-compose stop
Resume:       docker-compose up -d
Rebuild:      docker-compose build --no-cache
Full restart: docker-compose down && docker-compose up -d
Clean:        docker-compose down -v
```

---

**✨ Your WaselX dashboard is now ready to deploy!**

For any issues, check:
- Docker logs: `docker-compose logs -f`
- Browser console: F12
- Network tab: F12 → Network

Happy optimizing! 🚀
