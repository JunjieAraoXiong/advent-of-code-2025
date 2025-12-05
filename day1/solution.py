"""
Advent of Code 2025 - Day 1: Secret Entrance
"""


def solve_part1(input_file):
    """
    Part 1: Count how many times the dial LANDS on 0 after each rotation.
    """
    with open(input_file, 'r') as f:
        rotations = f.read().strip().split('\n')

    position = 50
    zero_count = 0

    for rotation in rotations:
        direction = rotation[0]
        distance = int(rotation[1:])

        if direction == 'R':
            position = (position + distance) % 100
        else:
            position = (position - distance) % 100

        if position == 0:
            zero_count += 1

    return zero_count


def solve_part2(input_file):
    """
    Part 2: Count how many times the dial CROSSES 0 during rotations.
    """
    with open(input_file, 'r') as f:
        rotations = f.read().strip().split('\n')

    position = 50
    zero_count = 0

    for rotation in rotations:
        direction = rotation[0]
        distance = int(rotation[1:])

        if direction == 'R':
            zero_count += (position + distance) // 100
            position = (position + distance) % 100
        else:
            if position == 0:
                crosses = distance // 100
            elif distance >= position:
                crosses = (distance - position) // 100 + 1
            else:
                crosses = 0
            zero_count += crosses
            position = (position - distance) % 100

    return zero_count


if __name__ == "__main__":
    import os
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_file = os.path.join(script_dir, "inputs.txt")

    print("Day 1: Secret Entrance")
    print("-" * 30)
    print(f"Part 1: {solve_part1(input_file)}")
    print(f"Part 2: {solve_part2(input_file)}")
