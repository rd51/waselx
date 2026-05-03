# Task Area C: Linked Lists, Queues & Order Pipeline

**Program:** MAIB — Data Structures & Algorithms Final Project  
**Section:** Task C — Linear Data Structures for Order Routing  
**Total Marks:** Q12 (10) + Q13 (8) + Q14 (12) + Q15 (8) + Q16 (10) + Q17 (10) = **58 marks**  
**Status:** [PLACEHOLDER: In Progress / Completed]

---

## Q12 [10 marks] — Doubly Linked List (Rider Route)

**Context:** WaselX riders need to manage delivery routes dynamically. A rider may receive urgent orders that must be inserted mid-route, or orders may be cancelled requiring deletion. A doubly-linked list (DLL) allows efficient insertion/deletion in both directions.

**Implementation file:** `task_c/linked_list.py`

**Scenario:** Rider has route with 6 stops; then receives urgent order (insert after stop 3); then order 5 is cancelled (delete).

---

### Q12a) Python Implementation Output [6 marks]

**Requirement:** Run `task_c/linked_list.py` and capture terminal output showing the DLL operations.

**Expected output format:**

```
==================================================
Q12: Doubly Linked List (DLL) — Rider Route Management
==================================================

Initial Route (6 stops):
Forward:  Stop1 <-> Stop2 <-> Stop3 <-> Stop4 <-> Stop5 <-> Stop6
Reverse:  Stop6 <-> Stop5 <-> Stop4 <-> Stop3 <-> Stop2 <-> Stop1

Insert urgent order after Stop3:
Action: Insert "URGENT_Order_2847" after Stop3
Forward:  Stop1 <-> Stop2 <-> Stop3 <-> URGENT_Order_2847 <-> Stop4 <-> Stop5 <-> Stop6
Reverse:  Stop6 <-> Stop5 <-> Stop4 <-> URGENT_Order_2847 <-> Stop3 <-> Stop2 <-> Stop1

Delete Stop5 (Order cancelled):
Action: Delete "Stop5"
Forward:  Stop1 <-> Stop2 <-> Stop3 <-> URGENT_Order_2847 <-> Stop4 <-> Stop6
Reverse:  Stop6 <-> Stop4 <-> URGENT_Order_2847 <-> Stop3 <-> Stop2 <-> Stop1

Operations Summary:
- Total nodes in final route: 7
- Insert position: After node 3
- Traversal directions: Forward and Backward both O(1) from any node

==================================================
```

**Your Answer:**

[INSERT actual terminal output from running task_c/linked_list.py]

---

### Q12b) Justification — DLL vs Array [4 marks]

**Requirement:** Write a 100-word explanation of why DLL is superior to a sorted array for managing rider routes with frequent changes.

**Word count target:** 100 words (±10%)

**Key points to cover:**
- Insertion complexity comparison (O(1) vs O(n))
- Deletion complexity comparison (O(1) vs O(n))
- Bidirectional traversal (forward for delivery, reverse for undo)
- Practical WaselX scenario: route changes mid-delivery

**Your Answer:**

[INSERT 100-word justification]

**Example structure:**
- Sentence 1: "For a rider route with frequent changes..."
- Sentence 2–3: "In an array, insertion requires O(n) shifting..."
- Sentence 4–5: "In a DLL, insertion is O(1) because..."
- Sentence 6: "Traversal in both directions is natural in DLL..."
- Sentence 7: "Therefore, DLL is the clear choice for..."

---

## Q13 [8 marks] — Circular Linked List (8 Riders, 20 Orders)

**Context:** WaselX dispatch assigns orders to available riders using round-robin scheduling. A circular linked list cycles through riders automatically: Rider1 → Rider2 → ... → Rider8 → Rider1. Rider 4 goes on break after order 11, reducing the circle to 7 riders.

**Scenario:** 8 riders, 20 orders, Rider4 removed after order 11.

**Implementation file:** `task_c/circular_list.py`

---

### Q13a+b) Order Assignment Simulation — All 20 Orders [6 marks]

**Requirement:** Simulate round-robin assignment of 20 orders to 8 riders, then to 7 after Rider4 is removed.

**Table format:**

