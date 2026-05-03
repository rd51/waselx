# Task Area B: Trees, BST & Balanced Trees

**Program:** MAIB — Data Structures & Algorithms Final Project  
**Section:** Task B — Binary Search Tree & AVL Tree Analysis  
**Total Marks:** Q8 (12) + Q9 (12) + Q10 (10) + Q11 (8) = **42 marks**  
**Status:** [PLACEHOLDER: In Progress / Completed]

---

## Q8 [12 marks] — Binary Search Tree (12 Order IDs)

**Context:** WaselX order dispatch system uses order IDs to track deliveries. A team member proposes storing order IDs in a BST for faster lookup during dispatch operations.

**Insertion sequence:** 1045, 1023, 1078, 1012, 1034, 1056, 1089, 1005, 1020, 1067, 1050, 1098

---

### Q8a) BST Diagram After All 12 Insertions [4 marks]

**Requirement:** Draw the final BST structure showing the tree after inserting all 12 order IDs in the given sequence. Must show parent-child relationships, not just a list.

**Format:** Use ASCII art or photograph of hand-drawn diagram. Each node shows the order ID.

**Example format:**
```
           1045
          /    \
       1023    1078
       /  \    /  \
    1012  1034 1056 1089
    /       \     \    \
  1005    [???] [???] [???]
```

**Your Answer:**

```
[INSERT ASCII tree diagram showing all 12 nodes with correct parent-child relationships]
Example:
           [root]
          /      \
       [left]    [right]
       /   \     /    \
      ... (etc)
```

**Explanation of tree structure:**
[INSERT: 3–5 sentences explaining the insertion order and how the tree grew]

---

### Q8b) Traversals [4 marks]

**Requirement:** Print the order IDs in three different tree traversal orders. Each traversal should visit all 12 nodes exactly once.

#### In-order Traversal (left → root → right)
*Property: Produces sorted output (ascending order)*

**Path traced:**
```
[INSERT: step-by-step trace showing which subtree visited at each step]
```

**Result (sorted order):**
```
[INSERT: 1005, 1012, 1020, 1023, 1034, 1045, 1050, 1056, 1067, 1078, 1089, 1098]
```

---

#### Pre-order Traversal (root → left → right)
*Property: Useful for tree copying; root always appears first*

**Path traced:**
```
[INSERT: step-by-step trace]
```

**Result (pre-order):**
```
[INSERT: 1045, 1023, 1012, 1005, 1020, 1034, 1078, 1056, 1050, 1067, 1089, 1098]
```

---

#### Post-order Traversal (left → right → root)
*Property: Useful for tree deletion; root always appears last*

**Path traced:**
```
[INSERT: step-by-step trace]
```

**Result (post-order):**
```
[INSERT: 1005, 1020, 1012, 1034, 1023, 1050, 1067, 1056, 1089, 1098, 1078, 1045]
```

---

### Q8c) Search for Order ID 1067 [2 marks]

**Requirement:** Trace the search path from root to target node 1067. Count the number of comparisons made.

**Search process:**

| Step | Current Node | Comparison | Decision | Comparison #|
|------|-------------|------------|----------|-------------|
| 1 | 1045 | 1067 > 1045? | Go right | 1 |
| 2 | [INSERT] | [INSERT comparison] | [INSERT decision] | 2 |
| 3 | [INSERT] | [INSERT comparison] | [INSERT decision] | 3 |
| 4 | 1067 | 1067 == 1067? | Found | 4 |

**Final answer:**
- **Path from root:** 1045 → [INSERT node] → [INSERT node] → 1067
- **Number of comparisons:** [INSERT — e.g., "4 comparisons"]
- **Nodes visited:** [INSERT — list in order]

---

### Q8d) Delete Order ID 1078 (Cancelled Order) [2 marks]

**Context:** Order 1078 was cancelled. Remove it from the BST while maintaining BST properties.

**Deletion analysis:**

**Step 1: Locate node to delete**
- Node 1078 found in tree: [INSERT location — e.g., "right child of 1045"]

**Step 2: Determine deletion case**
- **Case 1** — Leaf node (no children): Direct removal
- **Case 2** — One child: Replace with child
- **Case 3** — Two children: Replace with in-order successor (leftmost node in right subtree) or predecessor

**Deletion case applied:** [INSERT — e.g., "Case 3: two children"]

**Step 3: Find replacement node (if two children)**
- In-order successor of 1078: [INSERT node — e.g., "1089 (smallest node in right subtree)"]
- OR In-order predecessor of 1078: [INSERT node]

