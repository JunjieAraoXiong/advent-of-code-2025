# Day 3: Lobby - Step-by-Step Solution

## Problem Summary

Batteries are arranged in banks (one per line). Each battery shows a digit 1-9.
You must select exactly **K batteries** from each bank. The joltage is the number formed by those digits (in order).

- **Part 1:** K = 2 (select 2 batteries)
- **Part 2:** K = 12 (select 12 batteries)

**Goal:** Find the maximum joltage from each bank, sum them all.

---

## Part 1: Select 2 Batteries

### Step-by-Step Approach

#### Step 1: Understand the Problem

Given a string like `"987654321111111"`, pick 2 positions i < j to form the two-digit number `bank[i]bank[j]`.

To maximize a two-digit number AB:
1. Maximize A (tens digit) - most significant
2. Then maximize B (units digit)

#### Step 2: Naive Approach (O(n²))

Try all pairs:
```python
def max_joltage_naive(bank):
    best = 0
    n = len(bank)
    for i in range(n):
        for j in range(i + 1, n):
            joltage = int(bank[i]) * 10 + int(bank[j])
            best = max(best, joltage)
    return best
```

This works but is slow for long strings.

#### Step 3: Optimized Approach (O(n))

**Key insight:** For each position i, we only care about the maximum digit that appears AFTER position i.

Precompute `max_after[i]` = maximum digit in `bank[i+1:]`

```python
def max_joltage(bank):
    n = len(bank)

    # Precompute max_after array (scan right to left)
    max_after = [0] * n
    max_so_far = 0
    for i in range(n - 1, -1, -1):
        max_after[i] = max_so_far
        max_so_far = max(max_so_far, int(bank[i]))

    # Find best joltage
    best = 0
    for i in range(n - 1):
        joltage = int(bank[i]) * 10 + max_after[i]
        best = max(best, joltage)

    return best
```

#### Step 4: Example Walkthrough

Bank: `"811111111111119"`

**Step 1: Compute max_after array**

Scan from right to left:
| Index | Char | max_so_far (before) | max_after[i] | max_so_far (after) |
|-------|------|---------------------|--------------|-------------------|
| 14 | 9 | 0 | 0 | 9 |
| 13 | 1 | 9 | 9 | 9 |
| 12 | 1 | 9 | 9 | 9 |
| ... | 1 | 9 | 9 | 9 |
| 0 | 8 | 9 | 9 | 9 |

**Step 2: Find best joltage**

| Index | Digit | max_after | Joltage |
|-------|-------|-----------|---------|
| 0 | 8 | 9 | 89 |
| 1 | 1 | 9 | 19 |
| ... | 1 | 9 | 19 |

**Best: 89** (pick positions 0 and 14)

---

## Part 2: Select 12 Batteries

### Step-by-Step Approach

#### Step 1: Understand the Greedy Strategy

To maximize a K-digit number, we use a **greedy algorithm**:

1. For the **1st digit**: Pick the largest digit that leaves enough remaining digits (at least K-1 after it)
2. For the **2nd digit**: Pick the largest digit after the 1st pick that leaves K-2 remaining
3. Continue until all K digits are selected

**Why greedy works:** The leftmost digit is most significant. We always want to maximize it first.

#### Step 2: Determine Valid Ranges

For position i (0-indexed), we need K-i more digits after this one.

If bank has n digits and we need to pick K:
- For 1st digit (i=0): can pick from index 0 to n-K (inclusive)
- For 2nd digit (i=1): can pick from after 1st pick to n-K+1
- For i-th digit: can pick from after previous to n-K+i

#### Step 3: Algorithm

```python
def max_joltage_k(bank, k):
    n = len(bank)
    result = []
    start = 0  # Earliest position we can pick from

    for i in range(k):
        # Can pick from start to n-k+i (need k-i-1 more after this)
        end = n - k + i

        # Find max digit in range [start, end]
        best_pos = start
        best_digit = bank[start]
        for pos in range(start, end + 1):
            if bank[pos] > best_digit:
                best_digit = bank[pos]
                best_pos = pos

        result.append(best_digit)
        start = best_pos + 1  # Next pick must be after this one

    return int(''.join(result))
```

#### Step 4: Example Walkthrough

Bank: `"234234234234278"` (length 15), K = 12

We need to skip 3 digits (15 - 12 = 3).

**Iteration 1 (i=0):**
- Range: [0, 3] (indices 0,1,2,3)
- Digits: 2, 3, 4, 2
- Best: **4** at index 2
- start = 3

**Iteration 2 (i=1):**
- Range: [3, 4]
- Digits: 2, 3
- Best: **3** at index 4
- start = 5

**Iteration 3 (i=2):**
- Range: [5, 5]
- Digit: 4
- Best: **4** at index 5
- start = 6

**Continue...**

Final result: `434234234278`

Let's verify: Original is `234234234234278`
- Skip: 2 (index 0), 3 (index 1), 2 (index 3)
- Keep: 4,3,4,2,3,4,2,3,4,2,7,8 → `434234234278` ✓

#### Step 5: Another Example

Bank: `"818181911112111"` (length 15), K = 12

**Greedy selection:**
- i=0: Range [0,3], digits "8181" → pick **8** at 0, start=1
- i=1: Range [1,4], digits "1818" → pick **8** at 2, start=3
- i=2: Range [3,5], digits "181" → pick **8** at 4, start=5
- i=3: Range [5,6], digits "19" → pick **9** at 6, start=7
- i=4: Range [7,7], digit "1" → pick **1** at 7, start=8
- i=5-11: Pick remaining "1112111"

Result: `888911112111` ✓

---

## Visual Representation

```
Bank:    8 1 8 1 8 1 9 1 1 1 1 2 1 1 1
Index:   0 1 2 3 4 5 6 7 8 9 ...

Round 1: [0,1,2,3] → pick 8 at 0
         ^-------^

Round 2: [1,2,3,4] → pick 8 at 2
           ^-------^

Round 3: [3,4,5] → pick 8 at 4
             ^-----^

Round 4: [5,6] → pick 9 at 6
               ^---^

... continue picking remaining digits
```

---

## Time Complexity

### Part 1 (K=2)
- O(n) with precomputation

### Part 2 (K=12)
- Naive: O(K × n) per bank = O(12n)
- Can be optimized to O(n) using segment trees or sparse tables, but O(12n) is fast enough

---

## Summary

| Part | K | Strategy | Example |
|------|---|----------|---------|
| 1 | 2 | Precompute max after each position | "811...119" → 89 |
| 2 | 12 | Greedy: pick largest in valid range, repeat | "234234234234278" → 434234234278 |

## Key Insight

The greedy approach works because:
1. Digits are independent (no dependencies between choices beyond ordering)
2. Leftmost positions are most significant
3. Once we pick a digit, the remaining problem is the same but smaller

## Final Answers (My Input)
- **Part 1:** 17244
- **Part 2:** 171435596092638
