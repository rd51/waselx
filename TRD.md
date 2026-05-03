# Technical Requirements Document (TRD)
## WaselX Express — UAE Delivery Optimization

---

## 1. Document Header

| Field | Value |
|-------|-------|
| **Project Name** | WaselX Express — UAE Delivery Optimization |
| **Document Type** | Technical Requirements Document (TRD) |
| **Version** | 1.0 |
| **Program** | MAIB — Data Structures & Algorithms Final Project |
| **Institution** | S.P. Jain School of Global Management |
| **Team Size** | 3–4 members |
| **Team Members** | [PLACEHOLDER: To be filled by team] |
| **Date Created** | May 3, 2025 |
| **Last Updated** | May 3, 2025 |
| **Status** | Draft |
| **Repository** | https://github.com/rd51/waselx |

---

## 2. Project Overview

### 2.1 Business Context
WaselX Express is a last-mile delivery company operating across the UAE, providing same-day and next-day courier services to enterprise customers and e-commerce platforms. The company operates a network of **15 distribution nodes** (7 hub facilities and 8 delivery zones) across major metropolitan areas including Dubai, Abu Dhabi, and surrounding emirates. Current operational scale: **3,500 orders processed daily** with a fleet of **200 active riders**. The business faces critical operational challenges in route planning, order dispatch efficiency, and customer lookup, all of which directly impact delivery SLA compliance, rider utilization, and customer satisfaction.

### 2.2 Core Operational Problems Addressed

1. **Route Inefficiency (30% wasted kilometers)**
   - Current dispatch system uses heuristic routing; no systematic shortest-path optimization
   - Multi-stop routes often lack optimized sequencing, resulting in backtracking and unnecessary travel time
   - Impact: 5–10% of orders miss delivery windows; 15% of rider time spent on inefficient navigation
   - **DSA Solution:** Dijkstra's algorithm (Q2) for single-destination optimization; Floyd-Warshall (Q3) for all-pairs connectivity analysis; Minimum Spanning Trees (Q4) for network backbone planning

2. **Slow Order Dispatch (2–5 minute queue wait)**
   - Legacy dispatch system iterates through all active riders sequentially; no priority-based assignment
   - Urgent orders (high-priority/high-value) treated same as standard orders
   - Impact: Premium SLA orders miss delivery slots; rider idle time increases during peak hours
   - **DSA Solution:** Priority Queue (Q14) for order intake; Stack (Q15) for order status tracking; Heap-based min-heap for O(log n) assignment

3. **Poor Order Lookup (O(n) linear search)**
   - Customer service team manually searches order database (sequential scan)
   - Lookup for a specific order ID takes 2–10 seconds depending on database size
   - Impact: Increased support queue time; customer wait times during tracking inquiries
   - **DSA Solution:** Binary Search (Q19) on sorted order ID array for O(log n) lookup; AVL Tree (Q9) for balanced range queries

### 2.3 Project Scope
- **Prototype Status:** Python-based algorithmic prototype, not a production deployment
- **Target Environment:** Local development and academic evaluation
- **Not In Scope:** Cloud infrastructure, distributed systems, real-time GPS integration, payment processing, mobile apps
- **Deliverables:** Single-entry-point CLI application (`main.py`), 27 implemented algorithms with numerical traces, matplotlib visualizations, technical report with hand-worked solutions, README with setup and execution instructions

---

## 3. Technical Standards (Mandatory)

### 3.1 Language Requirement

| Aspect | Requirement |
|--------|-------------|
| **Python Version** | 3.10 or later (minimum) |
| **Rationale** | Python 3.10+ provides match statement (structural pattern matching), improved type hints with `typing.TypedDict`, and performance optimizations in core data structure operations; matches academic curriculum standards |
| **Compliance Rule** | All `.py` files must include `# Python 3.10+` comment at the top of the file. Any syntax or features used must be valid in Python 3.10. Team must verify with `python --version` before final submission. |
| **Verification Command** | `python --version && grep -r "Python 3.10+" *.py` |

### 3.2 Algorithm Implementation Policy

#### 3.2.1 Core Requirement
**All core algorithms must be implemented from scratch.** No library function substitution for the core algorithmic logic.