**Step 4: Perform deletion**
- Remove 1078
- Replace with [INSERT successor/predecessor]
- Update parent pointers

**BST after deletion:**

```
[INSERT updated ASCII tree after deleting 1078]
           1045
          /    \
       1023    1089
       /  \    /  \
    1012  1034 1056 [???]
    /       \     \
  1005    [???]  [???]
```

**Explanation:**
[INSERT: 2–3 sentences explaining how the tree was restructured after deletion]

---

## Q9 [12 marks] — AVL Tree (Same 12 Order IDs, With Self-Balancing)

**Context:** The unbalanced BST from Q8 shows poor performance in worst-case scenarios. An AVL tree automatically balances itself using rotations to maintain O(log n) search guarantee.

**Insertion sequence (same as Q8):** 1045, 1023, 1078, 1012, 1034, 1056, 1089, 1005, 1020, 1067, 1050, 1098

---

### Q9a) BST Height Comparison [2 marks]

**From Q8 (unbalanced BST):**
- **Tree height:** [INSERT — count longest path from root to leaf; e.g., "5 levels"]
- **Calculation:** longest path = [INSERT nodes visited]
- **Worst-case search time in BST:** O(height) = O([INSERT])

**AVL tree (balanced):**
- **Tree height:** [INSERT — e.g., "4 levels" (guaranteed ≤ 1.44 × log(n))]
- **Worst-case search time in AVL:** O(log n) = O(log 12) ≈ O([INSERT])

**Height reduction:** [INSERT — e.g., "From 5 to 4; saves 1 comparison in worst case"]

---

### Q9b) AVL Insertion With Rotations — Show At Least 2 Rotations [6 marks]

**AVL Property:** Every node's left and right subtrees have heights differing by at most 1. **Balance factor = height(left) - height(right)**.
- Valid balance factor: -1, 0, or +1
- Invalid (trigger rotation): -2 or +2

#### Rotation 1 — Triggered After Inserting [INSERT order ID]

**Before Rotation (showing imbalance):**

```
Imbalanced subtree:
           [INSERT node with BF = +2 or -2]
          /                    \
    (BF=?)                  (BF=?)
    /    \                  /    \
  ...    ...              ...    ...

Balance factors shown in parentheses: (BF = left_height - right_height)
```

**Rotation Type:** [INSERT — Left Rotate / Right Rotate / Left-Right / Right-Left]

**Rationale:** [INSERT — 2–3 sentences explaining why this rotation was needed]

**After Rotation:**

```
Rebalanced subtree:
           [INSERT node]
          /             \
    (BF=?)            (BF=?)
    /    \            /    \
  ...    ...        ...    ...

All balance factors now in [-1, 0, +1]
```

---

#### Rotation 2 — Triggered After Inserting [INSERT order ID]

**Before Rotation:**

```
Imbalanced subtree:
           [INSERT node with BF = ±2]
          /                    \
    (BF=?)                  (BF=?)
    /    \                  /    \
  ...    ...              ...    ...
```

**Rotation Type:** [INSERT — Left Rotate / Right Rotate / Left-Right / Right-Left]

**Rationale:** [INSERT — explanation]

**After Rotation:**

```
Rebalanced subtree:
           [INSERT node]
          /             \
    (BF=?)            (BF=?)
    /    \            /    \
  ...    ...        ...    ...
```

---

### Q9c) Performance Comparison: Unbalanced BST vs AVL Tree [4 marks]

| Metric | Unbalanced BST (Q8) | AVL Tree (Q9) |
|--------|:-------------------:|:-------------:|
| **Tree height** | [INSERT] | [INSERT] |
| **Comparisons to find Order ID 1067** | [INSERT] | [INSERT] |
| **Comparisons to find Order ID 1005** | [INSERT] | [INSERT] |
| **Worst-case search (Big O)** | O(n) = O(12) | O(log n) = O([INSERT ≈ 4]) |
| **Insertion complexity** | O(n) worst | O(log n) |
| **Guaranteed height** | Unbounded (can be n−1) | ≤ 1.44 × log(n+1) |

**Key insight:** [INSERT — 2–3 sentences on why AVL is superior for guaranteed performance]

---

## Q10 [10 marks] — Data Structure Recommendation: BST vs AVL vs Hash Table

**Context:** WaselX is growing to **15,000 orders per day**. The dispatch team needs to recommend a data structure for the Order ID lookup system that optimizes three critical operations:

