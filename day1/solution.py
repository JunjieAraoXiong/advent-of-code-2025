"""
Advent of Code 2025 - Day 1: Secret Entrance
Solution for both Part 1 and Part 2

Problem: A circular dial with numbers 0-99, starting at position 50.
We process rotation instructions (L/R + distance) and count how many times
the dial points at 0.
"""


def solve_part1(input_file):
    """
    Part 1: Count how many times the dial LANDS on 0 after each rotation.

    Approach:
    - Parse each rotation instruction (direction + distance)
    - Use modular arithmetic to handle the circular dial (% 100)
    - R (right) = add to position, L (left) = subtract from position
    - Count when final position after rotation equals 0
    """
    with open(input_file, 'r') as f:
        rotations = f.read().strip().split('\n')

    position = 50  # Dial starts at 50
    zero_count = 0

    for rotation in rotations:
        # Parse instruction: first char is direction, rest is distance
        direction = rotation[0]  # 'L' or 'R'
        distance = int(rotation[1:])  # numeric distance

        # Apply rotation using modular arithmetic (dial wraps at 100)
        if direction == 'R':
            position = (position + distance) % 100
        else:  # L
            position = (position - distance) % 100

        # Check if we landed on 0
        if position == 0:
            zero_count += 1

    return zero_count


def solve_part2(input_file):
    """
    Part 2: Count how many times the dial PASSES THROUGH 0 during any rotation.

    Key insight: We need to count every time the dial crosses 0, not just
    when it ends at 0.

    For RIGHT rotations (R):
    - We cross 0 when we go from 99 -> 0 (wrapping around)
    - Number of crossings = (position + distance) // 100
    - Example: From pos=95, R60 -> crosses 0 once (at step 5, position hits 100)

    For LEFT rotations (L):
    - We cross 0 when we go from 1 -> 0 (or wrap from 0 -> 99)
    - If starting at position P and moving left D steps:
      - If P == 0: first crossing at step 100, then every 100 steps
      - If P > 0: first crossing at step P (when we hit 0), then every 100 steps
    - Number of crossings = (distance - position) // 100 + 1 (if distance >= position)
    """
    with open(input_file, 'r') as f:
        rotations = f.read().strip().split('\n')

    position = 50  # Dial starts at 50
    zero_count = 0

    for rotation in rotations:
        direction = rotation[0]
        distance = int(rotation[1:])

        if direction == 'R':
            # Moving right: we hit 0 at absolute positions 100, 200, 300, etc.
            # Formula: (position + distance) // 100 gives number of times we wrap
            zero_count += (position + distance) // 100
            position = (position + distance) % 100
        else:  # L
            # Moving left: more complex calculation
            # We hit 0 at steps: position, position+100, position+200, etc.
            # But if position=0, we're LEAVING 0, not crossing it
            if position == 0:
                # Starting at 0, first crossing is at step 100 (full rotation back)
                crosses = distance // 100
            elif distance >= position:
                # We'll hit 0 at step=position, then again every 100 steps
                # Number of crossings = 1 + (remaining_distance) // 100
                crosses = (distance - position) // 100 + 1
            else:
                # We don't travel far enough to reach 0
                crosses = 0
            zero_count += crosses
            position = (position - distance) % 100

    return zero_count


if __name__ == "__main__":
    result1 = solve_part1("inputs.txt")
    print(f"Part 1: {result1}")

    result2 = solve_part2("inputs.txt")
    print(f"Part 2: {result2}")
