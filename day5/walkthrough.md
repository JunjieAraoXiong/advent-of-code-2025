# Day 5: Cafeteria - Step-by-Step Solution

## Problem Summary

The kitchen has a database with:
1. Fresh ingredient ID ranges (e.g., `3-5` means IDs 3, 4, 5 are fresh)
2. A list of available ingredient IDs to check

Ranges are **inclusive** and can **overlap**. An ingredient is fresh if it falls into ANY range.

- **Part 1:** How many of the available ingredient IDs are fresh?
- **Part 2:** How many total unique IDs are considered fresh by all ranges?

---

## Part 1: Check Available Ingredients

### Step-by-Step Approach

#### Step 1: Parse the Input

The input has two sections separated by a blank line:
- Section 1: Ranges (one per line, format `start-end`)
- Section 2: Ingredient IDs to check (one per line)

```python
def parse_input(input_file):
    with open(input_file, 'r') as f:
        content = f.read().strip()

    parts = content.split('\n\n')

    # Parse ranges
    ranges = []
    for line in parts[0].split('\n'):
        start, end = line.split('-')
        ranges.append((int(start), int(end)))

    # Parse ingredient IDs
    ingredients = [int(line) for line in parts[1].split('\n')]

    return ranges, ingredients
```

#### Step 2: Merge Overlapping Ranges

To efficiently check if an ID is in any range, we first merge overlapping ranges.

**Why merge?**
- Reduces the number of ranges to check
- Enables binary search for O(log N) lookups

**Merge Algorithm:**
1. Sort ranges by start value
2. For each range, check if it overlaps with the last merged range
3. If overlap: extend the last range
4. If no overlap: add as new range

```python
def merge_ranges(ranges):
    if not ranges:
        return []

    sorted_ranges = sorted(ranges)
    merged = [sorted_ranges[0]]

    for start, end in sorted_ranges[1:]:
        last_start, last_end = merged[-1]

        # Overlap or adjacent? (start <= last_end + 1)
        if start <= last_end + 1:
            merged[-1] = (last_start, max(last_end, end))
        else:
            merged.append((start, end))

    return merged
```

**Example:**
```
Original: [(3,5), (10,14), (16,20), (12,18)]
Sorted:   [(3,5), (10,14), (12,18), (16,20)]

Step 1: merged = [(3,5)]
Step 2: 10 > 5+1, no overlap → merged = [(3,5), (10,14)]
Step 3: 12 <= 14+1, overlap → merged = [(3,5), (10,18)]
Step 4: 16 <= 18+1, overlap → merged = [(3,5), (10,20)]
```

#### Step 3: Binary Search for Freshness Check

With merged, sorted ranges, we can use binary search:

```python
def is_fresh_binary_search(ingredient_id, merged_ranges):
    left, right = 0, len(merged_ranges) - 1

    while left <= right:
        mid = (left + right) // 2
        start, end = merged_ranges[mid]

        if start <= ingredient_id <= end:
            return True
        elif ingredient_id < start:
            right = mid - 1
        else:
            left = mid + 1

    return False
```

#### Step 4: Count Fresh Ingredients

```python
def solve_part1(input_file):
    ranges, ingredients = parse_input(input_file)
    merged = merge_ranges(ranges)

    fresh_count = 0
    for ingredient_id in ingredients:
        if is_fresh_binary_search(ingredient_id, merged):
            fresh_count += 1

    return fresh_count
```

#### Step 5: Example Walkthrough

Ranges: `3-5, 10-14, 16-20, 12-18`
Merged: `3-5, 10-20`

| ID | Check | Result |
|----|-------|--------|
| 1 | 1 < 3, not in 3-5; 1 < 10, not in 10-20 | spoiled |
| 5 | 3 <= 5 <= 5 ✓ | **fresh** |
| 8 | 8 > 5, not in 3-5; 8 < 10, not in 10-20 | spoiled |
| 11 | 10 <= 11 <= 20 ✓ | **fresh** |
| 17 | 10 <= 17 <= 20 ✓ | **fresh** |
| 32 | 32 > 20, not in any range | spoiled |

**Answer: 3** fresh ingredients

---

## Part 2: Count All Fresh IDs

### Step-by-Step Approach

#### Step 1: Understand the Problem

We need to count the **total number of unique IDs** covered by all ranges.

Key insight: After merging, each merged range covers `end - start + 1` unique IDs.

#### Step 2: Simple Formula

```python
def solve_part2(input_file):
    ranges, _ = parse_input(input_file)
    merged = merge_ranges(ranges)

    total_ids = 0
    for start, end in merged:
        total_ids += end - start + 1

    return total_ids
```

#### Step 3: Why Merging is Essential

Without merging, overlapping IDs would be counted multiple times:

```
Ranges: 10-14, 12-18

Without merge:
  10-14: 5 IDs (10,11,12,13,14)
  12-18: 7 IDs (12,13,14,15,16,17,18)
  Total: 12 ❌ (12,13,14 counted twice!)

With merge:
  10-18: 9 IDs (10,11,12,13,14,15,16,17,18)
  Total: 9 ✅
```

#### Step 4: Example Walkthrough

Ranges: `3-5, 10-14, 16-20, 12-18`
Merged: `[(3,5), (10,20)]`

| Range | Calculation | IDs |
|-------|-------------|-----|
| 3-5 | 5 - 3 + 1 | 3 |
| 10-20 | 20 - 10 + 1 | 11 |
| **Total** | | **14** |

Fresh IDs: 3, 4, 5, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20

---

## Algorithm Complexity

### Part 1

| Step | Time Complexity |
|------|-----------------|
| Parse input | O(N + M) |
| Sort ranges | O(N log N) |
| Merge ranges | O(N) |
| Check each ID | O(M log N) |
| **Total** | **O(N log N + M log N)** |

Where N = number of ranges, M = number of ingredients to check

### Part 2

| Step | Time Complexity |
|------|-----------------|
| Parse input | O(N) |
| Sort & merge | O(N log N) |
| Sum ranges | O(N) |
| **Total** | **O(N log N)** |

---

## Key Insights

1. **Range Merging** is the core technique - eliminates overlaps for accurate counting
2. **Sorting first** makes merging simple - just compare with the last merged range
3. **Adjacent ranges** (e.g., 3-5 and 6-10) should also be merged → use `start <= last_end + 1`
4. **Binary search** makes Part 1 efficient for many queries

---

## Common Pitfalls

1. **Off-by-one errors**: Ranges are inclusive, so size = `end - start + 1`, not `end - start`
2. **Forgetting to merge**: Without merging, Part 2 overcounts overlapping IDs
3. **Adjacent ranges**: `1-5` and `6-10` should merge to `1-10`

---

## Summary

| Part | Question | Method | Formula |
|------|----------|--------|---------|
| 1 | Is specific ID fresh? | Merge + Binary Search | - |
| 2 | Total fresh IDs? | Merge + Sum | `Σ(end - start + 1)` |

## Final Answers (My Input)
- **Part 1:** 679
- **Part 2:** 358155203664116
