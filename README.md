# WaselX - Delivery Network Optimization

WaselX is a Data Structures and Algorithms project that models delivery-network optimization for a last-mile logistics company. It includes graph algorithms, tree structures, linear data structures, sorting/searching benchmarks, a Flask API dashboard, and a self-contained Streamlit frontend.

## Project Structure

```text
WaselX/
|-- app.py                         # Flask backend API and dashboard
|-- streamlit_app.py               # Self-contained Streamlit frontend
|-- main.py                        # CLI demonstration entry point
|-- render.yaml                    # Render backend deployment blueprint
|-- data/                          # Network data and helpers
|-- task_a/                        # Graph algorithms
|-- task_b/                        # BST and AVL tree implementations
|-- task_c/                        # Linked lists, priority queue, stack
|-- task_d/                        # Sorting and searching algorithms
|-- task_e/                        # Network simulator
|-- static/                        # Flask dashboard CSS/JS
|-- templates/                     # Flask HTML templates
|-- utils/                         # Visualization helpers
|-- REPORT_TEMPLATE.md             # Academic report scaffold
`-- requirements.txt
```

## Requirements

- Python 3.10+
- pip

Install dependencies:

```bash
pip install -r requirements.txt
```

## Streamlit Cloud Deployment

Deploy `streamlit_app.py` as the app entrypoint.

The Streamlit app is self-contained and directly imports the project modules, so Streamlit Cloud does not need a separate Flask backend or `API_URL` secret.

## Render Backend Deployment

The Flask backend can be deployed as a separate Render Web Service.

Option A: Blueprint deployment

1. Push the repo to GitHub.
2. In Render, choose **New > Blueprint**.
3. Connect this repository and select `main`.
4. Render will read `render.yaml` and create the `waselx-api` web service.

Option B: Manual Web Service

Use these settings in Render:

```text
Service type: Web Service
Runtime: Python 3
Build command: pip install -r requirements.txt
Start command: gunicorn app:app
Health check path: /health
Instance type: Free
```

After deployment, verify the backend at:

```text
https://your-render-service.onrender.com/health
```

## Run Locally

Run the Streamlit frontend:

```bash
streamlit run streamlit_app.py
```

Frontend URL:

```text
http://localhost:8501
```

Optional Flask backend/API dashboard:

```bash
python app.py
```

Backend URL:

```text
http://localhost:5000
```

Run the CLI demonstration:

```bash
python main.py
```

## Core Features

- Network topology visualization with Plotly.
- Shortest path optimization by distance, time, or cost.
- Multi-criteria route comparison.
- Minimum spanning tree calculations using Kruskal and Prim.
- Sorting and searching benchmarks.
- Road-closure simulation.
- CLI, Flask, and Streamlit demonstration modes.

## Key Documents

- `REPORT_TEMPLATE.md` - long-form academic report scaffold.
- `QUICK_REFERENCE.md` - quick project reference.
- `WaselX_MAIB_Final_Project.docx` - assignment/project brief.

## Verification

```bash
python -m py_compile app.py streamlit_app.py main.py
```

Health checks when services are running:

```text
http://localhost:8501/healthz
http://localhost:5000/health
```
