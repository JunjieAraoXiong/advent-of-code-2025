# Day 1: Secret Entrance - Step-by-Step Solution

## Problem Summary

You have a circular dial numbered 0-99 (100 positions). Starting at position 50, you follow a sequence of rotations:
- `R` = rotate right (toward higher numbers)
- `L` = rotate left (toward lower numbers)
- The dial wraps around: 99 + 1 = 0, and 0 - 1 = 99

---

## Part 1: Count Landings on Zero

**Goal:** Count how many times the dial **lands on 0** after completing a rotation.

### Step-by-Step Approach

#### Step 1: Understand Modular Arithmetic

The dial has 100 positions (0-99). When we go past 99, we wrap back to 0:
```
new_position = (current_position ± distance) % 100
```

Python's modulo handles negative numbers correctly:
- `95 + 10 = 105` → `105 % 100 = 5`
- `5 - 10 = -5` → `-5 % 100 = 95`

#### Step 2: Parse Input

Each line is a rotation instruction like `R48` or `L68`:
```python
direction = rotation[0]    # 'R' or 'L'
distance = int(rotation[1:])  # numeric part
```

#### Step 3: Simulate Each Rotation

```python
position = 50  # Starting position
zero_count = 0

for rotation in rotations:
    direction = rotation[0]
    distance = int(rotation[1:])

    if direction == 'R':
        position = (position + distance) % 100
    else:  # L
        position = (position - distance) % 100

    if position == 0:
        zero_count += 1
```

#### Step 4: Example Walkthrough

Starting at 50 with rotations: `L68, L30, R48, L5, R60, L55, L1, L99, R14, L82`

| Step | Rotation | Calculation | Position | Landed on 0? |
|------|----------|-------------|----------|--------------|
| 0 | (start) | - | 50 | - |
| 1 | L68 | (50 - 68) % 100 = -18 % 100 | 82 | No |
| 2 | L30 | (82 - 30) % 100 | 52 | No |
| 3 | R48 | (52 + 48) % 100 | **0** | **Yes** |
| 4 | L5 | (0 - 5) % 100 | 95 | No |
| 5 | R60 | (95 + 60) % 100 | 55 | No |
| 6 | L55 | (55 - 55) % 100 | **0** | **Yes** |
| 7 | L1 | (0 - 1) % 100 | 99 | No |
| 8 | L99 | (99 - 99) % 100 | **0** | **Yes** |
| 9 | R14 | (0 + 14) % 100 | 14 | No |
| 10 | L82 | (14 - 82) % 100 | 32 | No |

**Answer: 3** (landed on 0 three times)

### Time Complexity
O(n) where n = number of rotations

---

## Part 2: Count All Crossings Through Zero

**Goal:** Count how many times the dial **passes through 0** during any click, not just at the end.

### Step-by-Step Approach

#### Step 1: Understand the Difference

- Part 1: Only count when we END at 0
- Part 2: Count EVERY time we touch 0 during movement

Example: `R1000` from position 50 passes through 0 **ten times** (at positions 100, 200, 300, ... 1000 on the "unwrapped" number line).

#### Step 2: Formula for Right Rotations (R)

When moving right, we cross 0 every time we wrap from 99 → 0.

Think of positions on an infinite number line: 0, 1, ..., 99, 100, 101, ..., 199, 200, ...

We cross 0 at positions 100, 200, 300, etc.

**Formula:** `crossings = (position + distance) // 100`

**Examples:**
| Start | Distance | Calculation | Crossings |
|-------|----------|-------------|-----------|
| 50 | 60 | (50+60)//100 = 1 | 1 |
| 95 | 10 | (95+10)//100 = 1 | 1 |
| 50 | 1000 | (50+1000)//100 = 10 | 10 |
| 50 | 40 | (50+40)//100 = 0 | 0 |

#### Step 3: Formula for Left Rotations (L)

When moving left, we cross 0 when we go from 1 → 0.

**Key insight:** If we START at 0 and move left, we go to 99 first - we're leaving 0, not crossing through it.

**Three cases:**

1. **Starting at 0:** First crossing is at step 100 (full rotation back)
   ```python
   crossings = distance // 100
   ```

2. **Starting at position P > 0, moving distance D >= P:**
   - First crossing at step P (when we hit 0)
   - Additional crossings every 100 steps
   ```python
   crossings = (distance - position) // 100 + 1
   ```

3. **Starting at position P, moving distance D < P:**
   - We don't go far enough to reach 0
   ```python
   crossings = 0
   ```

#### Step 4: Combined Code

```python
position = 50
zero_count = 0

for rotation in rotations:
    direction = rotation[0]
    distance = int(rotation[1:])

    if direction == 'R':
        zero_count += (position + distance) // 100
        position = (position + distance) % 100
    else:  # L
        if position == 0:
            crosses = distance // 100
        elif distance >= position:
            crosses = (distance - position) // 100 + 1
        else:
            crosses = 0
        zero_count += crosses
        position = (position - distance) % 100
```

#### Step 5: Example Walkthrough

Starting at 50 with same rotations:

| Step | Rotation | Start Pos | Crossings | End Pos |
|------|----------|-----------|-----------|---------|
| 1 | L68 | 50 | (68-50)//100 + 1 = 1 | 82 |
| 2 | L30 | 82 | 30 < 82, so 0 | 52 |
| 3 | R48 | 52 | (52+48)//100 = 1 | 0 |
| 4 | L5 | 0 | 5//100 = 0 | 95 |
| 5 | R60 | 95 | (95+60)//100 = 1 | 55 |
| 6 | L55 | 55 | (55-55)//100 + 1 = 1 | 0 |
| 7 | L1 | 0 | 1//100 = 0 | 99 |
| 8 | L99 | 99 | (99-99)//100 + 1 = 1 | 0 |
| 9 | R14 | 0 | (0+14)//100 = 0 | 14 |
| 10 | L82 | 14 | (82-14)//100 + 1 = 1 | 32 |

**Total crossings: 1+0+1+0+1+1+0+1+0+1 = 6**

---

## Summary

| Part | Question | Approach | Example Answer |
|------|----------|----------|----------------|
| 1 | How many times do we land on 0? | Simple modular arithmetic, check if position == 0 | 3 |
| 2 | How many times do we pass through 0? | Count wrap-arounds using integer division | 6 |

## Final Answers (My Input)
- **Part 1:** 1123
- **Part 2:** 6695
