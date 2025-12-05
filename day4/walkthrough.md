# Day 4: Printing Department - Step-by-Step Solution

## Problem Summary

Rolls of paper (`@`) are arranged on a grid. A forklift can access a roll if there are **fewer than 4 rolls** in the 8 adjacent positions (up, down, left, right, and 4 diagonals).

**Goal:** Count how many rolls of paper can be accessed by a forklift.

---

## Part 1: Count Accessible Rolls

### Step-by-Step Approach

#### Step 1: Understand the Grid and Adjacency

The grid is a 2D array of characters:
- `@` = roll of paper
- `.` = empty space

For each cell, there are 8 adjacent positions:
```
[NW] [N] [NE]
[W]  [X] [E]
[SW] [S] [SE]
```

Where X is the current position.

#### Step 2: Define the 8 Directions

We represent directions as (row_delta, col_delta) pairs:

```python
directions = [
    (-1, -1), (-1, 0), (-1, 1),  # up-left, up, up-right
    (0, -1),           (0, 1),   # left, right
    (1, -1),  (1, 0),  (1, 1)    # down-left, down, down-right
]
```

#### Step 3: Count Adjacent Rolls

For a given position (row, col), count how many of its 8 neighbors contain `@`:

```python
def count_adjacent_rolls(grid, row, col):
    rows = len(grid)
    cols = len(grid[0])

    count = 0
    for dr, dc in directions:
        new_row, new_col = row + dr, col + dc
        # Check bounds (don't go outside the grid)
        if 0 <= new_row < rows and 0 <= new_col < cols:
            if grid[new_row][new_col] == '@':
                count += 1

    return count
```

#### Step 4: Check Each Roll

Iterate through every cell in the grid:
1. If the cell contains `@` (a roll)
2. Count its adjacent rolls
3. If count < 4, it's accessible

```python
def solve_part1(grid):
    accessible_count = 0

    for row in range(len(grid)):
        for col in range(len(grid[0])):
            if grid[row][col] == '@':
                adjacent = count_adjacent_rolls(grid, row, col)
                if adjacent < 4:
                    accessible_count += 1

    return accessible_count
```

#### Step 5: Example Walkthrough

Grid:
```
..@@.@@@@.   (row 0)
@@@.@.@.@@   (row 1)
@@@@@.@.@@   (row 2)
@.@@@@..@.   (row 3)
@@.@@@@.@@   (row 4)
.@@@@@@@.@   (row 5)
.@.@.@.@@@   (row 6)
@.@@@.@@@@   (row 7)
.@@@@@@@@.   (row 8)
@.@.@@@.@.   (row 9)
```

Let's check a few positions:

**Position (0, 2) - the first `@` in row 0:**
```
Neighbors:
  . @ .     (row -1: out of bounds, counts as 0)
  . @ @     (row 0: positions 1,3)
  @ @ .     (row 1: positions 1,2,3)

Adjacent rolls: @(0,3) + @(1,1) + @(1,2) = 3
3 < 4, so ACCESSIBLE ✓
```

**Position (1, 1) - middle of the `@@@` cluster:**
```
Neighbors:
  . @ @     (row 0)
  @ X @     (row 1)
  @ @ @     (row 2)

Adjacent rolls: 2 + 2 + 3 = 7
7 >= 4, so NOT accessible ✗
```

**Position (0, 8) - near the edge:**
```
Neighbors:
  . . .     (row -1: out of bounds)
  @ X .     (row 0: position 7)
  . @ @     (row 1: positions 7,8,9)

Adjacent rolls: @(0,7) + @(1,8) + @(1,9) = 3
3 < 4, so ACCESSIBLE ✓
```

All 13 accessible positions:
| Row | Col | Adjacent Count |
|-----|-----|----------------|
| 0 | 2 | 3 |
| 0 | 3 | 3 |
| 0 | 5 | 3 |
| 0 | 6 | 3 |
| 0 | 8 | 3 |
| 1 | 0 | 2 |
| 2 | 6 | 3 |
| 4 | 0 | 2 |
| 4 | 9 | 3 |
| 7 | 0 | 2 |
| 9 | 0 | 1 |
| 9 | 2 | 3 |
| 9 | 8 | 3 |

**Answer: 13** accessible rolls

---

## Edge Cases to Consider

1. **Corner positions:** Only 3 neighbors
   ```
   X @ .
   @ @ .
   . . .
   ```

2. **Edge positions:** Only 5 neighbors (sides)
   ```
   . X @
   . @ @
   . . .
   ```

3. **Rolls at grid boundaries:** Some directions are out of bounds and count as 0

The solution handles these automatically by checking bounds before accessing the grid.

---

## Algorithm Complexity

### Time Complexity
- O(R × C) where R = rows and C = columns
- We visit each cell once
- For each cell, we check at most 8 neighbors (constant)
- Total: O(R × C)

### Space Complexity
- O(R × C) for storing the grid
- O(1) additional space for counting

---

## Visual Representation

