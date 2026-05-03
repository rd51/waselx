# WaselX Technical Requirements Report

## 1. Document Control

| Field | Value |
| --- | --- |
| Project | WaselX Delivery Network Optimization |
| Document | Overall Technical Requirements Report |
| Version | 1.0 |
| Date | May 3, 2026 |
| Program | Data Structures and Algorithms Group Final Project |
| Repository | https://github.com/rd51/waselx |
| Status | Final draft for submission |

## 2. Executive Summary

WaselX is a Python-based delivery network optimization prototype for demonstrating data structures and algorithms in a realistic logistics setting. The system models a delivery network with hubs, distribution points, weighted routes, and route disruptions. It provides both a Flask API/dashboard and a Streamlit frontend for interactive demonstrations of shortest paths, minimum spanning trees, sorting/searching benchmarks, and road-closure simulation.

The project is designed for local academic evaluation. Core algorithm logic is implemented inside task-specific modules, while the web layers expose those algorithms through user-facing visualizations and API endpoints. The final submission should prioritize correctness, repeatable local execution, clear documentation, and a small repository footprint.

## 3. Business Problem

WaselX represents a last-mile delivery company that needs better decision support for route planning, dispatch prioritization, order lookup, and network resilience. The main operational problems are:

- Route inefficiency from manual or heuristic route selection.
- Slow dispatch decisions when urgent orders are handled without priority.
- Inefficient order lookup when customer-service records are searched linearly.
- Limited visibility into how road closures affect the delivery network.

The project demonstrates how graph algorithms, trees, queues, stacks, sorting, and searching can reduce these operational risks.

## 4. System Scope

### In Scope

- Python implementations of required DSA tasks.
- Static delivery network data with weighted edges.
- Flask backend API and dashboard.
- Streamlit frontend that calls the Flask backend.
- Plotly-based visualizations for network and benchmark results.
- Local execution through Python virtual environment.
- Optional Docker support for backend and frontend services.
- Technical documentation for project requirements and final evaluation.

### Out of Scope

- Real-time GPS tracking.
- Payment processing.
- Authentication and user management.
- Live order ingestion from external systems.
- Cloud production deployment as a mandatory requirement.
- Database persistence beyond static project data.

## 5. User Roles

| Role | Needs |
| --- | --- |
| Student demonstrator | Run the app locally, explain algorithms, show outputs. |
| Evaluator | Review code structure, verify algorithm behavior, inspect report evidence. |
| Technical reviewer | Check API behavior, frontend/backend integration, and project reproducibility. |
| Business stakeholder | Understand how DSA choices map to delivery operations. |

## 6. Architecture Requirements

The system must follow a simple layered architecture:

1. Data layer: static network definitions in `data/network.py`.
2. Algorithm layer: graph, tree, queue, list, stack, sorting, and searching implementations in `task_a` through `task_e`.
3. Service layer: Flask API in `app.py`.
4. Presentation layer: Flask template dashboard and Streamlit frontend in `streamlit_app.py`.
5. Visualization layer: Plotly and helper visualization utilities.

Required local ports:

| Service | File | Port | URL |
| --- | --- | --- | --- |
| Flask backend | `app.py` | 5000 | `http://localhost:5000` |
| Streamlit frontend | `streamlit_app.py` | 8501 | `http://localhost:8501` |

## 7. Functional Requirements

| ID | Requirement | Acceptance Criteria |
| --- | --- | --- |
| FR-01 | Load delivery network data | App loads 15 nodes and weighted routes without external services. |
| FR-02 | Display network topology | Frontend renders Plotly graph with hub and distribution nodes. |
| FR-03 | Compute shortest path | API accepts start, end, and weight type, then returns path and metrics. |
| FR-04 | Compare route criteria | API compares distance, time, and cost route choices. |
| FR-05 | Compute MST | API returns Kruskal and Prim results with total cost and sample connections. |
| FR-06 | Benchmark sorting | App compares Bubble, Merge, and Quick sort behavior. |
| FR-07 | Benchmark searching | App compares Linear Search and Binary Search comparison counts. |
| FR-08 | Simulate road closure | App allows a route to be blocked and reports updated simulator status. |
| FR-09 | Provide health checks | Flask `/health` and Streamlit `/healthz` must respond successfully. |
| FR-10 | Run locally | User can start backend and frontend from the repository root. |

## 8. Algorithm Requirements

| Area | Modules | Required Concepts |
| --- | --- | --- |
| Graph algorithms | `task_a` | Graph representation, Dijkstra, Floyd-Warshall, MST, BFS, DFS. |
| Trees | `task_b` | BST insertion/search/traversal and AVL balancing. |
| Linear structures | `task_c` | Linked list, circular list, priority queue, stack. |
| Sorting/searching | `task_d` | Bubble sort, merge sort, quick sort, linear search, binary search. |
| Simulator | `task_e` | Network state changes and operational resilience simulation. |

Core algorithm implementations must remain readable and demonstrable for academic review. Libraries may be used for presentation, HTTP services, and charts, but not as substitutes for the core DSA logic.