| Order # | Assigned Rider | Cumulative Orders (Rider) | Note |
|---------|----------------|--------------------------|------|
| 1 | Rider1 | Rider1: 1 | Initial round: start at Rider1 |
| 2 | Rider2 | Rider2: 1 | Next in circle |
| 3 | Rider3 | Rider3: 1 | Next in circle |
| 4 | Rider4 | Rider4: 1 | Next in circle |
| 5 | Rider5 | Rider5: 1 | [INSERT] |
| 6 | Rider6 | Rider6: 1 | [INSERT] |
| 7 | Rider7 | Rider7: 1 | [INSERT] |
| 8 | Rider8 | Rider8: 1 | [INSERT] |
| 9 | Rider1 | Rider1: 2 | Circle complete; restart |
| 10 | Rider2 | Rider2: 2 | [INSERT] |
| 11 | [INSERT] | [INSERT] | [INSERT] — Rider4 goes on break after this |
| 12 | [INSERT] | [INSERT] | Rider4 removed; circle now 7 riders only |
| 13 | [INSERT] | [INSERT] | [INSERT] |
| 14 | [INSERT] | [INSERT] | [INSERT] |
| 15 | [INSERT] | [INSERT] | [INSERT] |
| 16 | [INSERT] | [INSERT] | [INSERT] |
| 17 | [INSERT] | [INSERT] | [INSERT] |
| 18 | [INSERT] | [INSERT] | [INSERT] |
| 19 | [INSERT] | [INSERT] | [INSERT] |
| 20 | [INSERT] | [INSERT] | [INSERT] |

**Completion check:**
- [ ] All 20 orders assigned
- [ ] Orders 1–11 distributed among 8 riders
- [ ] After order 11: Rider4 removed
- [ ] Orders 12–20 distributed among 7 riders
- [ ] "Cumulative Orders" column shows load balancing

---

### Q13c) Terminal Output [2 marks]

**Requirement:** Capture full terminal output from `task_c/circular_list.py` showing round-robin assignments.

**Expected format:**

```
==================================================
Q13: Circular Linked List — Round-Robin Order Dispatch
==================================================

Initial Circle: Rider1 → Rider2 → Rider3 → Rider4 → Rider5 → Rider6 → Rider7 → Rider8 → [back to Rider1]

Assigning 20 orders:
Order 1 → Rider1 (Rider1 total: 1)
Order 2 → Rider2 (Rider2 total: 1)
...
Order 11 → [INSERT] ([INSERT] total: [INSERT])

Rider4 goes on break — removing from circle.

New Circle: Rider1 → Rider2 → Rider3 → Rider5 → Rider6 → Rider7 → Rider8 → [back to Rider1]
Order 12 → [INSERT] ([INSERT] total: [INSERT])
...
Order 20 → [INSERT] ([INSERT] total: [INSERT])

Final Assignments:
Rider1: [INSERT count] orders
Rider2: [INSERT count] orders
[INSERT for all 7 active riders]

==================================================
```

**Your Answer:**

[INSERT actual terminal output from running task_c/circular_list.py]

---

## Q14 [12 marks] — Priority Queue (Min-Heap from Scratch)

**Context:** WaselX receives orders with urgency levels: Level 1 (urgent), Level 2 (standard), Level 3 (low-priority). A min-heap priority queue ensures urgent orders are always dispatched first. **Implementation must be from scratch (no heapq library).**

**10 test orders:**
- Order_B: priority 1 (urgent), arrival 2
- Order_E: priority 1 (urgent), arrival 5
- Order_A: priority 1 (urgent), arrival 1
- Order_I: priority 1 (urgent), arrival 9
- Order_D: priority 2 (standard), arrival 4
- Order_H: priority 2 (standard), arrival 8
- Order_C: priority 3 (low), arrival 3
- Order_G: priority 3 (low), arrival 7
- Order_F: priority 2 (standard), arrival 6
- Order_J: priority 3 (low), arrival 10

**Implementation file:** `task_c/priority_queue.py`

---

### Q14a) Heap State After All 10 Enqueues [3 marks]

**Requirement:** Show the heap (as array) after each enqueue, demonstrating sift-up operation.

**Example format:**

```
==================================================
Q14a: Priority Queue Construction — Min-Heap State
==================================================

Initial heap (empty): []

Enqueue Order_B (priority=1, arrival=2):
  → Heap: [(1, 2, 'Order_B')]

Enqueue Order_E (priority=1, arrival=5):
  → Heap: [(1, 2, 'Order_B'), (1, 5, 'Order_E')]

Enqueue Order_A (priority=1, arrival=1):
  → Compare (1,1) with parent (1,2): swap (1,1 < 1,2 by arrival time)
  → Heap: [(1, 1, 'Order_A'), (1, 2, 'Order_B'), (1, 5, 'Order_E')]

Enqueue Order_I (priority=1, arrival=9):
  → Heap: [(1, 1, 'Order_A'), (1, 2, 'Order_B'), (1, 5, 'Order_E'), (1, 9, 'Order_I')]

...

[INSERT all 10 enqueue steps with heap state after each]

Final Heap: [INSERT complete final heap array showing all 10 elements]
```

