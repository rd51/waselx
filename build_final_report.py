from __future__ import annotations

import re
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle


ROOT = Path(__file__).resolve().parent
OUTPUT_MD = ROOT / "REPORT_TEMPLATE.md"
OUTPUT_PDF = ROOT / "REPORT_TEMPLATE.pdf"


def read_section(path: Path) -> str:
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    if lines and lines[0].startswith("# Task Area"):
        lines = lines[1:]
    while lines and not lines[0].strip():
        lines = lines[1:]
    return "\n".join(lines).strip() + "\n"


def task_a_section() -> str:
    return """## Task Area A: Graph Algorithms

[INSERT Task Area A section here]

### Q1 [10 marks] - Graph Basics (Adjacency List + Matrix)

**Context:** WaselX delivery network consists of 15 nodes and 24 weighted bidirectional edges. Describe the adjacency list and adjacency matrix representations, then compare them for route planning.

**Your Answer:**

[INSERT complete answer for Q1, including: adjacency list summary, adjacency matrix snapshot, and comparison paragraph]

### Q2 [15 marks] - Dijkstra's Shortest Path

**Context:** Find the shortest path from H1 to D1 using Dijkstra's algorithm and show the hand trace.

**Your Answer:**

[INSERT complete answer for Q2, including: step-by-step trace, final path, total distance, and complexity]

### Q3 [15 marks] - Floyd-Warshall All-Pairs Shortest Paths

**Context:** Use Floyd-Warshall to compare all hub-to-hub routes and identify the best-connected hub.

**Your Answer:**

[INSERT complete answer for Q3, including: matrix iterations, best hub, farthest pair, and new edge recommendation]

### Q4 [15 marks] - Minimum Spanning Tree (Kruskal + Prim)

**Context:** Build a minimum-cost backbone for the delivery network using MST algorithms.

**Your Answer:**

[INSERT complete answer for Q4, including: Kruskal edge order, cycle checks, Prim growth, and total cost]

### Q5 [10 marks] - CTO Memo: Dijkstra vs Floyd-Warshall

**Context:** Recommend which path algorithm should be used for different business needs.

**Your Answer:**

[INSERT complete answer for Q5, including: executive memo, trade-off analysis, and recommendation]

### Q6 [15 marks] - Interactive Path Simulator

**Context:** Present the Dijkstra path visualization and the two-path overlay for route comparison.

**Your Answer:**

[INSERT complete answer for Q6, including: figure caption text, path trace, and explanation of visualization]

### Q7 [10 marks] - BFS & DFS Traversals

**Context:** Traverse the network from H3 using BFS and DFS and compare the visitation orders.

**Your Answer:**

[INSERT complete answer for Q7, including: BFS order, DFS order, and connectivity note]

---
"""