```
Original Grid:          Accessible (x = accessible roll):
..@@.@@@@.              ..xx.xx@x.
@@@.@.@.@@              x@@.@.@.@@
@@@@@.@.@@              @@@@@.x.@@
@.@@@@..@.              @.@@@@..@.
@@.@@@@.@@              x@.@@@@.@x
.@@@@@@@.@              .@@@@@@@.@
.@.@.@.@@@              .@.@.@.@@@
@.@@@.@@@@              x.@@@.@@@@
.@@@@@@@@.              .@@@@@@@@.
@.@.@@@.@.              x.x.@@@.x.
```

Rolls that are deeply embedded in clusters of other rolls (4+ neighbors) cannot be accessed.
Rolls on edges, corners, or with gaps nearby are accessible.

---

## Summary (Part 1)

| Step | Action |
|------|--------|
| 1 | Parse grid into 2D array |
| 2 | For each cell with `@` |
| 3 | Count adjacent `@` in 8 directions |
| 4 | If count < 4, increment accessible count |
| 5 | Return total accessible count |

---

## Part 2: Remove All Accessible Rolls Repeatedly

### Step-by-Step Approach

#### Step 1: Understand the Problem

Once a roll is removed, neighboring rolls may become accessible (they now have fewer adjacent rolls). We need to:
1. Find all currently accessible rolls
2. Remove them all
3. Repeat until no more rolls are accessible
4. Count the total number of rolls removed

#### Step 2: Simulation Algorithm

```python
def solve_part2(grid):
    # Convert to mutable grid
    grid = [list(row) for row in grid]
    total_removed = 0

    while True:
        # Find all accessible rolls
        accessible = find_accessible_rolls(grid)

        if not accessible:
            break  # No more rolls can be removed

        # Remove all accessible rolls
        for row, col in accessible:
            grid[row][col] = '.'

        total_removed += len(accessible)

    return total_removed
```

#### Step 3: Example Walkthrough

Starting grid has 57 rolls total.

| Iteration | Rolls Removed | Running Total | Remaining |
|-----------|---------------|---------------|-----------|
| 1 | 13 | 13 | 44 |
| 2 | 12 | 25 | 32 |
| 3 | 7 | 32 | 25 |
| 4 | 5 | 37 | 20 |
| 5 | 2 | 39 | 18 |
| 6 | 1 | 40 | 17 |
| 7 | 1 | 41 | 16 |
| 8 | 1 | 42 | 15 |
| 9 | 1 | 43 | 14 |
| Stop | 0 | **43** | 14 |

The remaining 14 rolls form a stable cluster where every roll has 4+ neighbors.

#### Step 4: Why Rolls Become Inaccessible

A roll remains inaccessible if it's surrounded by 4+ other rolls. Dense clusters in the center tend to be stable because:
- Interior rolls have many neighbors
- When edge rolls are removed, interior rolls may still have 4+ neighbors

Example of a stable 3x3 cluster:
```
@@@
@@@
@@@
```
The center roll has 8 neighbors - even if we remove corners/edges, the center stays protected.

#### Step 5: Visualization of Removal Process

```
Initial:          After round 1:    After round 2:    ... Final:
..@@.@@@@.        .......@..        ..........        ..........
@@@.@.@.@@        .@@.@.@.@@        .@@.....@.        ..........
@@@@@.@.@@        @@@@@...@@        .@@@@...@@        ..........
@.@@@@..@.        @.@@@@..@.        ..@@@@....        ...@@@....
@@.@@@@.@@        .@.@@@@.@.        .@.@@@@...        ...@@@@...
.@@@@@@@.@        .@@@@@@@.@        ..@@@@@@..        ...@@@@@..
.@.@.@.@@@        .@.@.@.@@@        ...@.@.@@@        ...@.@.@@.
@.@@@.@@@@        ..@@@.@@@@        ..@@@.@@@@        ...@@.@@@.
.@@@@@@@@.        .@@@@@@@@.        ..@@@@@@@.        ...@@@@@..
@.@.@@@.@.        ....@@@...        ....@@@...        ....@@@...
```

---

## Algorithm Complexity

### Part 2

**Time Complexity:**
- Each iteration: O(R × C) to scan the grid
- Maximum iterations: O(R × C) (at most one roll removed per iteration in worst case)
- Worst case: O((R × C)²)
- In practice: Much faster because multiple rolls are removed per iteration

**Space Complexity:**
- O(R × C) for the mutable grid
- O(R × C) for the list of accessible rolls (worst case)

---

## Key Insights

1. **Cascade Effect**: Removing rolls can expose previously inaccessible rolls
2. **Stable Clusters**: Dense clusters remain after all removals complete
3. **Simultaneous Removal**: We remove all accessible rolls in each round before recalculating
4. **Termination**: The algorithm always terminates because:
   - Each round removes at least 1 roll (if any are accessible)
   - Finite number of rolls means finite iterations

---

## Final Answers (My Input)
- **Part 1:** 1435
- **Part 2:** 8623