#### 3.2.2 Standard Library Scope — ALLOWED ONLY FOR
- **heapq:** Permitted ONLY in comparison benchmarks (Q22) labeled as `# [BENCHMARK ONLY — not primary implementation]`. NOT permitted as the underlying PriorityQueue in Q14.
- **collections.deque:** Permitted for queue/stack backing only in utility operations. NOT as the main algorithm data structure unless explicitly teaching deque behavior.
- **time, random, math:** Permitted for performance measurement, synthetic data generation, and mathematical utilities (e.g., `math.sqrt`). NOT for core algorithm computation.

#### 3.2.3 NetworkX Scope — ALLOWED ONLY FOR
- **Graph Visualization:** Drawing nodes and edges on a 2D plot in `utils/visualizer.py`
- **NOT Permitted:** NetworkX algorithm functions:
  - ❌ `nx.dijkstra_path(G, source, target)` as Dijkstra output
  - ❌ `nx.all_pairs_shortest_path_length(G)` as Floyd-Warshall output
  - ❌ `nx.minimum_spanning_tree(G, algorithm='kruskal')` as MST output
  - ❌ `nx.bfs_tree(G, source)` or `nx.dfs_tree(G, source)` as BFS/DFS output

#### 3.2.4 Violation Examples (PROHIBITED)
```python
# ❌ WRONG: Using heapq as primary PriorityQueue
from heapq import heappush, heappop
class PriorityQueue:
    def __init__(self):
        self.heap = []
    def insert(self, order_id, priority):
        heappush(self.heap, (priority, order_id))  # This is fine for learning, but
    def extract_min(self):
        return heappop(self.heap)[1]
# Problem: heappop is the library implementation; you're not learning the heap algorithm

# ❌ WRONG: Using NetworkX for algorithm
import networkx as nx
shortest_path = nx.dijkstra_path(G, "H1", "D1")  # This is not implementing Dijkstra

# ❌ WRONG: Using heapq in core algorithm without labeling
def dijkstra(graph, start):
    dist = {}
    heap = [(0, start)]
    while heap:
        d, node = heapq.heappop(heap)  # Unlabeled use; violates standard
```

#### 3.2.5 Compliant Examples (PERMITTED)
```python
# ✅ CORRECT: Manual heap implementation
class MinHeap:
    def __init__(self):
        self.heap = []
    
    def _bubble_up(self, idx):
        while idx > 0 and self.heap[idx] < self.heap[(idx - 1) // 2]:
            self.heap[idx], self.heap[(idx - 1) // 2] = self.heap[(idx - 1) // 2], self.heap[idx]
            idx = (idx - 1) // 2
    
    def insert(self, val):
        self.heap.append(val)
        self._bubble_up(len(self.heap) - 1)
    
    def extract_min(self):
        # ... manual deletion and heap repair

# ✅ CORRECT: Labeled benchmark use
# [BENCHMARK ONLY — not primary implementation]
import heapq
heap_time = measure_time(lambda: run_heapq_dijkstra(...))

# ✅ CORRECT: NetworkX for visualization only
import matplotlib.pyplot as plt
import networkx as nx
pos = nx.spring_layout(G)  # Layout algorithm (acceptable)
nx.draw(G, pos, ...)  # Drawing (acceptable)
```

#### 3.2.6 Enforcement
- **Code Review:** Every algorithm function must be reviewed to confirm no library substitution
- **Inline Comments:** Place `# Manual implementation of [algorithm name]` at function definition
- **Test Case:** Each algorithm file must include a `test_[algorithm_name]()` function with manual trace

---

### 3.3 Visualization Standard

| Requirement | Specification |
|-------------|---------------|
| **Primary Tool** | matplotlib (mandatory for Q6, Q22, Q27) |
| **Version** | Latest stable; specify as `matplotlib>=3.7` in `requirements.txt` |
| **Optional Supplement** | NetworkX (graph layout only; see section 3.2.3) |
| **Output Format** | `.png` files saved to `outputs/` directory |
| **Metadata** | All figures must include: title, axis labels (where applicable), legend (where applicable), caption with question number |
| **Resolution** | Minimum 150 DPI; save with `plt.savefig("filename.png", dpi=150, bbox_inches="tight")` |

#### 3.3.1 Sample Figure Requirements
- **Q6 Path Simulator:** Network graph with highlighted path overlay, legend showing start/end nodes, distance metric displayed
- **Q22 Sort Benchmark:** Line plot with array size on x-axis, comparison count on y-axis; separate series for Bubble, Merge, Quick sort
- **Q27 Comprehensive Simulator:** Network state before and after blockage, with blocked edges highlighted in red; active/blocked route counts in text box

---

### 3.4 Hand-Traced Numerical Solutions

