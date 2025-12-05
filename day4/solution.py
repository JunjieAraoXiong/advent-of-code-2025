"""
Day 4: Printing Department
--------------------------
Problem: Count rolls of paper (@) that are accessible by forklifts.
A roll is accessible if it has fewer than 4 rolls in its 8 adjacent positions.

Part 1: Count accessible rolls (in a single pass)
Part 2: Count total rolls that can be removed by repeatedly removing accessible rolls
"""


def parse_input(input_file):
    """Parse the input file into a 2D grid."""
    with open(input_file, 'r') as f:
        grid = [line.rstrip('\n') for line in f if line.strip()]
    return grid


def count_adjacent_rolls(grid, row, col):
    """
    Count the number of adjacent rolls (@) in the 8 neighboring positions.

    The 8 directions are:
    - Up-left, Up, Up-right
    - Left, Right
    - Down-left, Down, Down-right
    """
    rows = len(grid)
    cols = len(grid[0]) if rows > 0 else 0

    # 8 directions: (row_delta, col_delta)
    directions = [
        (-1, -1), (-1, 0), (-1, 1),  # up-left, up, up-right
        (0, -1),           (0, 1),   # left, right
        (1, -1),  (1, 0),  (1, 1)    # down-left, down, down-right
    ]

    count = 0
    for dr, dc in directions:
        new_row, new_col = row + dr, col + dc
        # Check bounds
        if 0 <= new_row < rows and 0 <= new_col < cols:
            if grid[new_row][new_col] == '@':
                count += 1

    return count


def solve_part1(input_file):
    """
    Count how many rolls of paper can be accessed by a forklift.
    A roll is accessible if it has fewer than 4 adjacent rolls.
    """
    grid = parse_input(input_file)

    accessible_count = 0
    rows = len(grid)
    cols = len(grid[0]) if rows > 0 else 0

    for row in range(rows):
        for col in range(cols):
            # Only check positions that have a roll (@)
            if grid[row][col] == '@':
                adjacent = count_adjacent_rolls(grid, row, col)
                # Accessible if fewer than 4 adjacent rolls
                if adjacent < 4:
                    accessible_count += 1

    return accessible_count


def verify_example():
    """Verify the solution with the example from the problem."""
    example_grid = [
        "..@@.@@@@.",
        "@@@.@.@.@@",
        "@@@@@.@.@@",
        "@.@@@@..@.",
        "@@.@@@@.@@",
        ".@@@@@@@.@",
        ".@.@.@.@@@",
        "@.@@@.@@@@",
        ".@@@@@@@@.",
        "@.@.@@@.@."
    ]

    accessible_count = 0
    rows = len(example_grid)
    cols = len(example_grid[0])

    # Track which positions are accessible for visualization
    accessible_positions = []

    for row in range(rows):
        for col in range(cols):
            if example_grid[row][col] == '@':
                # Count adjacent rolls
                directions = [
                    (-1, -1), (-1, 0), (-1, 1),
                    (0, -1),           (0, 1),
                    (1, -1),  (1, 0),  (1, 1)
                ]
                count = 0
                for dr, dc in directions:
                    new_row, new_col = row + dr, col + dc
                    if 0 <= new_row < rows and 0 <= new_col < cols:
                        if example_grid[new_row][new_col] == '@':
                            count += 1

                if count < 4:
                    accessible_count += 1
                    accessible_positions.append((row, col))

    print("Example verification:")
    print(f"  Accessible rolls: {accessible_count}")
    print(f"  Expected: 13")
    print(f"  Match: {accessible_count == 13}")

    # Show accessible positions
    print("\n  Accessible positions (marked with 'x' in problem):")
    for row, col in accessible_positions:
        print(f"    Row {row}, Col {col}")

    return accessible_count == 13


def find_accessible_rolls(grid):
    """
    Find all rolls that are currently accessible (fewer than 4 adjacent rolls).
    Returns a list of (row, col) positions.
    """
    accessible = []
    rows = len(grid)
    cols = len(grid[0]) if rows > 0 else 0

    for row in range(rows):
        for col in range(cols):
            if grid[row][col] == '@':
                adjacent = count_adjacent_rolls(grid, row, col)
                if adjacent < 4:
                    accessible.append((row, col))

    return accessible


def solve_part2(input_file, visualize=False):
    """
    Count total rolls that can be removed by repeatedly removing accessible rolls.

    Process:
    1. Find all accessible rolls (fewer than 4 adjacent rolls)
    2. Remove them all
    3. Repeat until no more rolls are accessible
    4. Return total count of removed rolls
    """
    grid = parse_input(input_file)
    # Convert to mutable list of lists
    grid = [list(row) for row in grid]

    total_removed = 0
    iteration = 0

    if visualize:
        # Count initial rolls
        initial_rolls = sum(row.count('@') for row in grid)
        print(f"\nInitial state: {initial_rolls} rolls")
        print_grid_summary(grid)

    while True:
        # Find all currently accessible rolls
        accessible = find_accessible_rolls(grid)

        if not accessible:
            # No more rolls can be removed
            break

        iteration += 1

        if visualize:
            print(f"\n{'='*50}")
            print(f"Iteration {iteration}: Removing {len(accessible)} rolls")
            # Show grid with accessible rolls highlighted
            print_grid_with_highlights(grid, accessible)

        # Remove all accessible rolls
        for row, col in accessible:
            grid[row][col] = '.'

        total_removed += len(accessible)

        if visualize:
            remaining = sum(row.count('@') for row in grid)
            print(f"Total removed so far: {total_removed}, Remaining: {remaining}")

    if visualize:
        print(f"\n{'='*50}")
        print("FINAL STATE (stable cluster remaining):")
        print_grid_summary(grid)
        remaining = sum(row.count('@') for row in grid)
        print(f"\nTotal rolls removed: {total_removed}")
        print(f"Rolls remaining (stable): {remaining}")

    return total_removed


