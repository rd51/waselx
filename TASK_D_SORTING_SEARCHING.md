# Task Area D: Sorting, Searching & Divide and Conquer

**Program:** MAIB - Data Structures & Algorithms Final Project  
**Section:** Task D - Sorting, Searching & Divide and Conquer  
**Total Marks:** Q18 (12) + Q19 (10) + Q20 (10) + Q21 (8) + Q22 (10) = **50 marks**  
**Status:** [PLACEHOLDER: In Progress / Completed]

---

## Q18 [12 marks] - Merge Sort + Quick Sort (15 orders)

**Dataset:** `(JLT,3),(Deira,1),(Marina,4),(JLT,1),(Deira,2),(Marina,2),(Silicon,5),(Deira,3),(JLT,2),(Marina,1),(Silicon,1),(Deira,4),(Silicon,3),(JLT,5),(Marina,3)`

**Implementation file:** `task_d/sorting.py`

**Sorting rule:** Sort by zone alphabetically, then by priority ascending within the same zone.

---

### Q18a) Merge Sort - divide and merge steps (first 3 levels) [6 marks]

**Requirement:** Show the first three levels of recursive division and at least three merge operations with a comparison log.

**Level 1 - Initial divide:**

```text
Left half:  [(JLT,3),(Deira,1),(Marina,4),(JLT,1),(Deira,2),(Marina,2),(Silicon,5),(Deira,3)]
Right half: [(JLT,2),(Marina,1),(Silicon,1),(Deira,4),(Silicon,3),(JLT,5),(Marina,3)]
```

**Level 2 - Divide left half again:**

```text
[INSERT split of the left half into two subarrays of size 4]
```

**Level 3 - Divide further:**

```text
[INSERT split of the level 2 subarrays into size 2 or size 1 subarrays]
```

**Merge steps (show at least 3 merge operations with comparison log):**

```text
[INSERT terminal output from merge steps in sorting.py]
```

**Final sorted output (Merge Sort):**

```text
[Deira,1], [Deira,2], [Deira,3], [Deira,4], [JLT,1], [JLT,2], [JLT,3], [JLT,5], [Marina,1], [Marina,2], [Marina,3], [Marina,4], [Silicon,1], [Silicon,3], [Silicon,5]
```

**Your Answer:**

[INSERT merge-sort divide/merge trace and final sorted output]

**Support checklist:**
- [ ] Level 2 split shown for both halves
- [ ] Level 3 split shown clearly
- [ ] At least 3 merge operations logged
- [ ] Comparison count mentioned in the merge log
- [ ] Final output matches the required sort order

---

### Q18b) Quick Sort - partitioning steps (first 2 levels) [4 marks]

**Requirement:** Show the first two partitioning levels using the last element as the pivot.

**Level 1 - pivot = (Marina,3) (last element):**

```text
Before partition: [(JLT,3),(Deira,1),(Marina,4),(JLT,1),(Deira,2),(Marina,2),(Silicon,5),(Deira,3),(JLT,2),(Marina,1),(Silicon,1),(Deira,4),(Silicon,3),(JLT,5),(Marina,3)]
After partition:  [elements < pivot] | pivot | [elements > pivot]
Pivot final index: [INSERT]
```

**Level 2 - partition left subarray:**

```text
[INSERT partition trace for the left subarray after level 1]
```

**Final sorted output (Quick Sort):**

```text
[INSERT final quick sort output - must match merge sort output exactly]
```

**Your Answer:**

[INSERT quick-sort partition trace and final sorted output]

**Support checklist:**
- [ ] Pivot choice explicitly shown
- [ ] Level 1 partition result shown
- [ ] Level 2 partition result shown
- [ ] Final output matches Merge Sort exactly

---

### Q18c) Comparison Count [2 marks]

**Requirement:** Count total comparisons for each algorithm and state which is more efficient for this partially structured dataset.

| Algorithm | Total Comparisons | More Efficient? |
|-----------|------------------:|-----------------|
| Merge Sort | [INSERT] | [INSERT] |
| Quick Sort | [INSERT] | [INSERT] |

**Written explanation:**

[INSERT 2-3 sentence explanation covering:]
- [INSERT] why one algorithm performs fewer comparisons on this dataset
- [INSERT] whether the data being partially structured helps or hurts either algorithm
- [INSERT] why stability matters when sorting by zone and priority

---

## Q19 [10 marks] - Binary Search vs Linear Search (Order ID 10347)

**Context:** Search for order ID 10347 in a sorted list of 1,000 order IDs.