def assemble_markdown() -> str:
    task_b = read_section(ROOT / "TASK_B_TREES.md")
    task_c = read_section(ROOT / "TASK_C_QUEUES.md")
    task_d = read_section(ROOT / "TASK_D_SORTING_SEARCHING.md")
    task_e = read_section(ROOT / "TASK_E_MANAGEMENT_LEADERSHIP.md")

    return f"""# WaselX Express - Technical Report
## Optimizing Last-Mile Delivery Operations Across the UAE Using Data Structures & Algorithms
**Program:** MAIB - Data Structures & Algorithms  
**Project Type:** Group Final Project  
**Team Members:**

| Name | Student ID | Primary Responsibility |
|------|-----------|------------------------|
| [Name 1] | [ID] | Task A + B (Graph, Trees) |
| [Name 2] | [ID] | Task C + D (Lists, Sorting) |
| [Name 3] | [ID] | Task E + Report (Strategy, Simulator) |
| [Name 4] | [ID] | Review + Presentation |

**Submission Date:** [INSERT]  
**Total Word Count:** ~[INSERT]  
**Total Marks Available:** 310

---

## Table of Contents

- [Task Area A: Graph Algorithms](#task-area-a-graph-algorithms)
  - [Q1 [10 marks] - Graph Basics (Adjacency List + Matrix)](#q1-10-marks---graph-basics-adjacency-list--matrix)
  - [Q2 [15 marks] - Dijkstra's Shortest Path](#q2-15-marks---dijkstras-shortest-path)
  - [Q3 [15 marks] - Floyd-Warshall All-Pairs Shortest Paths](#q3-15-marks---floyd-warshall-all-pairs-shortest-paths)
  - [Q4 [15 marks] - Minimum Spanning Tree (Kruskal + Prim)](#q4-15-marks---minimum-spanning-tree-kruskal--prim)
  - [Q5 [10 marks] - CTO Memo: Dijkstra vs Floyd-Warshall](#q5-10-marks---cto-memo-dijkstra-vs-floyd-warshall)
  - [Q6 [15 marks] - Interactive Path Simulator](#q6-15-marks---interactive-path-simulator)
  - [Q7 [10 marks] - BFS & DFS Traversals](#q7-10-marks---bfs--dfs-traversals)
- [Task Area B: Binary Search Trees](#task-area-b-binary-search-trees)
  - [Q8 [12 marks] - BST Insertion, Traversal & Search](#q8-12-marks---bst-insertion-traversal--search)
  - [Q9 [12 marks] - AVL Tree Balancing](#q9-12-marks---avl-tree-balancing)
  - [Q10 [10 marks] - BST vs AVL vs Hash Table](#q10-10-marks---bst-vs-avl-vs-hash-table)
  - [Q11 [8 marks] - Scaling Memo to CEO](#q11-8-marks---scaling-memo-to-ceo)
- [Task Area C: Linked Lists, Queues & Order Pipeline](#task-area-c-linked-lists-queues--order-pipeline)
  - [Q12 [10 marks] - Doubly Linked List (Rider Route)](#q12-10-marks---doubly-linked-list-rider-route)
  - [Q13 [8 marks] - Circular Linked List (8 Riders, 20 Orders)](#q13-8-marks---circular-linked-list-8-riders-20-orders)
  - [Q14 [12 marks] - Priority Queue (Min-Heap from Scratch)](#q14-12-marks---priority-queue-min-heap-from-scratch)
  - [Q15 [8 marks] - Stack (Order Lifecycle + Undo)](#q15-8-marks---stack-order-lifecycle--undo)
  - [Q16 [10 marks] - Single PQ vs 7 Zone Queues](#q16-10-marks---single-pq-vs-7-zone-queues)
  - [Q17 [10 marks] - Leadership Brief to CEO: Priority Queue Proposal](#q17-10-marks---leadership-brief-to-ceo-priority-queue-proposal)
- [Task Area D: Sorting, Searching & Divide and Conquer](#task-area-d-sorting-searching--divide-and-conquer)
  - [Q18 [12 marks] - Merge Sort + Quick Sort (15 Orders)](#q18-12-marks---merge-sort--quick-sort-15-orders)
  - [Q19 [10 marks] - Binary Search vs Linear Search](#q19-10-marks---binary-search-vs-linear-search)
  - [Q20 [10 marks] - Divide and Conquer Peak Hour Finder](#q20-10-marks---divide-and-conquer-peak-hour-finder)
  - [Q21 [8 marks] - Merge Sort vs Quick Sort for 50,000 Records](#q21-8-marks---merge-sort-vs-quick-sort-for-50000-records)
  - [Q22 [10 marks] - Sort Performance Benchmark](#q22-10-marks---sort-performance-benchmark)
- [Task Area E: Management, Leadership & Strategic Integration](#task-area-e-management-leadership--strategic-integration)
  - [Q23 [12 marks] - Executive Summary (Board Level)](#q23-12-marks---executive-summary-board-level)
  - [Q24 [10 marks] - Dual-Audience Algorithm Communication](#q24-10-marks---dual-audience-algorithm-communication)
  - [Q25 [10 marks] - Investment Decision Memo](#q25-10-marks---investment-decision-memo)
  - [Q26 [10 marks] - CTO Town Hall Response](#q26-10-marks---cto-town-hall-response)
  - [Q27 [15 marks] - Comprehensive Path Simulator](#q27-15-marks---comprehensive-path-simulator)
- [Figures Index](#figures-index)
- [References and Citations](#references-and-citations)
- [Academic Integrity Statement](#academic-integrity-statement)

---

{task_a_section()}
## Task Area B: Binary Search Trees

[INSERT Task Area B section here]

{task_b}
## Task Area C: Linked Lists, Queues & Order Pipeline

[INSERT Task Area C section here]

{task_c}
## Task Area D: Sorting, Searching & Divide and Conquer

[INSERT Task Area D section here]

{task_d}
## Task Area E: Management, Leadership & Strategic Integration

[INSERT Task Area E section here]

{task_e}

## Figures Index

| Figure # | Title | Source File | Question | Filename |
|----------|-------|------------|---------|---------|
| 1 | Dijkstra path H1->D4 | path_simulator_basic.py | Q6 | outputs/path_h1_d4.png |
| 2 | Two-path overlay | path_simulator_basic.py | Q6 | outputs/overlay_h5d5_h7d3.png |
| 3 | Sort benchmark chart | sort_benchmark.py | Q22 | outputs/sort_benchmark.png |
| 4 | Multi-criteria comparison | simulator.py | Q27 | outputs/simulator_comparison.png |
| 5 | Road closure rerouting | simulator.py | Q27 | outputs/closure_h1_d4.png |

---

## References and Citations

- [1] Cormen, T., Leiserson, C., Rivest, R., Stein, C. (2009). Introduction to Algorithms (3rd ed.). MIT Press.
- [2] Python Software Foundation. heapq - Heap queue algorithm. https://docs.python.org/3/library/heapq.html
- [3] Hunter, J. D. (2007). Matplotlib: A 2D graphics environment. Computing in Science & Engineering, 9(3), 90-95.
- [4] [INSERT any lecture notes, YouTube tutorials, or other sources used]

---

## Academic Integrity Statement

"We, the undersigned team members, confirm that all code and written analysis in this report was produced by our team. AI tools (GitHub Copilot) were used exclusively for debugging assistance and code suggestions. All AI-generated code is clearly marked with [AI-ASSISTED] comment blocks in the source files. No AI tool was used to generate the written management or leadership responses without disclosure."

Team signatures: [Name 1] | [Name 2] | [Name 3] | [Name 4]
"""