1. **Insertion** (new order every 2 seconds → ~15,000 insertions per day)
2. **Search** (customer support must answer "where is order X?" in <100ms)
3. **Range query** (analytics: "all orders between 10:00 and 11:30 AM?")

**Word count target:** 300 words  
**Marks distribution:** Table [2 marks] + Written analysis [8 marks]

---

### Complexity Comparison Table [2 marks]

| Operation | BST (Unbalanced) | AVL Tree | Hash Table |
|-----------|:----------------:|:--------:|:----------:|
| **Insert** | O(n) worst | O(log n) | O(1) average |
| **Search** | O(n) worst | O(log n) | O(1) average |
| **Delete** | O(n) worst | O(log n) | O(1) average |
| **Range query** | O(k + height) | O(k + log n) | **O(n)** — no ordering |
| **Space** | O(n) | O(n) | O(n) |
| **Ordering** | Yes (traversals) | Yes (traversals) | **No** |

**Legend:** k = number of elements in range; n = total elements; "—" = not applicable

---

### Written Recommendation [8 marks]

**Prompt:** Write a concise 300-word technical recommendation explaining which data structure is best for WaselX's order dispatch system.

**Structure your answer with:**
1. **Opening** — Restate the problem and three critical operations (50 words)
2. **Elimination analysis** — Why Hash Table fails range queries (70 words)
3. **BST vs AVL comparison** — Why unbalanced BST is too risky at scale (80 words)
4. **Final recommendation** — Advocate for AVL Tree with reasoning (60 words)
5. **Implementation note** — Timestamp as secondary index for range queries (40 words)

---

**Your Answer:**

[INSERT 300-word written analysis covering:]

[INSERT Opening paragraph (50 words):
- Restate problem: 15,000 orders/day, need fast insert + search + range query
- Introduce the three candidates: BST, AVL, Hash Table]

[INSERT Elimination analysis (70 words):
- Explain why Hash Table cannot efficiently handle range queries
- Example: "Query 'all orders from 10:00–11:30 AM' requires scanning entire hash table O(n) — unacceptable"]

[INSERT BST vs AVL comparison (80 words):
- Unbalanced BST risk: insertion sequence 1, 2, 3, ..., 15000 creates linear tree (height = n)
- At 15,000 orders: worst-case search = 15,000 comparisons
- AVL guarantee: height ≤ 1.44 × log(15,000) ≈ 38, so worst-case search = 38 comparisons
- Performance difference critical for 100ms SLA]

[INSERT Final recommendation (60 words):
- AVL Tree is the clear winner
- Provides O(log n) for all three operations
- Maintains ordering for range queries
- Slightly higher insertion cost (rebalancing) is worth the trade-off]

[INSERT Implementation note (40 words):
- Use order ID as primary key in AVL Tree
- Add secondary B-Tree or sorted list indexed by timestamp for efficient range queries
- Two-index approach ensures fast lookup + fast range queries]

---

## Q11 [8 marks] — COO Scaling Memo: Flat Array → Tree Migration

**Context:** WaselX's COO (Chief Operations Officer) is concerned about system performance as order volume scales. Current system uses a **flat sorted array of order IDs** with binary search. The COO asks for a technical assessment: "Should we migrate to a tree-based structure?"

**Your role:** Write a short consulting memo to the COO  
**Word count:** 250–300 words  
**Format:** Professional business memo  
**Marks:** Technical depth [5 marks] + Writing quality [3 marks]

---

### Memo Template