**Implementation file:** `task_d/searching.py`

---

### Q19a) Binary Search steps [4 marks]

**Requirement:** Show the search steps in table form until 10347 is found.

| Step | low | mid | high | arr[mid] | Action |
|------|----:|----:|-----:|---------:|--------|
| 1 | 0 | 499 | 999 | 10500 | Go left |
| 2 | [INSERT] | [INSERT] | [INSERT] | [INSERT] | [INSERT] |
| 3 | [INSERT] | [INSERT] | [INSERT] | [INSERT] | [INSERT] |
| 4 | [INSERT] | [INSERT] | [INSERT] | [INSERT] | [INSERT] |
| 5 | [INSERT] | [INSERT] | [INSERT] | 10347 | Found |

**Total comparisons (Binary Search):** [INSERT]

**Your Answer:**

[INSERT completed binary-search trace with all rows]

**Support checklist:**
- [ ] Search range halves correctly each step
- [ ] Target found in a sorted array
- [ ] Total comparison count stated clearly

---

### Q19b) Linear Search [2 marks]

**Requirement:** State the total comparisons required by linear search.

**Total comparisons to reach 10347:** [INSERT - 10347 - 10001 + 1 = 347 comparisons]

**Your Answer:**

[INSERT one short paragraph explaining why linear search is slower here]

---

### Q19c) Daily comparison calculation (500 calls/day) [4 marks]

| Algorithm | Comparisons per call | Total per day (500 calls) |
|-----------|---------------------:|--------------------------:|
| Binary Search | [INSERT] | [INSERT] |
| Linear Search | 347 (avg for 10347) | [INSERT] |
| Percentage improvement | - | [INSERT]% fewer comparisons |

**Your Answer:**

[INSERT 2-3 sentence calculation and explanation of the daily savings]

**Support checklist:**
- [ ] Binary search total comparisons filled
- [ ] Linear search daily total calculated
- [ ] Percentage improvement shown

---

## Q20 [10 marks] - Divide and Conquer Peak Hour Finder (6,000 orders)

**Context:** Find the peak hour for order volume using divide and conquer across 24 hourly buckets.

**Implementation file:** `task_d/searching.py` (or the peak-hour helper used in the project)

---

### Q20a) Divide-and-conquer approach - recursive call trace [4 marks]

**Requirement:** Insert the recursive trace showing how the algorithm narrows down the busiest hour.

```text
[INSERT terminal output from task_d/searching.py find_peak_hour_dc()]
Expected format:
D&C(hour 0-23): left half total=[X], right half total=[Y] -> recurse right
D&C(hour 12-23): left half total=[X], right half total=[Y] -> recurse left
...
Peak hour found: Hour [X] with [Y] orders
```

**Your Answer:**

[INSERT actual recursive trace and final peak-hour result]

**Support checklist:**
- [ ] Recursive calls shown clearly
- [ ] Branch choice explained at each level
- [ ] Final peak hour reported

---

### Q20b) Complexity comparison [2 marks]

| Approach | Time Complexity | Space Complexity |
|----------|----------------|------------------|
| Divide & Conquer (find 1 peak) | O(log 24) = O(1) effectively | O(log 24) call stack |
| Linear scan | O(24) | O(1) |

**Note:** For 24 fixed hours, both are effectively O(1). The divide-and-conquer advantage becomes clearer at larger scales such as minute-level or second-level buckets.

**Your Answer:**

[INSERT brief comparison paragraph]

---

### Q20c) Top 3 peak hours [4 marks]

| Rank | Hour | Orders | % of Daily Volume |
|------|-----:|-------:|------------------:|
| 1 | [INSERT] | [INSERT] | [INSERT]% |
| 2 | [INSERT] | [INSERT] | [INSERT]% |
| 3 | [INSERT] | [INSERT] | [INSERT]% |

**Efficiency discussion:**

[INSERT 100-word explanation discussing whether D&C is efficient for top-3 discovery and whether multiple runs or a modified approach is needed]

**Support checklist:**
- [ ] Top 3 hours listed
- [ ] Percentages sum sensibly
- [ ] Discussion addresses repeated D&C vs modified strategy

---

## Q21 [8 marks] - Merge Sort vs Quick Sort for 50,000 Records

**Context:** Choose the best algorithm for a nightly batch job that sorts 50,000 records, where 60% of the data is already partially sorted.

**Required length:** 250 words (approx.)

---

### Q21 Written Recommendation [8 marks]

**Your Answer:**