def escape_html(text: str) -> str:
    return (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )


def inline_format(text: str) -> str:
    text = escape_html(text)
    text = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", text)
    text = re.sub(r"\*(.+?)\*", r"<i>\1</i>", text)
    return text


def is_table_row(line: str) -> bool:
    return line.strip().startswith("|") and line.strip().endswith("|")


def parse_table(lines: list[str]):
    rows = []
    for line in lines:
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if cells and all(re.fullmatch(r"[:\-\s]+", cell or "") for cell in cells):
            continue
        rows.append(cells)
    return rows


def build_pdf(source_path: Path, target_path: Path) -> None:
    text = source_path.read_text(encoding="utf-8")
    lines = text.splitlines()

    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name="BodySmall", parent=styles["BodyText"], fontName="Helvetica", fontSize=8.5, leading=10.2, spaceAfter=3))
    styles.add(ParagraphStyle(name="Heading1Center", parent=styles["Title"], fontName="Helvetica-Bold", fontSize=18, leading=22, alignment=TA_CENTER, spaceAfter=8))
    styles.add(ParagraphStyle(name="Heading2Left", parent=styles["Heading1"], fontName="Helvetica-Bold", fontSize=13, leading=16, alignment=TA_LEFT, spaceBefore=8, spaceAfter=4))
    styles.add(ParagraphStyle(name="Heading3Left", parent=styles["Heading2"], fontName="Helvetica-Bold", fontSize=11, leading=13, alignment=TA_LEFT, spaceBefore=5, spaceAfter=3))
    styles.add(ParagraphStyle(name="MonoBlock", parent=styles["Code"], fontName="Courier", fontSize=8, leading=9.5, spaceAfter=4))

    doc = SimpleDocTemplate(
        str(target_path),
        pagesize=A4,
        rightMargin=16 * mm,
        leftMargin=16 * mm,
        topMargin=14 * mm,
        bottomMargin=14 * mm,
        title="WaselX Express - Technical Report",
        author="GitHub Copilot",
    )

    story = []
    i = 0
    in_code = False
    code_buffer: list[str] = []

    while i < len(lines):
        line = lines[i]
        stripped = line.strip()

        if stripped.startswith("```"):
            if in_code:
                if code_buffer:
                    story.append(Paragraph("<br/>".join(inline_format(code_line) for code_line in code_buffer), styles["MonoBlock"]))
                    story.append(Spacer(1, 2))
                code_buffer = []
                in_code = False
            else:
                in_code = True
            i += 1
            continue

        if in_code:
            code_buffer.append(line)
            i += 1
            continue

        if not stripped:
            story.append(Spacer(1, 4))
            i += 1
            continue

        if line.startswith("# "):
            story.append(Paragraph(inline_format(line[2:].strip()), styles["Heading1Center"]))
            i += 1
            continue

        if line.startswith("## "):
            story.append(Paragraph(inline_format(line[3:].strip()), styles["Heading2Left"]))
            i += 1
            continue

        if line.startswith("### "):
            story.append(Paragraph(inline_format(line[4:].strip()), styles["Heading3Left"]))
            i += 1
            continue

        if is_table_row(line):
            table_lines = [line]
            j = i + 1
            while j < len(lines) and is_table_row(lines[j]):
                table_lines.append(lines[j])
                j += 1
            rows = parse_table(table_lines)
            if rows:
                table = Table(
                    [[Paragraph(inline_format(cell), styles["BodySmall"]) for cell in row] for row in rows],
                    repeatRows=1,
                )
                table.setStyle(
                    TableStyle(
                        [
                            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#d9e8f5")),
                            ("TEXTCOLOR", (0, 0), (-1, 0), colors.black),
                            ("FONTNAME", (0, 0), (-1, -1), "Helvetica"),
                            ("FONTSIZE", (0, 0), (-1, -1), 8),
                            ("LEADING", (0, 0), (-1, -1), 9.5),
                            ("GRID", (0, 0), (-1, -1), 0.4, colors.grey),
                            ("VALIGN", (0, 0), (-1, -1), "TOP"),
                            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f7f9fc")]),
                            ("LEFTPADDING", (0, 0), (-1, -1), 4),
                            ("RIGHTPADDING", (0, 0), (-1, -1), 4),
                            ("TOPPADDING", (0, 0), (-1, -1), 3),
                            ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
                        ]
                    )
                )
                story.append(table)
                story.append(Spacer(1, 5))
            i = j
            continue

        if stripped.startswith("- ") or stripped.startswith("* "):
            story.append(Paragraph("• " + inline_format(stripped[2:]), styles["BodySmall"]))
            i += 1
            continue

        if re.match(r"^\d+\.\s+", stripped):
            story.append(Paragraph(inline_format(stripped), styles["BodySmall"]))
            i += 1
            continue

        if stripped == "---":
            story.append(Spacer(1, 4))
            i += 1
            continue

        story.append(Paragraph(inline_format(stripped), styles["BodySmall"]))
        i += 1

    doc.build(story)


if __name__ == "__main__":
    markdown = assemble_markdown()
    OUTPUT_MD.write_text(markdown, encoding="utf-8")
    build_pdf(OUTPUT_MD, OUTPUT_PDF)
    print(f"Generated markdown: {OUTPUT_MD}")
    print(f"Generated PDF: {OUTPUT_PDF}")
