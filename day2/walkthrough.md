# Day 2: Gift Shop - Step-by-Step Solution

## Problem Summary

You're given ranges of product IDs. An ID is **invalid** if it consists of a digit sequence repeated multiple times.

- **Part 1:** Pattern repeated **exactly twice** (e.g., `55`, `6464`, `123123`)
- **Part 2:** Pattern repeated **at least twice** (e.g., `111`, `123123123`, `1212121212`)

**Goal:** Find all invalid IDs in the given ranges and sum them.

---

## Part 1: Pattern Repeated Exactly Twice

### Step-by-Step Approach

#### Step 1: Understand Invalid IDs

An ID is invalid if its string representation is the same pattern repeated twice:
- `55` = "5" + "5" ✓
- `6464` = "64" + "64" ✓
- `123123` = "123" + "123" ✓
- `123` = odd length, can't be split evenly ✗
- `1234` = "12" ≠ "34" ✗

**Key observation:** The number must have an even number of digits, and the first half must equal the second half.

#### Step 2: Check if a Number is Invalid

```python
def is_invalid_part1(n):
    s = str(n)
    length = len(s)

    # Must have even number of digits
    if length % 2 != 0:
        return False

    half = length // 2
    return s[:half] == s[half:]
```

#### Step 3: Efficient Generation (Don't Iterate Every Number!)

**Problem:** Ranges can be huge (e.g., `1-10000000000`). We can't check every number.

**Solution:** Generate all possible invalid IDs and check if they fall in the range.

Invalid IDs with 2k digits are formed by repeating a k-digit number:
- 2 digits: 11, 22, 33, ..., 99 (repeat 1-9)
- 4 digits: 1010, 1111, ..., 9999 (repeat 10-99)
- 6 digits: 100100, 100101, ..., 999999 (repeat 100-999)

```python
def find_invalid_ids_part1(start, end):
    invalid_ids = []
    end_digits = len(str(end))

    # Check lengths 2, 4, 6, ...
    for total_digits in range(2, end_digits + 2, 2):
        half_digits = total_digits // 2

        # Generate all numbers with half_digits digits (no leading zeros)
        if half_digits == 1:
            min_half = 1  # 1-9
        else:
            min_half = 10 ** (half_digits - 1)  # 10, 100, 1000, ...

        max_half = 10 ** half_digits - 1  # 9, 99, 999, ...

        for half_num in range(min_half, max_half + 1):
            half_str = str(half_num)
            invalid_id = int(half_str + half_str)  # Repeat twice

            if start <= invalid_id <= end:
                invalid_ids.append(invalid_id)

    return invalid_ids
```

#### Step 4: Example Walkthrough

Range: `11-22`
- Check 2-digit invalid IDs: 11, 22, 33, ..., 99
- In range [11, 22]: **11** and **22**
- Sum: 11 + 22 = 33

Range: `95-115`
- 2-digit invalid IDs in range: **99**
- 4-digit invalid IDs: 1010, 1111, ... (all > 115)
- Sum: 99

Range: `998-1012`
- 2-digit: none in range
- 4-digit in range: **1010** (1111 > 1012)
- Sum: 1010

---

## Part 2: Pattern Repeated At Least Twice

### Step-by-Step Approach

#### Step 1: Understand the New Rule

Now patterns can repeat 2, 3, 4, ... times:
- `111` = "1" × 3 ✓
- `123123123` = "123" × 3 ✓
- `1212121212` = "12" × 5 ✓
- `1111` = "1" × 4 or "11" × 2 ✓ (either works)

#### Step 2: Check if a Number is Invalid

```python
def is_invalid_part2(n):
    s = str(n)
    length = len(s)

    # Try all possible pattern lengths
    for pattern_len in range(1, length // 2 + 1):
        # Pattern length must divide total length evenly
        if length % pattern_len != 0:
            continue

        pattern = s[:pattern_len]
        repetitions = length // pattern_len

        # Check if string equals pattern repeated
        if pattern * repetitions == s:
            return True

    return False
```

#### Step 3: Generate All Invalid IDs

For each total digit length, try all valid pattern lengths:

```python
def find_invalid_ids_part2(start, end):
    invalid_ids = set()  # Use set to avoid duplicates
    end_digits = len(str(end))

    for total_digits in range(2, end_digits + 2):
        for pattern_len in range(1, total_digits // 2 + 1):
            # Pattern length must divide total length
            if total_digits % pattern_len != 0:
                continue

            repetitions = total_digits // pattern_len

            # Generate all patterns (no leading zeros)
            if pattern_len == 1:
                min_pattern = 1
            else:
                min_pattern = 10 ** (pattern_len - 1)
            max_pattern = 10 ** pattern_len - 1

            for pattern_num in range(min_pattern, max_pattern + 1):
                pattern_str = str(pattern_num)
                invalid_id = int(pattern_str * repetitions)

                if start <= invalid_id <= end:
                    invalid_ids.add(invalid_id)

    return list(invalid_ids)
```

**Why use a set?** Numbers like `1111` can be generated multiple ways:
- "1" × 4
- "11" × 2

We only want to count it once.

#### Step 4: Example Walkthrough

Range: `95-115`
- Part 1 found: 99
- Part 2 also finds: **111** ("1" × 3)
- Sum: 99 + 111 = 210

Range: `565653-565659`
- Part 1: nothing (no 6-digit XX pattern in range)
- Part 2: **565656** = "56" × 3
- Sum: 565656

Range: `824824821-824824827`
- Part 1: nothing
- Part 2: **824824824** = "824" × 3
- Sum: 824824824

---

## Algorithm Complexity

### Part 1
- For a range up to N digits, we generate at most O(10^(N/2)) invalid IDs
- Much faster than iterating through all numbers in the range

### Part 2
- For each total length L, we try pattern lengths 1, 2, ..., L/2
- For each pattern length k, we generate 9 × 10^(k-1) patterns
- Still much faster than brute force

---

## Summary Table

| Part | Invalid ID Definition | Examples | Key Insight |
|------|----------------------|----------|-------------|
| 1 | Pattern × 2 | 55, 6464, 123123 | Even length, first half = second half |
| 2 | Pattern × 2+ | 111, 1212, 123123123 | Check all divisors of length |

## Final Answers (My Input)
- **Part 1:** 44854383294
- **Part 2:** 55647141923
