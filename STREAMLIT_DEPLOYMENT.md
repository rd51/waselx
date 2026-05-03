# Streamlit Deployment Guide

## Overview
The WaselX project now includes a Streamlit frontend (`streamlit_app.py`) that calls the existing Flask API backend. This enables rapid deployment of the interactive dashboard to the web.

## Files
- **`streamlit_app.py`** — Streamlit application (4 tabs: Network, Path Finder, Algorithms, Simulator)
- **`requirements.txt`** — Unified project dependencies
- **`Dockerfile.streamlit`** — Docker image for containerized Streamlit deployment
- **`.streamlit/config.toml`** — Streamlit configuration (theme, server settings)
- **`.streamlit/secrets.toml.example`** — API URL configuration template

## Deployment Options

### Option 1: Streamlit Cloud (Fastest, Free Tier)

**Prerequisites:**
- GitHub account with this repo pushed (`rd51/waselx`)
- Flask backend running and publicly accessible

**Steps:**
1. Go to [streamlit.io/cloud](https://streamlit.io/cloud)
2. Click "New app"
3. Select your GitHub repo (`rd51/waselx`)
4. Branch: `main`
5. Main file path: `streamlit_app.py`
6. Deploy!

**Configuration:**
- In the Streamlit Cloud dashboard, set Secrets:
  ```
  API_URL = "https://your-flask-api-url.com"
  ```

**Pros:** Free tier available, automatic deployments on git push, custom domain support  
**Cons:** Requires public Flask backend, limited compute resources on free tier

---

### Option 2: Docker Deployment (Production)

**Build the image:**
```bash
cd 'd:\Downloads\S.P. Jain\DSA\Group Final Project'
docker build -f Dockerfile.streamlit -t waselx-streamlit:latest .
```

**Run locally:**
```bash
docker run -p 8501:8501 \
  -e API_URL="http://host.docker.internal:5000" \
  waselx-streamlit:latest
```
Then visit: http://localhost:8501

**Deploy to cloud (e.g., AWS, GCP, DigitalOcean):**
1. Push image to Docker Hub / ECR / artifact registry
2. Use `docker-compose` with both Flask and Streamlit services:

```yaml
# docker-compose.all.yml
version: '3.8'
services:
  # Flask API backend
  flask-api:
    image: waselx:latest
    ports:
      - "5000:5000"
    environment:
      - FLASK_ENV=production
    volumes:
      - ./data:/app/data
  
  # Streamlit frontend
  streamlit-ui:
    image: waselx-streamlit:latest
    ports:
      - "8501:8501"
    environment:
      - API_URL=http://flask-api:5000
    depends_on:
      - flask-api
```

Run:
```bash
docker compose -f docker-compose.all.yml up -d
```

**Pros:** Full control, scales easily, supports HTTPS/TLS, custom domains  
**Cons:** Requires infrastructure setup

---

### Option 3: Local Development

**Install dependencies:**
```bash
pip install -r requirements.txt
```

**Start Flask API in one terminal:**
```bash
python app.py
```

**Start Streamlit in another terminal:**
```bash
streamlit run streamlit_app.py
```

Visit: http://localhost:8501

---

## Configuration

### API URL
Set the Flask API URL via Streamlit secrets:

**Local:**
```bash
# .streamlit/secrets.toml
API_URL = "http://localhost:5000"
```

**Production:**
```bash
# Streamlit Cloud dashboard → Settings → Secrets
API_URL = "https://api.yourdomain.com"
```

---

## Architecture

```
┌─────────────────────────┐
│   Streamlit Frontend    │ (Port 8501)
│   (streamlit_app.py)    │
│                         │
│ - Network Topology      │
│ - Path Finder           │
│ - Algorithms Benchmark  │
│ - Road Closure Sim      │
└────────────┬────────────┘
             │ HTTP Calls
             ↓
┌─────────────────────────┐
│  Flask API Backend      │ (Port 5000)
│   (app.py)              │
│                         │
│ - /api/shortest-path    │
│ - /api/simulator-status │
│ - /api/mst              │
│ - /api/sorting-bench    │
│ - /api/search-bench     │
└─────────────────────────┘
```

---

## Features

### 🌐 Network Tab
- Real-time network topology visualization
- Node and edge statistics
- Network connectivity status

### 🔍 Path Finder Tab
- Select start and end nodes
- Choose optimization criteria (distance, time, cost)
- Compare all three optimization paths side-by-side
- Visualize optimal routes on network graph

### 📊 Algorithms Tab
- **Sorting:** Bubble, Merge, Quick sort performance comparison
- **MST:** Kruskal's vs Prim's results
- **Searching:** Linear vs Binary search benchmarks

### 🚗 Simulator Tab
- Block/unblock individual routes
- Track active and blocked routes in real-time
- Verify network remains operational despite failures
- Test resilience and alternate routing

---

## Troubleshooting

### "API Offline" Error
- Ensure Flask backend is running: `python app.py`
- Verify API URL in Streamlit secrets matches Flask endpoint
- Check firewall/network connectivity

### Slow performance
- Increase venv memory allocation
- Cache API responses (see `@st.cache_data` in streamlit_app.py)
- Deploy frontend and backend in same Docker network

### Data not updating
- Clear Streamlit cache: `streamlit cache clear`
- Restart Streamlit: `Ctrl+C` and re-run

---

## Next Steps

1. **Immediate:**
   ```bash
   docker build -f Dockerfile.streamlit -t waselx-streamlit:latest .
   docker run -p 8501:8501 waselx-streamlit:latest
   ```

2. **For Streamlit Cloud:**
   - Push to GitHub
   - Sign in at streamlit.io/cloud
   - Select repo and main file

3. **For Production:**
   - Set up HTTPS/TLS with nginx
   - Deploy both services together (docker-compose)
   - Set custom domain and API endpoint

---

**Deployment Status:** ✅ Ready for deployment  
**Last Updated:** 2025-05-03