| Requirement | Detail |
|-------------|--------|
| **Scope** | ALL numerical questions: Q1, Q2, Q3, Q4, Q7, Q8, Q9, Q12, Q13, Q14, Q15, Q18, Q19, Q20 |
| **Format** | Tables for algorithm traces (Dijkstra steps, Floyd-Warshall matrices, BST insertion); diagrams for tree structures |
| **Minimum Content** | Step-by-step intermediate values, not final answer alone |
| **Penalty** | Final answer without working = 0 marks for that section |
| **Report Inclusion** | LaTeX-style tables in Word document, or hand-drawn diagrams (photographed, legible) |
| **Example:** Dijkstra(H1 → D1) | Step 1: dist[H1]=0, unvisited={all}; Step 2: visit H1, update neighbors; Step 3: select min dist unvisited node; ... final: dist[D1]=8 km |

#### 3.4.1 Required Hand-Traces by Question
- **Q1:** Node count, edge count, adjacency list (first 3 nodes)
- **Q2:** Dijkstra steps from H1 to D1 (5–7 iterations)
- **Q3:** Floyd-Warshall matrix snapshot after k=2 iterations; identify best hub
- **Q4:** Kruskal's edge selection order (first 5 edges); Prim's tree growth (first 4 nodes)
- **Q7:** BFS and DFS traversal order from H1
- **Q8:** BST insertion sequence; final tree structure diagram
- **Q9:** AVL tree after rotations; count of rotations performed
- **Q12–15:** Data structure operations (insertion, extraction, push/pop) with state snapshots
- **Q18:** Sorting trace for 5-element array; comparison count at each step
- **Q19:** Binary search trace on sorted array; target found at step N
- **Q20:** Divide-and-conquer recursion tree; subproblem sizes and base case hits

---

### 3.5 README.md Requirement

The file `README.md` must include the following sections in order:

```markdown
# WaselX Express — Delivery Optimization (README)

## 1. Project Overview
[One paragraph: business context, problem statement, scope]

## 2. Prerequisites
[System requirements: Python 3.10+, OS compatibility, optional tools]

## 3. Installation
[Step-by-step setup: clone repo, create venv, install dependencies]
```bash
python -m venv venv
source venv/bin/activate  # or: venv\Scripts\activate (Windows)
pip install -r requirements.txt
```

## 4. How to Run Each Task
[Instructions for main.py menu; list all 27 questions and their corresponding menu options]
```bash
python main.py
# Select task A (Graph & Paths): option 1
# [etc.]
```

## 5. Sample Output
[Terminal output screenshots or copy-paste from successful runs]

## 6. File Structure
[Tree diagram of project folders]

## 7. Academic Integrity Statement
[See section 3.6 below]

## 8. References
[Textbooks, documentation, tutorials cited]
```

---

### 3.6 Academic Integrity

#### 3.6.1 Code Authorship
- **Core Requirement:** All code written by team members
- **Exceptions:** Standard library imports (Python built-in) and external packages (installed via pip) are permitted without attribution
- **No Exceptions:** Copying open-source algorithm implementations, using Stack Overflow solutions without modification, using ChatGPT-generated code without review

#### 3.6.2 AI-Assisted Code Marking
Every line of code generated with AI assistance (including Copilot, ChatGPT, Claude, etc.) must be marked with an inline comment block:

```python
# [AI-ASSISTED: tool=GitHub Copilot, purpose=generated docstring template, reviewed by=Alice on 2025-05-01]
def dijkstra(graph, start):
    """Dijkstra's algorithm implementation."""
    # Rest of manually verified implementation
    pass
```

**Fields Required:**
- `tool`: Name of AI tool used
- `purpose`: What the AI generated (e.g., "generated initial skeleton", "docstring only")
- `reviewed by`: Team member name and date of manual review

#### 3.6.3 Benchmark vs. Core Implementation Labeling
Any use of standard library for **performance comparison benchmarks** (not primary algorithm logic) must be labeled:

```python
# [BENCHMARK ONLY — not primary implementation]
import heapq
def benchmark_heapq_dijkstra(graph, start):
    """For comparison only; not the submitted Dijkstra implementation."""
    # heapq usage here
    pass
```

#### 3.6.4 External Citations
All external references must be cited:
- **Textbooks:** Author, Title, Edition, Page Number (e.g., "Cormen et al., Introduction to Algorithms, 3rd ed., Chapter 9")
- **Documentation:** Tool name, URL, access date
- **Tutorials:** Author/Source, Tutorial Title, URL, access date
- **Location:** Include citations in `references.txt` file and inline code comments where applicable