## 9. API Requirements

The Flask backend must expose:

| Endpoint | Method | Purpose |
| --- | --- | --- |
| `/health` | GET | Backend health check. |
| `/api/network` | GET | Network summary. |
| `/api/graph` | GET | Serialized Plotly network graph. |
| `/api/shortest-path` | POST | Single shortest-path calculation. |
| `/api/compare-paths` | POST | Distance, time, and cost comparison. |
| `/api/mst` | GET | MST results from Kruskal and Prim. |
| `/api/sorting-benchmark` | GET | Sorting benchmark graph. |
| `/api/search-benchmark` | GET | Search comparison data. |
| `/api/road-closure` | POST | Block or unblock route. |
| `/api/simulator-status` | GET | Current simulator state. |

All JSON responses must include either `status: success` with data or `status: error` with a clear message.

## 10. Frontend Requirements

The Streamlit frontend must:

- Read `API_URL` from Streamlit secrets, environment variable, or default to `http://localhost:5000`.
- Show backend connection status in the sidebar.
- Render Plotly JSON returned by Flask using `plotly.io.from_json`.
- Provide tabs or sections for Network, Path Finder, Algorithms, and Simulator.
- Display route metrics in business-friendly units: kilometers, minutes, and AED.
- Avoid placeholder visualization messages in final delivery.

The Flask dashboard must:

- Serve the main dashboard at `/`.
- Load Plotly locally through `/plotly.min.js` so local demos do not depend on CDN access.
- Render API-driven graphs in the browser.

## 11. Data Requirements

The project data must be deterministic and stored inside the repository:

- Node IDs and labels.
- Weighted route list.
- Adjacency-list builder.
- Visualization coordinates and colors.

No external database is required for final submission. Generated logs, virtual environments, caches, and local output artifacts should not be committed.

## 12. Nonfunctional Requirements

| Category | Requirement |
| --- | --- |
| Portability | Must run on Windows with PowerShell and Python virtual environment. |
| Reproducibility | Dependencies must be installable with `pip install -r requirements.txt`. |
| Maintainability | Code should remain organized by task area and avoid unrelated refactors. |
| Observability | Local health endpoints and logs should support quick verification. |
| Performance | Algorithm benchmarks should complete quickly for demonstration-size inputs. |
| Reliability | Frontend should show a clear error if Flask API is offline. |
| Security | Secrets and environment files must remain ignored by git. |

## 13. Local Deployment Requirements

Backend:

```powershell
.\.venv\Scripts\python.exe app.py
```

Frontend:

```powershell
$env:API_URL = "http://localhost:5000"
.\.venv\Scripts\python.exe -m streamlit run streamlit_app.py
```

Verification:

```powershell
Invoke-RestMethod http://localhost:5000/health
Invoke-WebRequest http://localhost:8501/healthz -UseBasicParsing
```

## 14. Repository Requirements

The final repository should keep:

- Source code needed to run the backend, frontend, CLI demo, and algorithms.
- Minimal configuration for local execution and optional Docker.
- One overall technical requirements report.
- One final project report if required by submission.
- Essential images/assets used by the report or dashboard.

The final repository should exclude:

- Virtual environments.
- Python cache folders.
- Runtime logs.
- Generated output folders.
- Planning artifacts that are not part of final submission.
- Duplicate deployment guides that are not required for academic evaluation.

## 15. Verification Checklist

| Check | Expected Result |
| --- | --- |
| `python -m py_compile app.py streamlit_app.py` | No syntax errors. |
| Flask `/health` | Returns `status: healthy`. |
| Flask `/api/graph` | Returns serialized Plotly graph JSON. |
| Flask `/plotly.min.js` | Returns local Plotly JavaScript bundle. |
| Streamlit `/healthz` | Returns HTTP 200. |
| Streamlit Network tab | Renders Plotly network graph. |
| Streamlit Path Finder | Renders highlighted path graph after user action. |
| Git status | Only intentional final files changed, added, or deleted. |

## 16. Risks and Mitigations

| Risk | Mitigation |
| --- | --- |
| Local file named `streamlit.py` shadows installed Streamlit package | Remove the root-level `streamlit.py`; use `streamlit_app.py` as the entrypoint. |
| CDN Plotly script fails offline | Serve Plotly locally through Flask. |
| Ignored `.env` files are missing in another clone | Document local defaults and keep secrets out of git. |
| Excessive generated documentation clutters final submission | Keep a focused report set and delete planning/demo-only artifacts after approval. |
| Windows console encoding breaks Flask startup output | Use ASCII-safe startup messages. |

## 17. Final Deliverables

Recommended final deliverables:

- `app.py`
- `streamlit_app.py`
- `main.py`
- `requirements.txt`
- `data/`
- `task_a/` through `task_e/`
- `utils/`
- `static/`
- `templates/`
- `.streamlit/config.toml`
- `.streamlit/secrets.toml.example`
- `README.md`
- `TECHNICAL_REQUIREMENTS_REPORT.md`
- Final academic report file, if separately required
- Optional deployment files only if Docker deployment is part of submission