**Heap properties to verify:**
- [ ] Min element always at index 0
- [ ] Parent of node i at index i//2 (heap ordering property maintained)
- [ ] All leaf nodes below level h

**Your Answer:**

[INSERT detailed heap state progression for all 10 enqueues]

---

### Q14b) Dequeue Order (All 10 Extractions) [6 marks]

**Requirement:** Extract all 10 orders from the min-heap in priority order. Show comparison logic: priority 1 < 2 < 3, ties broken by arrival time (FIFO within priority level).

**Table format:**

| Dequeue # | Order | Priority | Arrival Order | Extraction Logic |
|-----------|-------|----------|---------------|------------------|
| 1 | Order_A | 1 | 1st | Lowest priority (1 < 2 < 3); earliest arrival |
| 2 | Order_B | 1 | 2nd | Priority 1; second arrival of priority 1 |
| 3 | Order_E | 1 | 5th | Priority 1; third arrival of priority 1 |
| 4 | Order_I | 1 | 9th | Priority 1; last arrival of priority 1 |
| 5 | Order_D | 2 | 4th | Priority 2; earliest arrival of priority 2 |
| 6 | [INSERT] | [INSERT] | [INSERT] | [INSERT] |
| 7 | [INSERT] | [INSERT] | [INSERT] | [INSERT] |
| 8 | [INSERT] | [INSERT] | [INSERT] | [INSERT] |
| 9 | [INSERT] | [INSERT] | [INSERT] | [INSERT] |
| 10 | [INSERT] | [INSERT] | [INSERT] | [INSERT] |

**Verification:**
- [ ] All priority 1 orders extracted first (in FIFO order: A, B, E, I)
- [ ] Then all priority 2 orders (in FIFO order by arrival)
- [ ] Then all priority 3 orders (in FIFO order by arrival)
- [ ] Total extracted = 10

**Your Answer:**

[INSERT completed table with all 10 dequeue operations]

---

### Q14c) Time Complexity Analysis [3 marks]

**Requirement:** Prove Big-O complexity for each operation.

| Operation | Big-O | Worst-Case Path | Justification |
|-----------|:-----:|-----------------|---------------|
| `enqueue(order, priority)` | O(log n) | Sift-up from leaf to root | Heap height = ⌈log₂(n)⌉; at most h comparisons |
| `dequeue()` / `extract_min()` | O(log n) | Sift-down from root to leaf | Heap height = ⌈log₂(n)⌉; at most h comparisons |
| `peek()` | O(1) | Direct access to root | Min element always at index 0; no traversal |
| `len()` | O(1) | Return stored counter | Single variable lookup |

**Detailed proof for enqueue (Q14c):**

[INSERT 1–2 paragraphs explaining:
- Worst case: element bubbles from leaf (index n) to root (index 0)
- Number of levels = ⌈log₂(n)⌉
- Each level = 1 comparison + 1 swap
- Total operations = O(log n)]

**Your Answer:**

[INSERT complexity analysis with proofs]

---

## Q15 [8 marks] — Stack (Order Lifecycle + Undo)

**Context:** Each order goes through a lifecycle: Received → Confirmed → Preparing → Dispatched → In Transit → Delivered. A stack tracks status changes, enabling undo operations (e.g., accidental dispatch mark can be rolled back).

**Implementation file:** `task_c/stack.py`

**Test scenario:** 3 orders (A, B, C) with varying paths; Order C is cancelled mid-way.

---

### Q15a) Stack Operations Illustrated [2 marks]

**Requirement:** Show push/pop operations for three orders.

**Order A (normal completion):**

```
Push: Received        → Stack: [Received]
Push: Confirmed       → Stack: [Received, Confirmed]
Push: Preparing       → Stack: [Received, Confirmed, Preparing]
Push: Dispatched      → Stack: [Received, Confirmed, Preparing, Dispatched]
Push: In Transit      → Stack: [Received, Confirmed, Preparing, Dispatched, In Transit]
Push: Delivered       → Stack: [Received, Confirmed, Preparing, Dispatched, In Transit, Delivered]
Final Status (peek()): Delivered
```