```
TO:       Chief Operations Officer, WaselX Express
FROM:     [INSERT Your Name], DSA Team
DATE:     [INSERT Date]
SUBJECT:  System Scaling Assessment: Flat Array vs AVL Tree for Order ID Lookup

---

EXECUTIVE SUMMARY
[INSERT 2–3 sentences explaining the recommendation and key improvement metric]
Example: "We recommend migrating from flat sorted array to AVL Tree to handle 
projected 4x order volume growth. Primary benefit: insertion cost reduction from 
O(n) to O(log n), enabling sustainable scaling beyond 15,000 orders/day."

---

CURRENT SYSTEM ANALYSIS
Current Architecture:
- Flat sorted array of order IDs
- Search operation: O(log n) binary search ✓ (acceptable)
- Insertion operation: O(n) due to array shifting ✗ (problematic)

Performance Metrics at Scale:
- Current volume: 3,500 orders/day → worst-case insertion = 3,500 shifts per insert
- Projected volume (2026): 15,000 orders/day → worst-case insertion = 15,000 shifts per insert
- Cost per shift: [INSERT — e.g., "1–2 milliseconds"] 
- Projected total insertion time: 15,000 × 15,000 = 225 million shifts per day = [INSERT hours unacceptable]

BOTTLENECK IDENTIFICATION
[INSERT 1–2 paragraphs analyzing why insertion is the critical bottleneck]
- Array insertion requires shifting all elements after insertion point
- At 3,500–15,000 insertions per day, cumulative shift cost becomes prohibitive
- Bottleneck worsens non-linearly as volume grows: doubling orders ≈ 4x shift overhead

---

PROPOSED SOLUTION: AVL TREE MIGRATION

Performance Gain:
| Operation | Current Array | Proposed AVL | Improvement |
|-----------|:-------------:|:------------:|:-----------:|
| Insert | O(n) | O(log n) | 100–1000x faster |
| Search | O(log n) | O(log n) | No change |
| Delete | O(n) | O(log n) | 100–1000x faster |
| Range query | O(log n + k) | O(log n + k) | No change |

Scaling example: At 15,000 orders/day
- Array insertion: avg 7,500 shifts → [INSERT time, e.g., "15 seconds total"]
- AVL insertion: max 38 comparisons → [INSERT time, e.g., "0.04 seconds total"]

---

MIGRATION PLAN

Phase 1 — Preparation (Week 1):
[INSERT steps: export current sorted array to CSV, validate data integrity, etc.]

Phase 2 — Development (Week 2–3):
[INSERT steps: implement AVL Tree class, build tree from existing data, test all operations]

Phase 3 — Parallel Validation (Week 4):
[INSERT steps: run both systems side-by-side, compare results, benchmark performance]

Phase 4 — Cutover (Week 5):
[INSERT steps: switch read/write traffic to AVL, decommission array, monitor for issues]

Estimated timeline: [INSERT 4–6 weeks]
Estimated effort: [INSERT developer hours or team-days]

---

RISKS & MITIGATION

Risk 1 — Tree rebalancing overhead during peak orders
Mitigation: [INSERT — implement background rebalancing, or batch insertions]

Risk 2 — Compatibility with existing APIs expecting array interface
Mitigation: [INSERT — wrapper class implements array-like getitem/setitem]

---

RECOMMENDATION

Proceed with AVL Tree migration to future-proof the order dispatch system for 
projected growth. The insertion cost reduction from O(n) to O(log n) is essential 
for maintaining <100ms dispatch latency at 15,000+ orders/day.

Next step: Approve development phase budget (Phase 2–3).

---
```

---

### Your Answer:

[INSERT 250–300 word memo addressing all sections above]

**Memo checklist:**
- [ ] TO/FROM/DATE/SUBJECT header included
- [ ] EXECUTIVE SUMMARY: One sentence stating recommendation + key metric
- [ ] CURRENT SYSTEM ANALYSIS: Shows O(n) bottleneck with scaled numbers (3,500 → 15,000)
- [ ] Calculation example: "15,000 orders × 7,500 avg shifts = X seconds per day"
- [ ] PROPOSED SOLUTION: AVL Tree with performance table showing 100–1000x improvement
- [ ] MIGRATION PLAN: 4–5 phases with timeline
- [ ] RISKS: At least 2 risks identified + mitigations
- [ ] RECOMMENDATION: Clear decision statement
- [ ] Professional tone, business vocabulary

---

## Summary: Task B Marks & Status

| Question | Topic | Marks | Completed? |
|----------|-------|-------|:----------:|
| Q8 | BST Construction & Operations | 12 | [ ] |
| Q9 | AVL Tree Balancing & Rotations | 12 | [ ] |
| Q10 | Data Structure Recommendation | 10 | [ ] |
| Q11 | Scaling Memo & Migration Strategy | 8 | [ ] |
| **Total** | **Trees & Balancing** | **42** | [ ] |

---

## Notes for Team

1. **Hand-drawn diagrams acceptable:** Q8a and Q9b tree diagrams can be drawn by hand, photographed, and inserted as images.
2. **AI-assisted code permitted:** If using ChatGPT for memo structure, mark with `[AI-ASSISTED: tool=ChatGPT, purpose=memo template, reviewed by=...]`
3. **Validation:** All traversals in Q8b must be manually traced (not computer-generated) and show working.
4. **Performance calculations:** Q11 memo must include at least one concrete calculation (e.g., "15,000 orders × 7,500 shifts/insert = X million shifts/day").

---

**Document Status:** Answer shell complete; ready for team to fill in [INSERT ...] sections  
**Last Updated:** May 3, 2025  
**Assigned To:** [PLACEHOLDER — team member name]