[INSERT 250-word recommendation covering:]
- Merge Sort: O(n log n) guaranteed, stable, uses O(n) extra memory
- Quick Sort: average O(n log n) but worst-case O(n^2), especially risky for partially sorted data with a naive pivot
- Stability: preserving chronological order for equal zones/priority values is important for audit trails
- Recommendation: Merge Sort for a nightly offline batch job because stability and guaranteed runtime matter more than in-place memory savings

**Suggested structure:**
1. State the job requirement and compare the two algorithms.
2. Explain why stability matters for WaselX records.
3. Explain the worst-case risk of Quick Sort on partially sorted input.
4. End with a clear recommendation for Merge Sort.

**Support checklist:**
- [ ] Around 250 words
- [ ] Stability explained
- [ ] Worst-case risk explained
- [ ] Clear final recommendation stated

---

## Q22 [10 marks] - Sort Performance Benchmark

**Figure 3:** Merge Sort vs Quick Sort execution time  
**Output file:** `outputs/sort_benchmark.png`

*Figure 3: Sort execution time (ms) for Merge Sort and Quick Sort across 5 dataset sizes (100-10,000 random integers). Each measurement averaged over 3 runs. Generated by `task_d/sort_benchmark.py`.*

---

### Q22 Results Table [6 marks]

| Dataset Size | Merge Sort (ms) | Quick Sort (ms) | Faster Algorithm |
|-------------|----------------:|----------------:|------------------|
| 100 | [INSERT] | [INSERT] | [INSERT] |
| 500 | [INSERT] | [INSERT] | [INSERT] |
| 1,000 | [INSERT] | [INSERT] | [INSERT] |
| 5,000 | [INSERT] | [INSERT] | [INSERT] |
| 10,000 | [INSERT] | [INSERT] | [INSERT] |

**Your Answer:**

[INSERT benchmark table values from the generated figure or benchmark script output]

**Support checklist:**
- [ ] All 5 dataset sizes filled
- [ ] Faster algorithm selected in each row
- [ ] Results match the plotted figure

---

### Q22 Benchmark Analysis [4 marks]

**Requirement:** Explain the observed time trends in the benchmark graph.

**Your Answer:**

[INSERT 120-150 word analysis covering:]
- [INSERT] how runtime changes as dataset size grows
- [INSERT] whether Merge Sort or Quick Sort is faster at small vs large sizes
- [INSERT] whether the benchmark matches the theoretical complexity expectations
- [INSERT] whether the data distribution appears to affect Quick Sort

---

## Summary: Task D Marks & Status

| Question | Topic | Marks | Completed? |
|----------|-------|-------|:----------:|
| Q18 | Merge Sort + Quick Sort | 12 | [ ] |
| Q19 | Binary Search vs Linear Search | 10 | [ ] |
| Q20 | Divide and Conquer Peak Hour Finder | 10 | [ ] |
| Q21 | Merge Sort vs Quick Sort Recommendation | 8 | [ ] |
| Q22 | Sort Performance Benchmark | 10 | [ ] |
| **Total** | **Sorting, Searching & Divide and Conquer** | **50** | [ ] |

---

## Notes for Team

1. **Code output required:** Q18a, Q18b, Q19a, Q20a, and Q22 need terminal output or figure evidence.
2. **Sorting order must match exactly:** Zone alphabetically, then priority ascending within each zone.
3. **Search steps should be explicit:** Show each low/mid/high update for binary search.
4. **Word count matters:** Q21 should be close to 250 words, not a short paragraph.
5. **Benchmark figure should be saved correctly:** Use the path `outputs/sort_benchmark.png`.

---

## Validation Checklist

Before submitting Task D, verify all items:

### Code & Output
- [ ] Q18a: Merge sort divide/merge trace shown
- [ ] Q18b: Quick sort partition trace shown
- [ ] Q19a: Binary search step table completed
- [ ] Q20a: Peak hour recursive trace included
- [ ] Q22: Benchmark figure referenced and results table filled

### Analysis & Tables
- [ ] Q18c: Comparison counts completed
- [ ] Q19b: Linear search comparison stated
- [ ] Q19c: Daily comparison savings calculated
- [ ] Q20b: Complexity table completed
- [ ] Q20c: Top 3 peak hours listed
- [ ] Q21: Recommendation around 250 words

---

**Document Status:** Answer shell complete; ready for team to fill in all [INSERT ...] sections  
**Last Updated:** May 3, 2026  
**Total estimated completion time:** 8-10 hours per team member