#### 3.6.5 Academic Integrity Statement (for README.md)
```
## Academic Integrity

This project is submitted as part of the MAIB Data Structures & Algorithms course.
All algorithms are implemented by the team members listed above.
Standard library usage is noted in code comments.
AI-assisted code is marked with [AI-ASSISTED: ...] tags and has been reviewed.
All external references are cited in the References section.

By submitting this work, we affirm that it is our own and meets the institutional
academic integrity policy. We assume full responsibility for any violations.
```

---

## 4. File Structure Requirements

### 4.1 Mandatory Directory Layout

```
waselx_project/
├── data/
│   ├── __init__.py
│   └── network.py              # Q1: 15 nodes, 24 edges (single source of truth)
│
├── task_a/
│   ├── __init__.py
│   ├── graph.py                # Q1: Adjacency list + matrix representation
│   ├── dijkstra.py             # Q2: Dijkstra's single-source shortest path
│   ├── floyd_warshall.py       # Q3: Floyd-Warshall all-pairs shortest path
│   ├── mst.py                  # Q4: Kruskal's + Prim's MST algorithms
│   ├── traversals.py           # Q7: BFS + DFS graph traversals
│   └── path_simulator_basic.py # Q6: Basic path simulation with rider assignment
│
├── task_b/
│   ├── __init__.py
│   ├── bst.py                  # Q8: Binary Search Tree (insertion, traversal, height)
│   └── avl.py                  # Q9: AVL Tree (balancing, rotations, height comparison)
│
├── task_c/
│   ├── __init__.py
│   ├── linked_list.py          # Q12: Doubly Linked List (insertion, deletion, traversal)
│   ├── circular_list.py        # Q13: Circular Linked List (rider round-robin)
│   ├── priority_queue.py       # Q14: Min-Heap Priority Queue (order intake)
│   └── stack.py                # Q15: Stack (order status, LIFO, push/pop)
│
├── task_d/
│   ├── __init__.py
│   ├── sorting.py              # Q18: Merge Sort + Quick Sort (comparison count)
│   ├── searching.py            # Q19 + Q20: Binary Search + Divide-and-Conquer
│   └── sort_benchmark.py       # Q22: Performance simulation (5 dataset sizes)
│
├── task_e/
│   ├── __init__.py
│   └── simulator.py            # Q27: Comprehensive network simulator
│
├── utils/
│   ├── __init__.py
│   └── visualizer.py           # Shared matplotlib drawing utility (network, trees, etc.)
│
├── outputs/                    # All saved .png figures (generated by running tasks)
│   └── (empty initially; populated by matplotlib.savefig calls)
│
├── main.py                     # Single entry point with menu-driven task selector
├── requirements.txt            # Dependencies (matplotlib>=3.7 mandatory)
├── TRD.md                      # This Technical Requirements Document
├── README.md                   # Setup and run instructions
├── references.txt              # Academic citations
└── .gitignore                  # Exclude outputs/, __pycache__, .venv
```

### 4.2 File Purpose Summary

| File | Purpose | Question(s) | Status |
|------|---------|------------|--------|
| `data/network.py` | 15 nodes, 24 edges, weights | Q1–Q27 (all) | — |
| `task_a/graph.py` | Adjacency list/matrix construction | Q1 | — |
| `task_a/dijkstra.py` | Single-source shortest path | Q2 | — |
| `task_a/floyd_warshall.py` | All-pairs shortest path | Q3 | — |
| `task_a/mst.py` | Kruskal's and Prim's algorithms | Q4 | — |
| `task_a/traversals.py` | BFS and DFS | Q7 | — |
| `task_a/path_simulator_basic.py` | Rider assignment, path checking | Q6 | — |
| `task_b/bst.py` | Binary Search Tree | Q8 | — |
| `task_b/avl.py` | AVL Tree with rotations | Q9 | — |
| `task_c/linked_list.py` | Doubly Linked List | Q12 | — |
| `task_c/circular_list.py` | Circular Linked List (round-robin) | Q13 | — |
| `task_c/priority_queue.py` | Min-Heap Priority Queue | Q14 | — |
| `task_c/stack.py` | Stack (LIFO) | Q15 | — |
| `task_d/sorting.py` | Merge Sort + Quick Sort | Q18 | — |
| `task_d/searching.py` | Binary Search + Divide-and-Conquer | Q19, Q20 | — |
| `task_d/sort_benchmark.py` | Performance comparison on 5 sizes | Q22 | — |
| `task_e/simulator.py` | Multi-criteria network simulator | Q27 | — |
| `utils/visualizer.py` | matplotlib wrapper (draw network, trees) | Q6, Q22, Q27 | — |
| `main.py` | CLI menu, task orchestration | All | — |

