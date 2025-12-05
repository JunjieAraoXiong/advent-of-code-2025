# Day 5: Cafeteria

## Story

As the forklifts break through the wall, the Elves are delighted to discover that there was a cafeteria on the other side after all. The kitchen Elves are struggling with their new inventory management system - they can't figure out which ingredients are fresh and which are spoiled.

## Problem

The database contains:
1. A list of fresh ingredient ID ranges (e.g., `3-5` means IDs 3, 4, 5 are fresh)
2. A blank line separator
3. A list of available ingredient IDs to check

Ranges are inclusive and can overlap. An ingredient is fresh if it falls into ANY range.

### Example

```
3-5
10-14
16-20
12-18

1
5
8
11
17
32
```

Analysis:
- ID 1: spoiled (not in any range)
- ID 5: fresh (in range 3-5)
- ID 8: spoiled
- ID 11: fresh (in range 10-14)
- ID 17: fresh (in range 16-20 AND 12-18)
- ID 32: spoiled

**Answer: 3** fresh ingredients

## Part 1

How many of the available ingredient IDs are fresh?
