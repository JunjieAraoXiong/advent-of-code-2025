# Day 3: Lobby

## Story

You descend a short staircase, enter the surprisingly vast lobby, and are quickly cleared by the security checkpoint. The elevators are all offline due to an electrical surge. The escalator needs emergency power from batteries.

## Problem

Batteries are arranged into banks (one per line). Each battery has a joltage rating (1-9).

Within each bank, you need to turn on **exactly two batteries**. The joltage produced equals the two-digit number formed by those batteries' digits (in order, no rearranging).

**Goal:** Find the largest possible joltage each bank can produce, then sum them all.

### Example

```
987654321111111
811111111111119
234234234234278
818181911112111
```

- `987654321111111`: Largest is **98** (first two batteries)
- `811111111111119`: Largest is **89** (batteries showing 8 and 9)
- `234234234234278`: Largest is **78** (last two batteries)
- `818181911112111`: Largest is **92**

Total: 98 + 89 + 78 + 92 = **357**

## Part 1

Find the maximum joltage possible from each bank; what is the total output joltage?