---

## 5. Data Requirements

### 5.1 Network Data (Single Source of Truth)

**File:** `data/network.py`

**Specification:**
```python
# Python 3.10+

# 15 nodes: 7 hubs (H1–H7) + 8 delivery zones (D1–D8)
NODES = ["H1", "H2", "H3", "H4", "H5", "H6", "H7", 
         "D1", "D2", "D3", "D4", "D5", "D6", "D7", "D8"]

NODE_LABELS = {
    "H1": "Dubai Marina Hub",
    "H2": "Business Bay Hub",
    # ... (full mapping)
}

# 24 bidirectional edges: (from, to, distance_km, time_min, cost_aed)
EDGES = [
    ("H1", "H2", 3.5, 8, 2.0),
    ("H1", "D3", 8.0, 15, 5.5),
    # ... (all 24 edges)
]

# Utilities
def build_adjacency_list(): -> dict[str, list[tuple]]
def build_adjacency_matrix(): -> list[list[float]]
```

**Constraints:**
- All algorithm files must `import NODES, EDGES, NODE_LABELS from data.network`
- No hardcoding edge data in `task_a/dijkstra.py`, `task_a/mst.py`, etc.
- If data changes, update `data/network.py` only; all algorithms automatically use new data

### 5.2 Test Datasets by Question

| Question | Dataset | Specification |
|----------|---------|---------------|
| **Q8/Q9 (BST/AVL)** | Order IDs | `[1045, 1023, 1078, 1012, 1034, 1056, 1089, 1005, 1020, 1067, 1050, 1098]` (12 elements) |
| **Q14 (Priority Queue)** | Orders with priority | 10 orders: 5 urgent (priority 1), 3 standard (priority 2), 2 low (priority 3) |
| **Q18 (Sorting)** | Zones + Priority tuples | `[(Z01, 1), (Z02, 3), (Z03, 1), ... (Z15, 2)]` (15 tuples from brief) |
| **Q19 (Binary Search)** | Sorted order ID array | Range 10001–11000 (1000 elements); search for target = 10347 |
| **Q20 (Divide-and-Conquer)** | Simulated orders | 6000 orders distributed across 24 hours; track peak/off-peak |
| **Q22 (Sort Benchmark)** | Random datasets | Sizes [100, 500, 1000, 5000, 10000]; random integers for each run |

### 5.3 Data Validation
- **Script:** `data/network.py` must include validation:
  ```python
  def validate_network():
      assert len(NODES) == 15, "Must have exactly 15 nodes"
      assert len(EDGES) == 24, "Must have exactly 24 edges"
      # Check bidirectionality, weight ranges, etc.
  ```
- **Call in main.py:** `validate_network()` before any algorithm execution

---

## 6. Output and Reporting Standards

### 6.1 Code Output (Console/Terminal)

#### 6.1.1 Requirements
- Every `if __name__ == "__main__":` block must produce **clearly labeled, readable terminal output**
- Use **separator lines** (e.g., `"="*50`, `"-"*50`) between sections in printed output
- Print **algorithm complexity** (Big O: time, space) at the end of each implementation section

#### 6.1.2 Example Output Format
```
==================================================
Q2: Dijkstra's Single-Source Shortest Path
==================================================
Graph: 15 nodes, 24 edges (from data.network)
Start Node: H1 (Dubai Marina Hub)
End Node: D1 (Al Barsha Distribution)

Dijkstra Trace:
Step 1: Initialization
  dist[H1] = 0, unvisited = {all nodes}
Step 2: Process H1 (dist=0)
  Update H2: dist=3.5, H3: dist=8.0, H4: dist=...
Step 3: Process H2 (dist=3.5)
  Update neighbors: ...
...
Step N: Finish
  dist[D1] = 8 km (FINAL ANSWER)

Path: H1 → H3 → D1
Distance: 8.0 km
Time: 15 min
Cost: 5.50 AED

Complexity:
  Time: O((V + E) log V) with min-heap
  Space: O(V)

==================================================
```