**Order B (normal completion):**

```
[INSERT similar push sequence for Order B]
Final Status: Delivered
```

**Order C (cancelled after Preparing):**

```
Push: Received        → Stack: [Received]
Push: Confirmed       → Stack: [Received, Confirmed]
Push: Preparing       → Stack: [Received, Confirmed, Preparing]
Pop (Cancel): Preparing removed → Stack: [Received, Confirmed]
Final Status: Confirmed (order cancelled; reverted to last confirmed state)
```

**Your Answer:**

[INSERT push/pop sequences for all 3 orders]

---

### Q15b) Stack State for 3 Orders [3 marks]

**Requirement:** Terminal output showing stack snapshots at key moments.

**Expected output:**

```
==================================================
Q15: Stack — Order Status Tracking & Undo Operations
==================================================

Order_2847 Status Lifecycle:
Initial Stack: []
Push Received   → [Received]
Push Confirmed  → [Received, Confirmed]
Push Preparing  → [Received, Confirmed, Preparing]
Push Dispatched → [Received, Confirmed, Preparing, Dispatched]
Push In Transit → [Received, Confirmed, Preparing, Dispatched, In Transit]
Push Delivered  → [Received, Confirmed, Preparing, Dispatched, In Transit, Delivered]
Current Status (top of stack): Delivered ✓

Order_2851 Status Lifecycle:
[INSERT]

Order_2855 Status Lifecycle (with cancellation):
Initial Stack: []
Push Received   → [Received]
Push Confirmed  → [Received, Confirmed]
Push Preparing  → [Received, Confirmed, Preparing]
**CANCELLATION TRIGGERED**
Pop Preparing   → [Received, Confirmed]
Current Status (top of stack): Confirmed (Order reverted)

==================================================
```

**Your Answer:**

[INSERT actual terminal output from running task_c/stack.py]

---

### Q15c) Undo Demonstration [3 marks]

**Requirement:** Show an accidental status push and undo operation (pop to recover).

**Scenario:** Rider mistakenly marks Order_2847 as "Dispatched" before it was properly "Confirmed".

**Example output:**

```
==================================================
Q15c: Undo Demonstration — Error Recovery
==================================================

Current Stack (Order_2847): [Received, Confirmed, Preparing]
Current Status: Preparing ✓

MISTAKE: Accidental push of "Dispatched" (rider tapped button twice)
Push Dispatched → [Received, Confirmed, Preparing, Dispatched]
Stack after mistake: [Received, Confirmed, Preparing, Dispatched]
Current Status: Dispatched ✗ (INCORRECT — skipped In Transit check)

UNDO OPERATION: pop() called
Pop Dispatched  → [Received, Confirmed, Preparing]
Stack after undo: [Received, Confirmed, Preparing]
Current Status: Preparing ✓ (RECOVERED)
Message: "Status reverted successfully. Order in Preparing state."

==================================================
```

**Your Answer:**

[INSERT undo demonstration output]

---

## Q16 [10 marks] — Single PQ vs 7 Zone Queues (300 words)

**Context:** WaselX must decide: (1) **Single Global Priority Queue** — all 3,500 orders enter one PQ sorted by priority, or (2) **Zone FIFOs with Pre-sort** — each of 7 zones has its own FIFO, orders pre-sorted by zone, then by priority within zone.

**Marks:** Table [2 marks] + Written analysis [8 marks]

---

### Q16 Comparison Table [2 marks]

| Criterion | Single Global PQ | 7 Zone FIFOs + Pre-sort |
|-----------|:----------------:|:----------------------:|
| **Dispatch fairness** | [INSERT] | [INSERT] |
| **Priority honor** | [INSERT] | [INSERT] |
| **Implementation complexity** | [INSERT] | [INSERT] |
| **Latency (assign order)** | [INSERT] | [INSERT] |
| **Scalability to 15,000 orders** | [INSERT] | [INSERT] |
| **Geographic routing efficiency** | [INSERT] | [INSERT] |

**Row guidance:**