def print_grid_summary(grid, max_rows=20):
    """Print a summary of the grid (first and last few rows if large)."""
    rows = len(grid)
    cols = len(grid[0]) if rows > 0 else 0

    if rows <= max_rows:
        for row in grid:
            print(''.join(row))
    else:
        # Show first 8 and last 8 rows
        print(f"  (showing first 8 and last 8 of {rows} rows, {cols} cols)")
        for i in range(8):
            print(f"  {''.join(grid[i])}")
        print(f"  ... ({rows - 16} rows omitted) ...")
        for i in range(rows - 8, rows):
            print(f"  {''.join(grid[i])}")


def print_grid_with_highlights(grid, highlights, max_rows=20):
    """
    Print grid with highlighted positions shown as 'X' (rolls about to be removed).
    """
    highlight_set = set(highlights)
    rows = len(grid)

    if rows <= max_rows:
        for r, row in enumerate(grid):
            line = ''
            for c, char in enumerate(row):
                if (r, c) in highlight_set:
                    line += 'X'  # Highlighted (about to be removed)
                else:
                    line += char
            print(line)
    else:
        print(f"  ({len(highlights)} rolls marked for removal across {rows} rows)")


def visualize_example():
    """Run the example with full visualization."""
    example_grid = [
        list("..@@.@@@@."),
        list("@@@.@.@.@@"),
        list("@@@@@.@.@@"),
        list("@.@@@@..@."),
        list("@@.@@@@.@@"),
        list(".@@@@@@@.@"),
        list(".@.@.@.@@@"),
        list("@.@@@.@@@@"),
        list(".@@@@@@@@."),
        list("@.@.@@@.@.")
    ]

    print("\n" + "=" * 60)
    print("VISUAL WALKTHROUGH - Example Grid")
    print("=" * 60)

    # Count initial rolls
    initial_rolls = sum(row.count('@') for row in example_grid)
    print(f"\nInitial state ({initial_rolls} rolls):")
    print("Legend: @ = roll, . = empty, X = about to be removed")
    print()
    for row in example_grid:
        print(''.join(row))

    total_removed = 0
    iteration = 0

    while True:
        accessible = find_accessible_rolls(example_grid)

        if not accessible:
            break

        iteration += 1
        highlight_set = set(accessible)

        print(f"\n{'-'*60}")
        print(f"Iteration {iteration}: Found {len(accessible)} accessible rolls (marked X)")
        print()

        # Print with highlights
        for r, row in enumerate(example_grid):
            line = ''
            for c, char in enumerate(row):
                if (r, c) in highlight_set:
                    line += 'X'
                else:
                    line += char
            print(line)

        # Remove rolls
        for row, col in accessible:
            example_grid[row][col] = '.'

        total_removed += len(accessible)
        remaining = sum(row.count('@') for row in example_grid)

        print(f"\nAfter removal: {len(accessible)} removed, {remaining} remaining")

    print(f"\n{'='*60}")
    print("FINAL STATE (no more accessible rolls):")
    print()
    for row in example_grid:
        print(''.join(row))

    remaining = sum(row.count('@') for row in example_grid)
    print(f"\n{'='*60}")
    print(f"SUMMARY:")
    print(f"  Initial rolls:  {initial_rolls}")
    print(f"  Total removed:  {total_removed}")
    print(f"  Remaining:      {remaining}")
    print(f"  Iterations:     {iteration}")
    print("=" * 60)


def verify_example_part2():
    """Verify Part 2 solution with the example from the problem."""
    example_grid = [
        list("..@@.@@@@."),
        list("@@@.@.@.@@"),
        list("@@@@@.@.@@"),
        list("@.@@@@..@."),
        list("@@.@@@@.@@"),
        list(".@@@@@@@.@"),
        list(".@.@.@.@@@"),
        list("@.@@@.@@@@"),
        list(".@@@@@@@@."),
        list("@.@.@@@.@.")
    ]

    total_removed = 0
    iteration = 0

    while True:
        accessible = find_accessible_rolls(example_grid)

        if not accessible:
            break

        iteration += 1
        removed_count = len(accessible)

        # Remove all accessible rolls
        for row, col in accessible:
            example_grid[row][col] = '.'

        total_removed += removed_count

    print("Part 2 Example verification:")
    print(f"  Total rolls removed: {total_removed}")
    print(f"  Expected: 43")
    print(f"  Match: {total_removed == 43}")

    return total_removed == 43


if __name__ == "__main__":
    import sys
    import os

    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_file = os.path.join(script_dir, "inputs.txt")

    # Check for visualization flag
    show_visual = '--visual' in sys.argv or '-v' in sys.argv

    if show_visual:
        visualize_example()
        print()

    print("Day 4: Printing Department")
    print("-" * 30)
    print(f"Part 1: {solve_part1(input_file)}")
    print(f"Part 2: {solve_part2(input_file, visualize=False)}")

    if not show_visual:
        print("\nTip: Run with --visual flag for step-by-step visualization")