#### 6.1.3 Separator Consistency
- Top-level task separator: `"="*50`
- Subsection separator: `"-"*40`
- Data row separator: `"|"`
- Result box: `"─"*30` or `"-"*30`

### 6.2 Figure Output (matplotlib)

#### 6.2.1 Saving Specification
All figures must be saved using:
```python
import matplotlib.pyplot as plt
plt.savefig(
    f"outputs/{descriptive_filename}.png",
    dpi=150,
    bbox_inches="tight",
    facecolor="white"
)
```

#### 6.2.2 Figure Requirements
- **Filename:** Descriptive (e.g., `dijkstra_h1_d1.png`, `sort_benchmark_comparison.png`, `avl_tree_final.png`)
- **Title:** Must appear on figure (e.g., `plt.title("Dijkstra's Algorithm: H1 → D1")`)
- **Axis Labels:** Required where applicable (e.g., x-axis: "Array Size", y-axis: "Comparisons")
- **Legend:** Required if multiple series (e.g., separate lines for Bubble, Merge, Quick sort)
- **Resolution:** 150 DPI minimum
- **Color Scheme:** Professional (avoid neon colors; use matplotlib's default or seaborn colorblind palette)

#### 6.2.3 Sample Figures by Question
| Question | Figure Type | Filename | Content |
|----------|-------------|----------|---------|
| Q6 | Network graph | `q6_path_simulator.png` | Nodes, edges, highlighted path overlay |
| Q8 | Tree diagram | `q8_bst_structure.png` | BST nodes with edges, labels |
| Q9 | Tree diagram | `q9_avl_final_balanced.png` | AVL tree after rotations |
| Q18 | Line plot | `q18_sorting_benchmark.png` | 3 lines (Bubble, Merge, Quick) vs array size |
| Q22 | Bar chart | `q22_algorithm_comparison.png` | 5 bars (dataset sizes) with comparison counts |
| Q27 | Network state | `q27_network_simulator_blockage.png` | Before/after blockage (2 subplots) |

### 6.3 Technical Report Figures

#### 6.3.1 Inclusion Standard
- Every simulation figure (Q6, Q22, Q27) must appear in the **technical report** (Word document or PDF)
- Every tree diagram (Q8, Q9) should be included or hand-drawn equivalent

#### 6.3.2 Caption Format
```
Figure N: [Description]. 
Generated by: [filename.py]
Algorithm: [algorithm name]
Input: [key parameters]
Output: [key results]
```

**Example:**
```
Figure 1: Dijkstra's Algorithm Trace (H1 → D1)
Generated by: task_a/dijkstra.py
Algorithm: Dijkstra's single-source shortest path
Input: Graph from data/network.py, start=H1, end=D1
Output: Path = [H1, H3, D1], Distance = 8 km, Time = 15 min
```

---

## 7. Question-to-File Mapping

| Q# | Description | File | Function(s) | Type | Marks | Status |
|----|-------------|------|-------------|------|-------|--------|
| 1 | Graph Construction | `task_a/graph.py` | `build_graph()`, `to_adjacency_list()`, `to_adjacency_matrix()` | Algorithm | 5 | — |
| 2 | Dijkstra's Algorithm | `task_a/dijkstra.py` | `dijkstra()` | Algorithm | 10 | — |
| 3 | Floyd-Warshall | `task_a/floyd_warshall.py` | `floyd_warshall()` | Algorithm | 10 | — |
| 4 | MST (Kruskal's + Prim's) | `task_a/mst.py` | `kruskal()`, `prim()` | Algorithm | 15 | — |
| 5 | (Reserved/Extension) | — | — | — | — | — |
| 6 | Path Simulator (Basic) | `task_a/path_simulator_basic.py` | `assign_rider()`, `simulate_delivery()` | Simulation | 10 | — |
| 7 | BFS + DFS | `task_a/traversals.py` | `bfs()`, `dfs()` | Algorithm | 10 | — |
| 8 | BST | `task_b/bst.py` | `BST.insert()`, `BST.search()`, `BST.height()` | Data Structure | 10 | — |
| 9 | AVL Tree | `task_b/avl.py` | `AVL.insert()`, `AVL.rotate_left()`, `AVL.rotate_right()` | Data Structure | 15 | — |
| 10 | (Reserved/Extension) | — | — | — | — | — |
| 11 | (Reserved/Extension) | — | — | — | — | — |
| 12 | Linked List | `task_c/linked_list.py` | `LinkedList.insert()`, `LinkedList.delete()` | Data Structure | 10 | — |
| 13 | Circular Linked List | `task_c/circular_list.py` | `CircularList.insert()`, `CircularList.round_robin()` | Data Structure | 10 | — |
| 14 | Priority Queue | `task_c/priority_queue.py` | `PriorityQueue.insert()`, `PriorityQueue.extract_min()` | Data Structure | 10 | — |
| 15 | Stack | `task_c/stack.py` | `Stack.push()`, `Stack.pop()`, `Stack.peek()` | Data Structure | 5 | — |
| 16 | (Reserved/Extension) | — | — | — | — | — |
| 17 | (Reserved/Extension) | — | — | — | — | — |
| 18 | Sorting (Merge + Quick) | `task_d/sorting.py` | `merge_sort()`, `quick_sort()` | Algorithm | 10 | — |
| 19 | Binary Search | `task_d/searching.py` | `binary_search()` | Algorithm | 5 | — |
| 20 | Divide & Conquer | `task_d/searching.py` | `merge_count_inversions()` | Algorithm | 5 | — |
| 21 | (Reserved/Extension) | — | — | — | — | — |
| 22 | Sort Benchmark | `task_d/sort_benchmark.py` | `benchmark_sorting()` | Simulation | 15 | — |
| 23 | (Reserved/Extension) | — | — | — | — | — |
| 24 | (Reserved/Extension) | — | — | — | — | — |
| 25 | (Reserved/Extension) | — | — | — | — | — |
| 26 | (Reserved/Extension) | — | — | — | — | — |
| 27 | Comprehensive Simulator | `task_e/simulator.py` | `simulate_network()`, `handle_blockage()` | Simulation | 15 | — |

---

## 8. Marks Allocation Summary

### 8.1 Marks by Task Area

| Task Area | Questions | Total Marks | High Priority (15+) |
|-----------|-----------|------------|-------------------|
| **Task A** (Graph & Paths) | Q1–Q7 | 60 | Q4 (15), Q2 (10), Q3 (10) |
| **Task B** (Trees) | Q8–Q9 | 25 | Q9 (15) |
| **Task C** (Linear Structures) | Q12–Q15 | 35 | None |
| **Task D** (Sorting & Searching) | Q18–Q20, Q22 | 45 | Q22 (15), Q4 (15 via MST) |
| **Task E** (Comprehensive) | Q27 | 15 | Q27 (15) |
| **TOTAL** | 27 | **180** | **5 high-priority questions** |

### 8.2 High-Priority Questions (15 Marks Each)
These questions must be completed and tested thoroughly before final submission:
1. **Q4 — MST (Kruskal's + Prim's):** 15 marks — requires hand-traced edge selection order
2. **Q9 — AVL Tree:** 15 marks — requires rotation diagrams and height comparison with BST
3. **Q22 — Sort Benchmark:** 15 marks — requires 5 dataset sizes, comparison counts, visualization
4. **Q27 — Comprehensive Simulator:** 15 marks — requires network state before/after blockage

### 8.3 Marks Distribution Rationale
- **Algorithms (Q1–Q7, Q18–Q20):** 65% of total marks — core learning outcomes
- **Data Structures (Q8–Q15):** 35% of total marks — application and design
- **Simulation & Benchmarking (Q6, Q22, Q27):** embedded within algorithm tasks; not separate
- **Report & Documentation:** additional +15% bonus if hand-traces and visualizations are complete and clear

---

## 9. Compliance Checklist

Use the following checklist to verify readiness for submission. All items must be checked ✅ before final submission.

### 9.1 Code Quality & Standards
- [ ] Python version confirmed as 3.10+: `python --version` returns 3.10 or later
- [ ] `requirements.txt` present with `matplotlib>=3.7` and all dependencies
- [ ] All `.py` files include `# Python 3.10+` comment at the top
- [ ] No use of prohibited libraries (e.g., no `import heapq` as primary PriorityQueue, no `nx.dijkstra_path(...)` for algorithm computation)
- [ ] All algorithms labeled with `# Manual implementation of [algorithm name]`
- [ ] All benchmark code labeled with `# [BENCHMARK ONLY — not primary implementation]`
- [ ] Each algorithm includes test function `test_[algorithm_name]()` with manual trace

### 9.2 Data Integrity
- [ ] `data/network.py` contains exactly 15 nodes and 24 bidirectional edges
- [ ] `data/network.py` includes `validate_network()` function
- [ ] All algorithm files import from `data.network` (not hardcoded edge data)
- [ ] All test datasets match specification (Q8: 12 order IDs, Q19: 1000-element array, etc.)

### 9.3 Visualization Standards
- [ ] All matplotlib figures saved to `outputs/` directory at 150+ DPI
- [ ] All `.png` files include title, axis labels, legend (where applicable)
- [ ] Each figure has descriptive filename (e.g., `dijkstra_h1_d1.png`, not `figure1.png`)
- [ ] Q6, Q22, Q27 figures are included in technical report with captions

### 9.4 Hand-Traced Solutions
- [ ] All 14 numerical questions (Q1–Q4, Q7–Q9, Q12–Q15, Q18–Q20) include step-by-step traces
- [ ] Traces shown in technical report as tables (Dijkstra steps) or diagrams (tree structures)
- [ ] Final answers supported by intermediate working (not final answer alone)

### 9.5 Documentation
- [ ] `README.md` present with sections: Overview, Prerequisites, Installation, How to Run, Sample Output, File Structure, Academic Integrity
- [ ] `README.md` includes exact terminal commands for setup and execution
- [ ] `TRD.md` (this document) included in repository
- [ ] `references.txt` includes all external citations (textbooks, documentation, tutorials)

### 9.6 File Structure
- [ ] Project folder contains all required directories: `data/`, `task_a/`, `task_b/`, `task_c/`, `task_d/`, `task_e/`, `utils/`, `outputs/`
- [ ] All files match file structure in section 4.1
- [ ] `main.py` present as single entry point with menu
- [ ] `.gitignore` excludes `outputs/`, `__pycache__/`, `.venv/`

### 9.7 Academic Integrity
- [ ] All AI-assisted code marked with `# [AI-ASSISTED: tool=..., purpose=..., reviewed by=...]`
- [ ] All benchmark code labeled as `# [BENCHMARK ONLY]`
- [ ] `README.md` includes Academic Integrity statement (section 3.6.5)
- [ ] No copy-pasted solutions from Stack Overflow, GitHub, or other sources
- [ ] External references cited in code comments and `references.txt`

### 9.8 Testing & Verification
- [ ] `main.py` runs without errors; menu displays all 27 questions
- [ ] Each question (Q1–Q27) produces readable console output with complexity notation
- [ ] Each figure-generating task (Q6, Q22, Q27) produces `.png` file in `outputs/`
- [ ] At least 2 test cases per algorithm function pass manual verification

### 9.9 Final Submission Checklist
- [ ] All code committed to GitHub repository `https://github.com/rd51/waselx`
- [ ] Latest commit includes: all `.py` files, `.png` figures, `README.md`, `TRD.md`, `requirements.txt`
- [ ] Technical report (Word or PDF) includes hand-traces, figures, final answers
- [ ] Team member names and individual contributions documented (optional separate file: `CONTRIBUTORS.md`)
- [ ] Project folder is clean (no temporary files, debug prints commented out)

---

## 10. Sign-Off

| Role | Name | Signature | Date |
|------|------|-----------|------|
| Project Lead | [Name] | _____ | [Date] |
| Technical Lead | [Name] | _____ | [Date] |
| QA / Testing | [Name] | _____ | [Date] |
| Academic Advisor | [Instructor] | _____ | [Date] |

---

## Appendices

### Appendix A: Glossary
- **DSA:** Data Structures and Algorithms
- **Q#:** Question number (Q1–Q27)
- **TRD:** Technical Requirements Document
- **CLI:** Command-line interface
- **DPI:** Dots per inch (resolution metric for images)
- **Big O:** Asymptotic complexity notation

### Appendix B: References & Further Reading
- Cormen, T. H., Leiserson, C. E., Rivest, R. L., & Stein, C. (2009). *Introduction to Algorithms* (3rd ed.). MIT Press.
- Bhargava, A. Y. (2016). *Grokking Algorithms: An Illustrated Guide for Programmers*. Manning Publications.
- Python Software Foundation. (n.d.). *The Python Tutorial*. Retrieved from https://docs.python.org/3/
- matplotlib Documentation. (n.d.). Retrieved from https://matplotlib.org/
- NetworkX Documentation. (n.d.). Retrieved from https://networkx.org/

### Appendix C: Revision History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | May 3, 2025 | DSA Team | Initial TRD draft; all 27 questions defined; compliance checklist added |

---

**Document Status:** Draft v1.0  
**Last Updated:** May 3, 2025  
**Next Review:** Upon team submission  
**Approved By:** [Instructor Name]

---
