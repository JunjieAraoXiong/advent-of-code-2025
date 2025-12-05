# Day 4: Printing Department

## Story

You ride the escalator down to the printing department. They have lots of large rolls of paper everywhere. The Elves want to break through a wall to the cafeteria, but their forklifts are busy moving paper rolls.

## Problem

The rolls of paper (`@`) are arranged on a grid. Forklifts can only access a roll if there are **fewer than 4 rolls** in the 8 adjacent positions.

### Example

```
..@@.@@@@.
@@@.@.@.@@
@@@@@.@.@@
@.@@@@..@.
@@.@@@@.@@
.@@@@@@@.@
.@.@.@.@@@
@.@@@.@@@@
.@@@@@@@@.
@.@.@@@.@.
```

Accessible rolls (marked with `x`):

```
..xx.xx@x.
x@@.@.@.@@
@@@@@.x.@@
@.@@@@..@.
x@.@@@@.@x
.@@@@@@@.@
.@.@.@.@@@
x.@@@.@@@@
.@@@@@@@@.
x.x.@@@.x.
```

**Answer: 13** accessible rolls

## Part 1

Count how many rolls of paper can be accessed by a forklift.
