# WaselX - Delivery Network Optimization

WaselX is a Data Structures and Algorithms project that models delivery-network optimization for a last-mile logistics company. It includes graph algorithms, tree structures, linear data structures, sorting/searching benchmarks, a Flask API dashboard, and a Streamlit frontend.

## Project Structure

```text
WaselX/
|-- app.py                         # Flask backend API and dashboard
|-- streamlit_app.py               # Streamlit frontend
|-- main.py                        # CLI demonstration entry point
|-- data/                          # Network data and helpers
|-- task_a/                        # Graph algorithms
|-- task_b/                        # BST and AVL tree implementations
|-- task_c/                        # Linked lists, priority queue, stack
|-- task_d/                        # Sorting and searching algorithms
|-- task_e/                        # Network simulator
|-- static/                        # Flask dashboard CSS/JS
|-- templates/                     # Flask HTML templates
|-- utils/                         # Visualization helpers
|-- TECHNICAL_REQUIREMENTS_REPORT.md
|-- TRD.md
`-- requirements.txt
```

## Requirements

- Python 3.10+
- pip

Install dependencies:

```bash
pip install -r requirements.txt
```

## Run Locally

Start the Flask backend:

```bash
python app.py
```

Backend URL:

```text
http://localhost:5000
```

Start the Streamlit frontend in another terminal:

```bash
streamlit run streamlit_app.py
```

Frontend URL:

```text
http://localhost:8501
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
- Academic technical requirements report for final evaluation.

## Key Documents

- `TECHNICAL_REQUIREMENTS_REPORT.md` - overall final technical requirements report.
- `TRD.md` - detailed technical requirements document.
- `REPORT_TEMPLATE.md` - long-form academic report template.
- `TASK_B_TREES.md`, `TASK_C_QUEUES.md`, `TASK_D_SORTING_SEARCHING.md`, `TASK_E_MANAGEMENT_LEADERSHIP.md` - task-area documentation.

## Verification

```bash
python -m py_compile app.py streamlit_app.py main.py
```

Health checks:

```text
http://localhost:5000/health
http://localhost:8501/healthz
```