1. **Dispatch fairness:** Does urgent order from Zone 5 jump ahead of standard order from Zone 1?
2. **Priority honor:** Does the system respect priority 1 > 2 > 3 globally?
3. **Implementation complexity:** Single PQ = simpler (one heap); Zone FIFOs = more complex (7 queues, router logic)
4. **Latency (assign order):** Single PQ = O(log n) per dequeue; Zone FIFOs = O(1) per zone
5. **Scalability:** Single PQ = heap with 15,000 elements; Zone FIFOs = 7 queues with ~2,143 each
6. **Geographic routing efficiency:** Zone FIFOs naturally route riders to nearby orders; Single PQ may create cross-zone inefficiency

**Your Answer:**

[INSERT completed comparison table with all 6 criteria filled]

---

### Q16 Written Recommendation [8 marks]

**Word count target:** 300 words (±15%)

**Structure your answer:**

1. **Opening (50 words):** Restate the two options and decision criteria
2. **Single PQ analysis (80 words):** Pros (fairness, priority honor) and cons (latency, geographic inefficiency)
3. **Zone FIFO analysis (80 words):** Pros (latency, geographic efficiency) and cons (priority fairness, regional hoarding)
4. **Recommendation (60 words):** Choose one, justify with metrics
5. **Implementation note (30 words):** Hybrid approach or phased rollout strategy

**Key metrics to include:**
- 3,500 orders/day → ~1 order per 25 seconds
- 7 zones → ~500 orders/zone/day
- 200 riders → ~17.5 orders/rider/day
- Target dispatch latency: <10 seconds per order

**Your Answer:**

[INSERT 300-word written analysis structured as above]

---

## Q17 [10 marks] — CEO Leadership Brief: Priority Queue Proposal

**Context:** WaselX's VIP customers (premium subscribers) are churning due to slow dispatch compared to competitors. The proposal: implement 5-tier priority queue instead of FIFO to guarantee VIP orders dispatch within 30 seconds.

**Role:** Write a leadership brief to the CEO (non-technical audience)  
**Word count:** 300–350 words (strict)  
**Format:** Professional prose, no bullet points, no code, business language  
**Marks:** Business case [3] + Technical explanation [2] + Implementation plan [3] + Rider communication [2]

---

### Business Case Calculation [included in brief]

**Revenue impact of VIP churn:**
- Current VIP customers: ~5% of 3,500 orders/day = 175 VIP orders/day
- Premium price per VIP order: AED 25 (vs standard AED 8)
- Annual VIP revenue: 175 orders/day × 365 days × AED 25 = **AED ~1.6M/year**
- Churn risk: If 20% of VIP orders are lost to competitors = **AED ~320K/year revenue loss**
- Competitor advantage: They offer 30-second dispatch guarantee; we offer FIFO (unpredictable)

**ROI of Priority Queue:**
- Development cost: ~40 developer hours = ~AED 20,000
- Deployment cost: minimal (existing infrastructure)
- Expected revenue recovery: 50% of churn = AED 160,000/year
- **Payback period: <2 months**

---

### CEO Leadership Brief Template

```
TO:       Chief Executive Officer, WaselX Express
FROM:     [INSERT Your Name], DSA & Operations Team
DATE:     [INSERT Date]
SUBJECT:  Priority Queue Initiative — Retain VIP Revenue, Defend Market Position

---

EXECUTIVE SUMMARY
[INSERT 2–3 sentences stating the strategic problem, proposed solution, and financial impact]

Example: "WaselX is losing VIP customer orders to competitors who offer priority dispatch. 
We propose implementing a priority-based order queue to guarantee 30-second dispatch for 
VIP customers. This initiative will recover ~AED 160,000 in annual revenue at minimal cost."

---

BUSINESS PROBLEM
[INSERT 1–2 paragraphs on VIP customer dissatisfaction and revenue risk]

VIP customers (5% of daily volume, 175 orders/day) currently receive the same service as 
standard customers under our FIFO system. Competitors offer priority dispatch guarantees, 
resulting in VIP churn. Analysis shows we're losing [INSERT % or AED value] per month to 
competitor switching.

Revenue at risk: 175 VIP orders × AED 25 premium × 365 days = AED 1.6M annually. 
Even 20% churn (5% of VIP base) = AED 320K annual loss. This is unsustainable in a 
competitive market where delivery speed is a primary service differentiator.

---

PROPOSED SOLUTION
[INSERT 1–2 paragraphs on priority queue system — explain simply, non-technical]

We propose a "service tier" based order queue. Instead of first-come, first-served, 
orders will be routed based on service level: VIP (30-second guarantee), Premium 
(60-second), Standard (2-minute window). The queue automatically prioritizes based on 
customer tier and order arrival time.

Implementation requires no new infrastructure — it's a software optimization to our 
existing dispatch system. Riders will receive orders in the same way (via app notification), 
but order selection will be intelligent rather than sequential.

---

TRANSITION & RISK MITIGATION
[INSERT 1–2 paragraphs on rollout plan and communication strategy]

Rollout plan: Phase 1 (Week 1–2) parallel testing with 10% of daily volume to validate 
system. Phase 2 (Week 3–4) gradual expansion to 50% of volume. Phase 3 (Week 5) full 
deployment. Riders will be trained that they're serving different service commitments, 
not showing favoritism — this is consistent with how airlines and restaurants operate.

Communication to customers: transparency. We'll announce the new tier system to all 
customers, highlighting the option to upgrade for faster dispatch. This positions the 
change as enhancement, not discrimination.

---

FINANCIAL IMPACT
[INSERT 1 paragraph with ROI calculation]

Development cost: AED 20,000  
Expected revenue recovery: AED 160,000/year (50% churn recovery)  
Payback period: <2 months  
Net 5-year impact: AED 800,000 profit (conservative estimate)

---

RECOMMENDATION
Proceed immediately with Phase 1 parallel testing. Success here establishes WaselX as 
a customer-centric delivery leader and drives market differentiation against competitors.

---
```

---

### Your Answer:

[INSERT 300–350 word CEO leadership brief following the structure above]

**Checklist:**
- [ ] 300–350 words (count and verify)
- [ ] No bullet points (professional prose only)
- [ ] No code or technical jargon
- [ ] Business language: "revenue," "churn," "ROI," "competitive advantage"
- [ ] Opening states problem, solution, financial impact in 2–3 sentences
- [ ] Revenue calculation included: AED 1.6M annual VIP revenue, AED 320K churn risk
- [ ] Transition plan: 3 phases with timeline
- [ ] Rider communication strategy: "service commitments not favoritism"
- [ ] Closing: Clear recommendation with action items

---

## Summary: Task C Marks & Status

| Question | Topic | Marks | Completed? |
|----------|-------|-------|:----------:|
| Q12 | Doubly Linked List | 10 | [ ] |
| Q13 | Circular Linked List | 8 | [ ] |
| Q14 | Priority Queue (Min-Heap) | 12 | [ ] |
| Q15 | Stack (Undo Operations) | 8 | [ ] |
| Q16 | Single PQ vs Zone Queues | 10 | [ ] |
| Q17 | CEO Brief (Priority Queue) | 10 | [ ] |
| **Total** | **Order Pipeline & Queues** | **58** | [ ] |

---

## Notes for Team

1. **Code output mandatory:** Q12a, Q13c, Q15c require actual terminal output from running Python code.
2. **Hand-calculations required:** Q14a heap construction and Q14b dequeue order must show step-by-step logic.
3. **Word count enforcement:** Q16 (300 ±15%), Q17 (300–350 exact) — run through word counter before submission.
4. **AI-assisted marking:** If using ChatGPT for CEO brief structure, mark with `[AI-ASSISTED: ...]`.
5. **Professional tone:** Q16 and Q17 are business documents; use formal vocabulary, no contractions, proper citations.

---

## Validation Checklist

Before submitting Task C, verify all items:

### Code & Output
- [ ] Q12a: DLL output shows forward/reverse traversal, insert, delete
- [ ] Q13c: Circular list output shows 8 → 7 rider transitions
- [ ] Q14a: Heap array progression shown for all 10 enqueues
- [ ] Q14b: All 10 dequeues listed in correct priority order
- [ ] Q15b+c: Stack operations and undo demonstration both output

### Analysis & Tables
- [ ] Q12b: 100-word justification (count verified)
- [ ] Q13a+b: 20-row assignment table with all cells filled
- [ ] Q14c: Complexity table with Big-O proofs
- [ ] Q16: 6-row comparison table completed
- [ ] Q16: 300-word analysis written (count verified)

### Leadership Documents
- [ ] Q17: 300–350 word CEO brief (count verified)
- [ ] Q17: Includes AED 1.6M and AED 320K revenue calculations
- [ ] Q17: No bullet points; professional prose only
- [ ] Q17: 3-phase rollout plan mentioned

---

**Document Status:** Answer shell complete; ready for team to fill in [INSERT ...] sections  
**Last Updated:** May 3, 2025  
**Total estimated completion time:** 10–12 hours per team member (implementation + analysis + writing)

---
